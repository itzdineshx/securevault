from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import os
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json
import logging # Import the logging library
from dotenv import load_dotenv

# Load environment variables from .env when present
load_dotenv()

# Import utilities
from utils import process_upload, fetch_and_display_blockchain_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Database URL from environment (allows swapping SQLite for other DBs in production)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./securevault.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_hash = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Blockchain structure
class Block:
    def __init__(self, index, timestamp, file_hash, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.file_hash}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, datetime.utcnow(), "0" * 64, "0" * 64)
        self.chain.append(genesis_block)

    def add_block(self, file_hash):
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow(),
            file_hash=file_hash,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

# Initialize blockchain
blockchain = Blockchain()

app = FastAPI(title="Secure File Upload API")

# Configure CORS origins via environment variable (comma separated)
cors_origins_raw = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:8501")
cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadResponse(BaseModel):
    filename: str
    file_hash: str
    block: dict

class BlockResponse(BaseModel):
    index: int
    timestamp: str
    file_hash: str
    previous_hash: str
    block_hash: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "text/plain"]
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type uploaded: {file.content_type} for file {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, JPG, PNG, and TXT files are allowed.")
    
    try:
        logger.info(f"Starting upload process for file: {file.filename}")
        # Save file
        file_path = os.path.join("uploads", file.filename)
        logger.info(f"Saving file to: {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        logger.info(f"File saved successfully.")
        
        # Calculate SHA-256 hash
        file_hash = hashlib.sha256(content).hexdigest()
        logger.info(f"Calculated file hash: {file_hash}")
        
        # Check if file hash already exists
        logger.info("Checking for existing file hash in database.")
        existing_upload = db.query(Upload).filter(Upload.file_hash == file_hash).first()
        if existing_upload:
            logger.warning(f"File already exists with hash: {file_hash}")
            raise HTTPException(status_code=400, detail="File already exists in the system")
        
        # Save to database
        logger.info("Adding file metadata to database.")
        upload = Upload(filename=file.filename, file_hash=file_hash)
        db.add(upload)
        db.commit()
        logger.info("Database commit successful.")
        
        # Add to blockchain
        logger.info("Adding block to blockchain.")
        new_block = blockchain.add_block(file_hash)
        logger.info(f"New block added with index: {new_block.index}")
        
        # Prepare block data for response
        block_data = {
            "index": new_block.index,
            "timestamp": new_block.timestamp.isoformat(),
            "file_hash": new_block.file_hash,
            "previous_hash": new_block.previous_hash,
            "hash": new_block.hash
        }
        
        logger.info(f"Upload successful for file: {file.filename}")
        return UploadResponse(
            filename=file.filename,
            file_hash=file_hash,
            block=block_data
        )
        
    except HTTPException as http_exc:
        # Re-raise HTTPException to return specific error messages
        logger.error(f"HTTPException during upload: {http_exc.detail}", exc_info=True)
        raise http_exc
        
    except Exception as e:
        # Log the detailed error before raising a generic 500
        logger.error(f"An unexpected error occurred during upload for file {file.filename}: {e}", exc_info=True) 
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

@app.get("/chain/")
async def get_chain():
    return {
        "chain": [
            {
                "index": block.index,
                "timestamp": block.timestamp.isoformat(),
                "file_hash": block.file_hash,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            }
            for block in blockchain.chain
        ],
        "length": len(blockchain.chain)
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/log/", response_model=List[BlockResponse])
async def get_blockchain_log():
    return [
        BlockResponse(
            index=block.index,
            timestamp=block.timestamp.isoformat(),
            file_hash=block.file_hash,
            previous_hash=block.previous_hash,
            block_hash=block.hash
        )
        for block in blockchain.chain
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))
