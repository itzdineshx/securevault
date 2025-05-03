import streamlit as st
from datetime import datetime
import pandas as pd
from utils import process_upload, fetch_and_display_blockchain_data

# ---------- HEADER COMPONENT ---------- #
def render_header():
    """Render the application header."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 SecureVault", anchor=False)
        st.markdown("<p style='font-size: 1.2rem; font-weight: 500; text-align: center;'>Secure Document Upload & Blockchain Verification</p>", unsafe_allow_html=True)

# ---------- SIDEBAR COMPONENT ---------- #
def render_sidebar():
    """Render the application sidebar with navigation."""
    with st.sidebar:
        st.title("🔒 SecureVault")
        st.divider()
        
        st.subheader("Navigation")
        page = st.radio(
            "Choose a page",
            ["📤 Upload Document", "📋 Blockchain Log"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        st.subheader("About")
        with st.expander("What is SecureVault?", expanded=True):
            # Use markdown directly for better theme handling
            st.markdown("""
                SecureVault uses blockchain technology to ensure the integrity 
                and security of your uploaded documents.
                
                - 🔒 Secure file storage
                - ⛓️ Blockchain verification
                - 📝 Document history tracking
            """)
        
        # Theme toggle might need adjustment depending on Streamlit version/handling
        # st.divider()
        # st.toggle("Dark Mode", help="Toggle between light and dark theme") 
        # Commenting out toggle as direct theme control is complex and often built-in
        
    return page

# ---------- UPLOAD COMPONENT ---------- #
def render_upload_page():
    """Render the document upload page."""
    st.header("📤 Upload Document", anchor=False)
    # Move the description text outside/before the card
    st.write("Upload your documents securely with blockchain verification.") 
    
    # Start the card containing the uploader and expander
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    # st.write("Upload your documents securely with blockchain verification.") # Remove from inside card
    
    with st.expander("Supported File Types", expanded=False):
        st.write("""
        - PDF documents (.pdf)
        - Images (.jpg, .jpeg, .png)
        - Text files (.txt) - If supported by backend
        
        Files are securely hashed and recorded in the blockchain.
        """)
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a file to upload",
                type=["pdf", "jpg", "jpeg", "png", "txt"], # Ensure backend supports txt if listed
                help="Supported formats: PDF, JPG, PNG, TXT",
                label_visibility="visible",
                key="file_uploader"
            )
        
        upload_btn = False # Initialize upload_btn
        if uploaded_file:
            with col2:
                # Add margin-top to button for better spacing
                st.markdown("<style>.stButton button { margin-top: 28px; }</style>", unsafe_allow_html=True)
                upload_btn = st.button(
                    "Upload File", 
                    key="upload_btn",
                    use_container_width=True,
                    help="Click to upload and secure your document",
                    type="primary"
                )
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file and upload_btn:
        process_upload(uploaded_file) # Call utility function

# ---------- BLOCKCHAIN LOG COMPONENT ---------- #
def render_blockchain_log():
    """Render the blockchain log page with visualization."""
    st.header("📋 Blockchain Log", anchor=False)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("View the complete blockchain history of uploaded files.")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        refresh_btn = st.button(
            "🔄 Refresh Log", 
            key="refresh_btn",
            help="Click to refresh the blockchain data",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if refresh_btn:
        st.rerun()
    
    fetch_and_display_blockchain_data() # Call utility function 