import streamlit as st
from datetime import datetime
import pandas as pd
from utils import process_upload, fetch_and_display_blockchain_data
from utils import fetch_blocks, download_file_bytes
import json
import hashlib

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
            ["📤 Upload Document", "📋 Blockchain Log", "✅ Verify File"],
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
                # Show a compact preview/info area for the selected file
                with col1:
                    st.markdown("", unsafe_allow_html=True)
                    try:
                        if uploaded_file.type.startswith("image"):
                            st.image(uploaded_file, width=600, clamp=True)
                    except Exception:
                        pass

                with col2:
                    st.markdown("<div class='card compact'>", unsafe_allow_html=True)
                    st.markdown(f"**Filename:** {uploaded_file.name}")
                    st.markdown(f"**Type:** {uploaded_file.type or 'N/A'}")
                    try:
                        size_kb = round(len(uploaded_file.getvalue()) / 1024, 1)
                        st.markdown(f"**Size:** {size_kb} KB")
                    except Exception:
                        pass
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Add margin-top to button for better spacing
                    st.markdown("<style>.stButton button { margin-top: 8px; }</style>", unsafe_allow_html=True)
                    upload_btn = st.button(
                        "Upload File", 
                        key="upload_btn",
                        use_container_width=False,
                        help="Click to upload and secure your document",
                        type="primary"
                    )
        
    # Removed the surrounding `.card` to avoid large empty space above uploader.
    
    if uploaded_file and upload_btn:
        # Show a compact progress indicator and notifications
        progress = st.progress(0)
        try:
            progress.progress(30)
            process_upload(uploaded_file) # Call utility function
            progress.progress(100)
            st.success("Upload complete — block added to the chain.")
        except Exception as e:
            st.error(f"Upload failed: {e}")
        finally:
            progress.empty()

