import streamlit as st
from theme_manager import ThemeManager

def render_sidebar():
    """Render themed sidebar with Athena title and all features"""
    ThemeManager.initialize()
    theme = ThemeManager.get_current_theme()

    bg = theme['background']
    text = theme['primary_text']
    secondary = theme['secondary_text']
    border = theme['border']
    accent = theme['accent']
    accent2 = theme.get('accent_secondary', accent)
    card = theme['card_bg']

    css = f"""
    <style>
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: {bg} !important;
        border-right: 1px solid {border} !important;
    }}

    section[data-testid="stSidebar"] h1 {{
        color: {accent} !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        margin: 0 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }}

    section[data-testid="stSidebar"] h2 {{
        color: {accent} !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li {{
        color: {text} !important;
        font-size: 0.85rem !important;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: {accent} !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        width: 100%;
        font-weight: 600;
        transition: all 0.3s ease;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: {accent2} !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}

    section[data-testid="stSidebar"] hr {{
        border-top: 1px solid {border} !important;
        margin: 1rem 0 !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] > div {{
        background: {card} !important;
        border-radius: 8px;
        border: 1px solid {border};
        padding: 0.75rem;
    }}

    .status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }}

    .status-running {{
        background-color: #06D6A0;
        box-shadow: 0 0 8px #06D6A0;
    }}

    .status-error {{
        background-color: #EF476F;
        box-shadow: 0 0 8px #EF476F;
    }}

    .status-warning {{
        background-color: #FFB627;
        box-shadow: 0 0 8px #FFB627;
    }}

    .feature-item {{
        display: flex;
        align-items: center;
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background: {card};
        border-radius: 6px;
        border: 1px solid {border};
        transition: all 0.3s ease;
    }}

    .feature-item:hover {{
        background: {accent}22;
        border-color: {accent};
        transform: translateX(3px);
    }}

    .feature-icon {{
        font-size: 1.2rem;
        margin-right: 0.75rem;
    }}

    .feature-name {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {text};
    }}

    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

    with st.sidebar:
        # ATHENA TITLE (NO LOGO)
        st.markdown(f"""
            <div style='text-align: center; margin: 1rem 0 1.5rem 0;'>
                <h1 style='color: {accent}; margin: 0; line-height: 1; font-size: 2.2rem; font-family: "Georgia", "Times New Roman", serif; font-weight: 800;'>
                    Athena
                </h1>
                <p style='color: {secondary}; font-size: 0.75rem; margin: 0.25rem 0 0 0; font-style: italic;'>
                    AI Research Assistant
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # SYSTEM STATUS
        st.markdown("<h2>System Status</h2>", unsafe_allow_html=True)
        
        ollama_status = check_ollama_status()
        
        if ollama_status['running']:
            st.markdown(f"""
                <div style='background: {card}; padding: 0.75rem; border-radius: 8px; border: 1px solid {border}; margin-bottom: 0.5rem;'>
                    <p style='margin: 0; font-size: 0.85rem;'>
                        <span class='status-indicator status-running'></span>
                        <strong>Ollama:</strong> Running
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if ollama_status['models']:
                model_status = "status-running" if ollama_status['llama3_available'] else "status-warning"
                model_text = "Available" if ollama_status['llama3_available'] else "Not found"
                
                st.markdown(f"""
                    <div style='background: {card}; padding: 0.75rem; border-radius: 8px; border: 1px solid {border}; margin-bottom: 0.5rem;'>
                        <p style='margin: 0; font-size: 0.85rem;'>
                            <span class='status-indicator {model_status}'></span>
                            <strong>Model:</strong> llama3 - {model_text}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Show all available models
                if len(ollama_status['models']) > 0:
                    with st.expander("Available Models", expanded=False):
                        for model in ollama_status['models']:
                            st.caption(f"• {model}")
        else:
            st.markdown(f"""
                <div style='background: {card}; padding: 0.75rem; border-radius: 8px; border: 1px solid {border}; margin-bottom: 0.5rem;'>
                    <p style='margin: 0; font-size: 0.85rem;'>
                        <span class='status-indicator status-error'></span>
                        <strong>Ollama:</strong> Not running
                    </p>
                    <p style='margin: 0.5rem 0 0 0; font-size: 0.75rem; color: {secondary};'>
                        Start with: <code>ollama serve</code>
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # AVAILABLE FEATURES SECTION
        st.markdown("<h2>Features</h2>", unsafe_allow_html=True)
        
        # Core Features (always available)
        features = [
            "Research Summary",
            "Q&A Engine",
            "Semantic Search",
            "Chat Interface",
            "Agent Tracking",
        ]
        
        # Check optional features
        optional_features = get_available_features()
        
        # Display core features with same styling as optional
        for name in features:
            st.markdown(f"""
                <div style='background: {card}; padding: 0.5rem 0.75rem; margin: 0.25rem 0; border-radius: 6px; border: 1px solid {border};'>
                    <span class='status-indicator status-running'></span>
                    <span style='font-size: 0.85rem; color: {text};'>{name}</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Add optional features with status indicators
        st.markdown(f"<p style='color: {secondary}; font-size: 0.75rem; margin-top: 1rem; margin-bottom: 0.5rem;'>Optional Features:</p>", unsafe_allow_html=True)
        
        for feature, available in optional_features.items():
            status_class = "status-running" if available else "status-error"
            
            st.markdown(f"""
                <div style='background: {card}; padding: 0.5rem 0.75rem; margin: 0.25rem 0; border-radius: 6px; border: 1px solid {border};'>
                    <span class='status-indicator {status_class}'></span>
                    <span style='font-size: 0.85rem; color: {text};'>{feature}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # THEME TOGGLE
        theme_text = "Light Mode" if theme['name'] == "dark" else "Dark Mode"
        
        if st.button(theme_text, use_container_width=True, key="theme_toggle"):
            ThemeManager.toggle_theme()
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # SESSION STATS (if document loaded)
        if st.session_state.get("pdf_uploaded", False):
            st.markdown("<h2>Session Stats</h2>", unsafe_allow_html=True)
            
            filename = st.session_state.get("pdf_filename", "N/A")
            text_len = len(st.session_state.get("pdf_text", ""))
            
            st.markdown(f"""
                <div style='background: {card}; padding: 0.75rem; border-radius: 8px; border: 1px solid {border};'>
                    <p style='margin: 0.25rem 0; font-size: 0.8rem;'>
                        <strong>Document:</strong><br/>
                        <span style='color: {secondary};'>{filename}</span>
                    </p>
                    <p style='margin: 0.5rem 0 0.25rem 0; font-size: 0.8rem;'>
                        <strong>Text length:</strong> {text_len:,} chars
                    </p>
            """, unsafe_allow_html=True)
            
            # Show which indexes are ready
            indexes = []
            if "qa_chain" in st.session_state:
                indexes.append("Q&A")
            if "semantic_index" in st.session_state:
                indexes.append("Semantic")
            
            if indexes:
                st.markdown(f"""
                    <p style='margin: 0.5rem 0 0.25rem 0; font-size: 0.8rem;'>
                        <strong>Ready:</strong> {', '.join(indexes)}
                    </p>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)

        # QUICK ACTIONS
        st.markdown("<h2>Quick Actions</h2>", unsafe_allow_html=True)
        
        if st.button("Reset Session", use_container_width=True, key="reset_session"):
            for key in list(st.session_state.keys()):
                if key != "theme":
                    del st.session_state[key]
            st.success("Session reset!")
            st.rerun()


def check_ollama_status():
    """Check if Ollama is running and which models are available"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            llama3_available = any("llama3" in name for name in model_names)
            
            return {
                'running': True,
                'models': model_names,
                'llama3_available': llama3_available
            }
        else:
            return {'running': False, 'models': [], 'llama3_available': False}
    except:
        return {'running': False, 'models': [], 'llama3_available': False}


def get_available_features():
    """Check which optional features are available"""
    features = {}
    
    try:
        from document_comparison import DocumentComparison
        features['Document Comparison'] = True
    except ImportError:
        features['Document Comparison'] = False
    
    try:
        from voice_interface import render_voice_tab
        features['Voice Assistant'] = True
    except ImportError:
        features['Voice Assistant'] = False
    
    try:
        from kg_visualizer import render_knowledge_graph_tab
        features['Knowledge Graph'] = True
    except ImportError:
        features['Knowledge Graph'] = False
    
    try:
        from advanced_rag import AdvancedRAG
        features['Advanced RAG'] = True
    except ImportError:
        features['Advanced RAG'] = False
    
    return features