import streamlit as st

st.set_page_config(
    page_title="DocuMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header { text-align: center; padding: 2rem 0; }
    .main-header h1 { font-size: 3rem; margin-bottom: 0.5rem; }
    .main-header p { font-size: 1.2rem; color: #888; }
    .feature-card {
        padding: 1.5rem; border-radius: 10px;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #333; margin: 0.5rem 0;
    }
    .feature-card h3 { margin: 0 0 0.5rem 0; color: #00d4ff; }
    .feature-card p { margin: 0; color: #ccc; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.markdown("# 🧠 **DocuMind**")
st.markdown("<p>Document Intelligence — RAG-Powered Q&A Engine</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Upload Documents")
    st.markdown("PDF, DOCX, TXT, MD — multi-page support with smart chunking")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Semantic Search")
    st.markdown("Vector embeddings with ChromaDB for precise context retrieval")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 🤖 LLM-Powered Q&A")
    st.markdown("OpenAI, Ollama, or Demo mode — answers grounded in your documents")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

with st.container():
    st.markdown("### 🚀 Quick Start")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**1.** Upload documents in the **Upload Docs** page")
    with c2:
        st.info("**2.** Ask questions in the **Chat Q&A** page — that's it!")

    st.caption(
        "Configure LLM provider via `.env` file. "
        "Default is demo mode (no API key needed). "
        "Set `LLM_PROVIDER=openai` or `ollama` for real answers."
    )

st.sidebar.markdown("## 🧠 DocuMind")
st.sidebar.markdown("**v2.0.0** — Document Intelligence with RAG + OCR + Export")
st.sidebar.divider()
st.sidebar.markdown("### Navigation")
st.sidebar.page_link("main.py", label="🏠 Home", icon="🏠")
st.sidebar.page_link("pages/01_Upload_Docs.py", label="📄 Upload Docs", icon="📄")
st.sidebar.page_link("pages/02_Chat_QA.py", label="💬 Chat Q&A", icon="💬")
st.sidebar.page_link("pages/05_Summarize.py", label="📝 Summarize", icon="📝")
st.sidebar.page_link("pages/04_Extract_Export.py", label="📊 Extract & Export", icon="📊")
st.sidebar.page_link("pages/03_Knowledge_Base.py", label="📚 Knowledge Base", icon="📚")

st.sidebar.divider()
st.sidebar.markdown("### 🚀 Features")
st.sidebar.markdown("- ✅ Q&A with RAG")
st.sidebar.markdown("- ✅ OCR for scanned PDFs")
st.sidebar.markdown("- ✅ Summarization")
st.sidebar.markdown("- ✅ Structured extraction")
st.sidebar.markdown("- ✅ Export to Excel")
