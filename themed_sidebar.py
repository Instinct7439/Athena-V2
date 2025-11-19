import streamlit as st
from theme_manager import ThemeManager
from themed_style import get_themed_style

def render_themed_sidebar():
    """Render themed sidebar with toggle"""

    ThemeManager.initialize()
    theme = ThemeManager.get_current_theme()

    accent = theme["accent"]
    secondary = theme["secondary_text"]
    logo = theme["logo"]

    # Apply global themed CSS
    st.markdown(get_themed_style(), unsafe_allow_html=True)

    # SIDEBAR CONTENT
    with st.sidebar:

        # LOGO + TITLE
        try:
            st.markdown(
                """
                <div style="
                    <img src="assets\" width="110">
                    text-align: center;
                    margin-top: 0.5rem;
                    margin-bottom: 0.5rem;
                ">
                <img src="assets/logo.png" width="110">
                """,
                unsafe_allow_html=True
            )

            st.image(logo, width=110)

            st.markdown(
                f"""
                <h2 style="
                    color: {accent};
                    margin-top: 0.5rem;
                    margin-bottom: 0;
                    text-align: center;
                    font-weight: 800;
                ">
                    Athena
                </h2>

                <p style="
                    color: {secondary};
                    margin-top: 0;
                    font-size: 0.85rem;
                    text-align: center;
                ">
                    AI Research Assistant
                </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:
            st.markdown(
                f"""
                <div style='text-align: center; margin-bottom: 0.75rem;'>
                    <div style='font-size: 3rem; margin-bottom: 0.25rem;'>🦉</div>
                    <h1 style='font-size: 1.4rem; margin: 0; color: {accent}; font-weight: 700;'>
                        Athena
                    </h1>
                    <p style='text-align: center; color: {secondary}; font-size: 0.8rem; margin: 0.15rem 0 0 0;'>
                        AI Research Assistant
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"<hr style='margin: 0.75rem 0; border: none; border-top: 1px solid {theme['border']};'>",
            unsafe_allow_html=True
        )

        # ---- THEME TOGGLE BUTTON ----
        theme_icon = "🌙" if ThemeManager.is_dark() else "☀️"
        theme_text = "Light Mode" if ThemeManager.is_dark() else "Dark Mode"

        if st.button(f"{theme_icon} {theme_text}", key="theme_toggle", use_container_width=True):
            ThemeManager.toggle_theme()
            st.rerun()

        st.markdown(
            f"<hr style='margin: 0.75rem 0; border: none; border-top: 1px solid {theme['border']};'>",
            unsafe_allow_html=True
        )

        # ---- ABOUT SECTION ----
        st.markdown("<h2>ℹ️ About</h2>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='line-height: 1.5; font-size: 0.85rem; color:{secondary};'>
            Athena helps you:
            </div>
            <ul style='margin-top: 0.5rem; margin-bottom: 0.75rem; line-height: 1.5; font-size: 0.85rem; color:{secondary};'>
                <li>Analyze research papers</li>
                <li>Extract insights</li>
                <li>Build knowledge graphs</li>
                <li>Compare documents</li>
                <li>Ask contextual questions</li>
            </ul>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<hr style='margin: 1rem 0; border: none; border-top: 1px solid {theme['border']};'>",
            unsafe_allow_html=True
        )

        # ---- SYSTEM STATUS ----
        st.markdown("<h2>🔧 System Status</h2>", unsafe_allow_html=True)

        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)

            if response.status_code == 200:
                st.success("✓ Ollama: Running")
                models = response.json().get("models", [])
                if any("llama3" in m.get("name", "") for m in models):
                    st.success("✓ llama3: Available")
                else:
                    st.warning("⚠️ llama3: Not found")
            else:
                st.error("✗ Ollama: Error")
        except:
            st.error("✗ Ollama: Not running")
            st.caption("Start with: `ollama serve`")

        # ---- SESSION STATS ----
        if st.session_state.get("pdf_uploaded", False):
            st.markdown(
                f"<hr style='margin: 1rem 0; border: none; border-top: 1px solid {theme['border']};'>",
                unsafe_allow_html=True
            )
            st.markdown("<h2>📊 Session Stats</h2>", unsafe_allow_html=True)

            stats = f"""
            <div style='background: {theme["card_bg"]}; padding: 0.75rem; border-radius: 6px; border: 1px solid {theme["border"]};'>
                <p style='margin: 0.25rem 0; font-size: 0.8rem;'><strong>Document:</strong><br/>{st.session_state.get("pdf_filename", "N/A")}</p>
                <p style='margin: 0.25rem 0; font-size: 0.8rem;'><strong>Text length:</strong> {len(st.session_state.get("pdf_text", "")):,} chars</p>
            """

            if "qa_chain" in st.session_state:
                stats += "<p><strong>Q&A Index:</strong> ✓ Ready</p>"

            if "semantic_index" in st.session_state:
                stats += "<p><strong>Semantic Index:</strong> ✓ Ready</p>"

            stats += "</div>"

            st.markdown(stats, unsafe_allow_html=True)

        # ---- RESET BUTTON ----
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reset Session", key="sidebar_reset_session", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != "theme":
                    del st.session_state[key]
            st.success("✓ Session reset! Refreshing…")
            st.rerun()
