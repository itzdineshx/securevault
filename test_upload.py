import requests
import os

# Test file path
TEST_FILE = "test.txt"

def test_upload(file_path):
    if not os.path.exists(file_path):
        print(f"Test file not found: {file_path}")
        return
    
    from dotenv import load_dotenv
    load_dotenv()
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    url = f"{BACKEND_URL}/upload/"
    files = {'file': open(file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"\nTesting file upload:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing upload: {str(e)}")
    finally:
        files['file'].close()

if __name__ == "__main__":
    print("Testing file upload API...")
    test_upload(TEST_FILE)