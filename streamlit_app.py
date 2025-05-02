import streamlit as st
import requests
from requests.exceptions import RequestException
import pandas as pd
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="SecureVault",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Remove the white top bar */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Remove the padding at the top */
    .stApp {
        margin-top: -3rem;
    }
    
    /* Customize the main app background */
    .stApp {
        background: linear-gradient(135deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
        min-height: 100vh;
    }
    
    /* Main content area styling */
    .main-content {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Upload section styling */
    .upload-section {
        background: rgba(248, 249, 250, 0.9);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Log table styling */
    .log-table {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #1a2a6c, #b21f1f);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #b21f1f, #1a2a6c);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(26, 42, 108, 0.9);
        color: white;
        backdrop-filter: blur(10px);
    }
    
    .sidebar .sidebar-content .stRadio > div {
        color: white;
    }
    
    /* Success box styling */
    .success-box {
        background: rgba(232, 245, 233, 0.9);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }
    
    /* Error box styling */
    .error-box {
        background: rgba(255, 235, 238, 0.9);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid rgba(244, 67, 54, 0.2);
    }
    
    /* Custom title styling */
    .custom-title {
        color: white;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Custom subtitle styling */
    .custom-subtitle {
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# Add custom header
st.markdown("""
    <div class="custom-title">
        <h1>🔒 SecureVault</h1>
    </div>
    <div class="custom-subtitle">
        <h3>Secure Document Upload & Blockchain Verification</h3>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🔒 SecureVault")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "",
    ["📤 Upload Document", "📋 Blockchain Log"],
    label_visibility="collapsed"
)

# Add sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
    SecureVault uses blockchain technology to ensure the integrity and security of your uploaded documents.
    
    - 🔒 Secure file storage
    - ⛓️ Blockchain verification
    - 📝 Document history tracking
""")

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if page == "📤 Upload Document":
    st.title("📤 Upload Document")
    st.markdown("Upload your Aadhaar card or other documents securely.")
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "jpg", "jpeg", "png"],
        help="Supported formats: PDF, JPG, PNG"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            # Prepare the file for upload
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            # Show upload button
            if st.button("Upload File", key="upload_btn"):
                with st.spinner("Uploading file..."):
                    # Send file to FastAPI backend
                    response = requests.post(
                        "http://localhost:8000/upload",
                        files=files
                    )
                    
                    # Check if the request was successful
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ File uploaded successfully!")
                        
                        # Display file details
                        st.markdown("### 📄 File Details")
                        st.markdown(f"**📎 Filename:** {result['filename']}")
                        st.markdown(f"**🔑 File Hash:** `{result['file_hash']}`")
                        
                        # Display block details
                        st.markdown("### ⛓️ Block Details")
                        st.markdown(f"**#️⃣ Index:** {result['block']['index']}")
                        st.markdown(f"**⏰ Timestamp:** {result['block']['timestamp']}")
                        st.markdown(f"**🔗 Block Hash:** `{result['block']['hash']}`")
                        st.markdown(f"**⏮️ Previous Hash:** `{result['block']['previous_hash']}`")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Show success animation
                        st.balloons()
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error(f"❌ Error uploading file: {response.text}")
                        st.markdown('</div>', unsafe_allow_html=True)
        
        except RequestException as e:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ Failed to connect to the server. Please make sure the FastAPI backend is running. Error: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)

else:  # Blockchain Log page
    st.title("📋 Blockchain Log")
    st.markdown("View the complete blockchain history of uploaded files.")
    
    # Add refresh button
    if st.button("🔄 Refresh Log", key="refresh_btn"):
        st.experimental_rerun()
    
    try:
        # Fetch blockchain data
        response = requests.get("http://localhost:8000/log/")
        
        if response.status_code == 200:
            blocks = response.json()
            
            if blocks:
                # Convert to DataFrame for better display
                df = pd.DataFrame(blocks)
                
                # Format the DataFrame
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Display the table with custom styling
                st.markdown('<div class="log-table">', unsafe_allow_html=True)
                st.dataframe(
                    df,
                    column_config={
                        "index": "Index",
                        "timestamp": "Timestamp",
                        "file_hash": "File Hash",
                        "previous_hash": "Previous Hash",
                        "block_hash": "Block Hash"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ No blocks in the blockchain yet.")
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error(f"❌ Error fetching blockchain data: {response.text}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    except RequestException as e:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ Failed to connect to the server. Please make sure the FastAPI backend is running. Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 