# ---------- BLOCKCHAIN LOG COMPONENT ---------- #
def render_blockchain_log():
    """Render the blockchain log page with visualization."""
    st.header("📋 Blockchain Log", anchor=False)
    st.write("View the complete blockchain history of uploaded files.")

    # Compact refresh button centered in the page
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        refresh_btn = st.button(
            "🔄 Refresh Log",
            key="refresh_btn",
            help="Click to refresh the blockchain data",
            use_container_width=True,
        )
    
    if refresh_btn:
        st.rerun()

    # Fetch blocks for stats, recent strip, and export
    blocks = fetch_blocks()

    # Top stats: total blocks, last upload
    total_blocks = len(blocks)
    last_ts = None
    last_block_hash = None
    if total_blocks:
        try:
            last_ts = blocks[-1].get('timestamp')
            last_block_hash = blocks[-1].get('block_hash')
        except Exception:
            last_ts = None
            last_block_hash = None

    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.markdown("<div class='card compact'>", unsafe_allow_html=True)
        st.metric("Total Blocks", total_blocks)
        st.markdown("</div>", unsafe_allow_html=True)
    with stat2:
        st.markdown("<div class='card compact'>", unsafe_allow_html=True)
        st.metric("Last Upload", last_ts or "—")
        st.markdown("</div>", unsafe_allow_html=True)
    with stat3:
        st.markdown("<div class='card compact'>", unsafe_allow_html=True)
        st.metric("Latest Hash", (last_block_hash[:10] + "…") if last_block_hash else "—")
        st.markdown("</div>", unsafe_allow_html=True)
    with stat4:
        st.markdown("<div class='card compact'>", unsafe_allow_html=True)
        st.markdown("**Export**")
        export_cols = st.columns(2)
        with export_cols[0]:
            st.download_button(
                "JSON",
                data=json.dumps(blocks, default=str),
                file_name="blockchain.json",
                mime="application/json",
                use_container_width=True,
                key="download_json_btn",
            )
        with export_cols[1]:
            try:
                import pandas as _pd
                df = _pd.DataFrame(blocks)
                st.download_button(
                    "CSV",
                    data=df.to_csv(index=False),
                    file_name="blockchain.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_csv_btn",
                )
            except Exception:
                st.caption("CSV export unavailable")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Recent uploads strip (show thumbnails or file icons)
    recent = fetch_blocks(limit=6)
    if recent:
        st.subheader("Recent Uploads")
        row_size = 3
        rows = [recent[i : i + row_size] for i in range(0, len(recent), row_size)]
        for row in rows:
            cols = st.columns(row_size)
            for idx, blk in enumerate(row):
                with cols[idx]:
                    st.markdown("<div class='card compact'>", unsafe_allow_html=True)
                    fn = blk.get('filename', blk.get('file_hash', 'file'))
                    is_image = isinstance(fn, str) and fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
                    if is_image:
                        data = download_file_bytes(blk.get('file_hash'))
                        if data:
                            try:
                                st.image(data, width=180)
                            except Exception:
                                st.write("🖼️ Image")
                        else:
                            st.write("🖼️ Image")
                    else:
                        st.markdown("### 📄")
                    st.write(fn)
                    st.caption(f"Block #{blk.get('index', '—')}")
                    file_bytes = None
                    try:
                        file_bytes = download_file_bytes(blk.get('file_hash'))
                    except Exception:
                        file_bytes = None
                    if file_bytes:
                        st.download_button(
                            "Download file",
                            data=file_bytes,
                            file_name=fn,
                            use_container_width=True,
                            key=f"recent_download_{blk.get('index', idx)}",
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No recent uploads to show.")

    st.divider()

    # Finally render the graph & table using existing utility (which includes compact cards)
    fetch_and_display_blockchain_data()


# ---------- VERIFY COMPONENT ---------- #
def render_verify_page():
    """Render the dedicated verification page with chain integrity and hash checks."""
    st.header("✅ Verify File", anchor=False)
    st.write("Verify a document against the blockchain, inspect matches, and confirm chain integrity.")

    left, right = st.columns([1.2, 0.8])
    with left:
        verify_file = st.file_uploader(
            "Upload a file to verify",
            type=["pdf", "jpg", "jpeg", "png", "txt"],
            key="verify_uploader_page",
            help="Compare the file hash against the blockchain records."
        )
        verify_hash = st.text_input(
            "Or paste a file hash",
            key="verify_hash_page",
            placeholder="64-character SHA-256 hash"
        )
        verify_btn = st.button("Verify File", key="verify_btn_page", type="primary")

    with right:
        blocks = fetch_blocks()
        total_blocks = len(blocks)
        chain_ok = True
        for idx, block in enumerate(blocks):
            if idx > 0 and block.get("previous_hash") != blocks[idx - 1].get("block_hash"):
                chain_ok = False
                break

        st.markdown("<div class='card compact'>", unsafe_allow_html=True)
        st.metric("Total Blocks", total_blocks)
        st.metric("Chain Integrity", "Valid" if chain_ok else "Broken")
        st.markdown("</div>", unsafe_allow_html=True)

    if verify_btn:
        target_hash = None
        file_name = None
        if verify_file is not None:
            try:
                data = verify_file.getvalue()
                target_hash = hashlib.sha256(data).hexdigest()
                file_name = verify_file.name
            except Exception as e:
                st.error(f"Could not read uploaded file: {e}")
        elif verify_hash:
            target_hash = verify_hash.strip()

        if not target_hash:
            st.warning("Please upload a file or provide a hash to verify.")
            return

        matches = [b for b in blocks if b.get("file_hash") == target_hash]
        if matches:
            st.success(f"Verified: match found in {len(matches)} block(s).")
            for match in matches:
                info1, info2 = st.columns([1, 1])
                with info1:
                    st.markdown("<div class='card compact'>", unsafe_allow_html=True)
                    st.write(f"**Filename:** {match.get('filename', 'Unknown')}")
                    st.write(f"**Index:** {match.get('index', '—')}")
                    st.write(f"**Timestamp:** {match.get('timestamp', '—')}")
                    st.markdown("</div>", unsafe_allow_html=True)
                with info2:
                    st.markdown("<div class='card compact'>", unsafe_allow_html=True)
                    st.code(match.get('file_hash', ''), language=None)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("No matching file hash found in the blockchain.")

        st.divider()
        st.subheader("Verification Summary")
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("Input Type", "File" if verify_file is not None else "Hash")
        with summary_cols[1]:
            st.metric("Target Hash", (target_hash[:12] + "…") if target_hash else "—")
        with summary_cols[2]:
            st.metric("Source", file_name or "Manual Input")
