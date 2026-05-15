import streamlit as st
# Remove direct imports of requests, pandas, datetime, graphviz as they are now in utils/ui_components
from ui_components import render_header, render_sidebar, render_upload_page, render_blockchain_log, render_verify_page

# ---------- CONFIGURATION ---------- #
def configure_page():
    """Configure the page settings and theme."""
    st.set_page_config(
        page_title="SecureVault",
        page_icon="🔒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS styles remain here as they apply globally
    st.markdown("""
        <style>
        /* Light theme defaults (fallbacks) */
        :root {
            --background-color-light: #f8fafc;
            --text-color-light: #0f172a;
            --primary-color-light: #1e40af;
            --card-background-light: #ffffff;
            --border-color-light: #e6edf3;
            --card-padding: 1.5rem;
        }

        /* Compact card variant for tighter UI */
        .card.compact {
            padding: 0.6rem 1rem !important;
            margin-bottom: 0.75rem !important;
            border-radius: 10px !important;
        }

        /* Tighter global card default */
        .card {
            padding: var(--card-padding) !important;
            background-color: var(--card-background-light);
            border: 1px solid var(--border-color-light);
            border-radius: 12px;
        }

        /* File uploader compact style */
        .stFileUploader {
            max-width: 720px;
        }

        /* Improve button appearance and spacing */
        .stButton>button {
            background: linear-gradient(180deg, #2563eb, #1e40af) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 6px rgba(16,24,40,0.2);
            padding: 10px 14px !important;
            border-radius: 8px !important;
        }

        /* Smaller header spacing */
        .stApp header ~ div { padding-top: 8px !important; }

        /* Theme colors */
        :root {
            /* Dark Mode Overrides (applied via media query) */
            --primary-color-dark: #bfdbfe; /* Light blue for dark bg */
            --secondary-color-dark: #fda4af;
            --accent-color-dark: #fcd34d;
            --text-color-dark: #f3f4f6; /* Light gray text for dark bg */
            --background-color-dark: #111827; /* Dark background */
            --card-background-dark: #1f2937;
            --border-color-dark: #374151;
        }
        
        /* Apply Light Mode Colors by Default */
        body {
            background-color: var(--background-color-light);
            color: var(--text-color-light);
        }
        .stApp > header {
            background-color: var(--background-color-light);
        }
        /* Ensure default text color is applied widely */
        div[data-testid="stMarkdownContainer"], div[data-testid="stText"], label[data-testid="stWidgetLabel"], div[data-testid="stExpander"] div[role="button"], .stButton>button, .stFileUploader label {
             color: var(--text-color-light) !important; 
        }
         h1, h2, h3 {
             color: var(--primary-color-light) !important;
             font-weight: 600;
        }
        .card {
            background-color: var(--card-background-light);
            border: 1px solid var(--border-color-light);
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        /* Dark Mode Adjustments */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: var(--background-color-dark);
                color: var(--text-color-dark);
            }
            .stApp > header {
                 background-color: var(--background-color-dark);
            }
            div[data-testid="stMarkdownContainer"], div[data-testid="stText"], label[data-testid="stWidgetLabel"], div[data-testid="stExpander"] div[role="button"], .stButton>button, .stFileUploader label {
                 color: var(--text-color-dark) !important;
            }
             h1, h2, h3 {
                 color: var(--primary-color-dark) !important;
            }
            .card {
                 background-color: var(--card-background-dark);
                 border: 1px solid var(--border-color-dark);
                 box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.2); 
            }
            /* Adjust graph node color for dark mode */
             .stGraphVizChart > svg g.node > polygon { fill: #374151; stroke: #6b7280; }
             .stGraphVizChart > svg g.node > text { fill: var(--text-color-dark); }
             .stGraphVizChart > svg g.edge > path { stroke: #6b7280; }
             .stGraphVizChart > svg g.edge > polygon { fill: #6b7280; stroke: #6b7280; }
             .stGraphVizChart > svg g.edge > text { fill: var(--text-color-dark); }
        }
        
        /* Responsive Design Adjustments */
        @media (max-width: 768px) {
            .stButton > button { width: 100%; }
            .card { padding: 1rem 1.5rem; }
        }
        </style>
    """, unsafe_allow_html=True)

# ---------- MAIN APP ---------- #
def main():
    """Main application entry point."""
    configure_page()
    
    render_header()
    
    selected_page = render_sidebar()
    
    with st.container():
        if selected_page == "📤 Upload Document":
            render_upload_page()
        elif selected_page == "📋 Blockchain Log":
            render_blockchain_log()
        elif selected_page == "✅ Verify File":
            render_verify_page()
        # Add else or default case if needed

if __name__ == "__main__":
    main()
