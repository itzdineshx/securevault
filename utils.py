import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
from requests.exceptions import RequestException
import pandas as pd
from datetime import datetime
import graphviz

# Backend URL can be injected via env for containerized deployments
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000") # Define backend URL constant


# ---------- UPLOAD PROCESSING ---------- #
def process_upload(uploaded_file):
    """Process the file upload and display results."""
    try:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        
        with st.spinner("Uploading and securing your document..."):
            response = requests.post(f"{BACKEND_URL}/upload/", files=files)
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ File uploaded successfully!")
                
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["📄 File Details", "⛓️ Block Details"])
                
                with tab1:
                    st.metric("Filename", result['filename'])
                    st.markdown("**File Hash:**")
                    st.code(result['file_hash'], language=None)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Block Index", result['block']['index'])
                        # Safely format timestamp
                        try:
                            ts = datetime.fromisoformat(result['block']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        except (ValueError, TypeError):
                            ts = result['block']['timestamp'] # Fallback
                        st.metric("Timestamp", ts)
                    with col2:
                        st.markdown("**Block Hash:**")
                        st.code(result['block']['hash'], language=None)
                        st.markdown("**Previous Hash:**")
                        st.code(result['block']['previous_hash'], language=None)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.balloons()
            else:
                try: # Try to parse detail from JSON error
                    error_detail = response.json().get("detail", response.text)
                except requests.exceptions.JSONDecodeError:
                    error_detail = response.text # Fallback to raw text
                st.error(f"❌ Error uploading file: {error_detail}")
    
    except RequestException as e:
        st.error(f"❌ Failed to connect to the server ({BACKEND_URL}). Please ensure it's running. Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")

# ---------- BLOCKCHAIN DATA HANDLING ---------- #
def create_blockchain_graph(blocks):
    """Create a Graphviz graph representing the blockchain."""
    dot = graphviz.Digraph(comment='Blockchain', format='svg')
    dot.attr(rankdir='LR') 
    # Use theme variables for node colors if possible, fallback otherwise
    # Note: Accessing CSS variables directly isn't straightforward in Python
    # Using fixed colors that work reasonably well in light/dark for now
    dot.attr('node', shape='box', style='filled', fillcolor='#e0f2fe', fontname='Helvetica', fontsize='10', color='#a5f3fc', fontcolor='#0e7490') 
    dot.attr('edge', fontname='Helvetica', fontsize='8', color='#94a3b8', fontcolor='#334155')

    if not blocks:
        return dot

    for i, block in enumerate(blocks):
        node_label = f"Block {block['index']}\n{block['block_hash'][:8]}..."
        dot.node(str(block['index']), label=node_label)
        
        if i > 0:
            prev_block_index = str(blocks[i-1]['index'])
            curr_block_index = str(block['index'])
            edge_label = f"{block['previous_hash'][:8]}..."
            dot.edge(prev_block_index, curr_block_index, label=edge_label)
            
    return dot

def fetch_and_display_blockchain_data():
    """Fetch blockchain data and display it as a graph and a table in tabs."""
    try:
            with st.spinner("Fetching blockchain data..."):
            response = requests.get(f"{BACKEND_URL}/log/")
            
            if response.status_code == 200:
                blocks = response.json()
                
                if blocks:
                    tab1, tab2 = st.tabs(["📊 Visual Representation", "💾 Raw Data"])
                    
                    with tab1:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.subheader("Blockchain Structure")
                        blockchain_graph = create_blockchain_graph(blocks)
                        # Try rendering the graph, catch potential Graphviz errors
                        try:
                            st.graphviz_chart(blockchain_graph)
                            st.caption("Each block is linked to the previous one using its hash.")
                        except Exception as graph_err:
                            st.warning(f"Could not render graph. Graphviz might not be installed correctly. Error: {graph_err}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with tab2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.subheader("Blockchain Data Table")
                        df = pd.DataFrame(blocks)
                        # Safely format timestamp in DataFrame
                        try:
                           df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                        except (ValueError, TypeError):
                           st.warning("Could not format timestamp column correctly.")
                           pass # Keep original timestamp if conversion fails
                           
                        st.dataframe(
                            df,
                            column_config={
                                "index": st.column_config.NumberColumn("Index", help="Block index in the chain"),
                                "timestamp": st.column_config.TextColumn("Timestamp", help="When the block was created"),
                                "file_hash": st.column_config.TextColumn("File Hash", help="Unique hash of the uploaded file"),
                                "previous_hash": st.column_config.TextColumn("Previous Hash", help="Hash of the previous block"),
                                "block_hash": st.column_config.TextColumn("Block Hash", help="Hash of this block")
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.info("ℹ️ No blocks in the blockchain yet.")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                try:
                    error_detail = response.json().get("detail", response.text)
                except requests.exceptions.JSONDecodeError:
                    error_detail = response.text
                st.error(f"❌ Error fetching blockchain data: {error_detail}")
    
    except RequestException as e:
        st.error(f"❌ Failed to connect to the server ({BACKEND_URL}). Please ensure it's running. Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}") 
