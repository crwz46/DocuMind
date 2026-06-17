import streamlit as st

from documind.database import ConversationDB

st.set_page_config(page_title="DocuMind — Home", page_icon="🧠", layout="wide")

if "user" not in st.session_state:
    st.switch_page("main.py")

user = st.session_state["user"]

st.sidebar.markdown(f"### 👤 {user['username']}")
st.sidebar.markdown(f"Role: **{user['role']}**")
st.sidebar.divider()

if st.sidebar.button("Logout", use_container_width=True):
    for key in ["user", "token", "current_conv"]:
        st.session_state.pop(key, None)
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("## 🧠 DocuMind")
st.sidebar.markdown("**v3.0.0** — Multi-User RAG Platform")
st.sidebar.divider()
st.sidebar.markdown("### Navigation")
st.sidebar.page_link("pages/01_Home.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/02_Upload_Docs.py", label="Upload Docs", icon="📄")
st.sidebar.page_link("pages/03_Chat_QA.py", label="Chat Q&A", icon="💬")
st.sidebar.page_link("pages/06_Summarize.py", label="Summarize", icon="📝")
st.sidebar.page_link("pages/05_Extract_Export.py", label="Extract & Export", icon="📊")
st.sidebar.page_link("pages/04_Knowledge_Base.py", label="Knowledge Base", icon="📚")

conv_db = ConversationDB()
convs = conv_db.list_by_user(user["id"])
if convs:
    st.sidebar.divider()
    st.sidebar.markdown("### Recent Chats")
    for c in convs[:5]:
        if st.sidebar.button(f"💬 {c['title'][:30]}", key=f"conv_{c['id']}", use_container_width=True):
            st.session_state["current_conv"] = c["id"]
            st.switch_page("pages/03_Chat_QA.py")

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
    .user-badge {
        display: inline-block; background: #00d4ff22; padding: 0.25rem 1rem;
        border-radius: 20px; border: 1px solid #00d4ff44; color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div style='text-align: right'><span class='user-badge'>👤 {user['username']}</span></div>", unsafe_allow_html=True)

st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.markdown("# 🧠 **DocuMind**")
st.markdown("<p>Multi-User Document Intelligence — RAG + OCR + Extraction + Export</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Upload Docs")
    st.markdown("PDF, DOCX, TXT, MD with optional OCR for scans")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 💬 Chat Q&A")
    st.markdown("RAG-powered answers with source citations")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Extract & Export")
    st.markdown("Structured JSON extraction → Excel export")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Summarize")
    st.markdown("4 summary styles: short, bullet, detailed, executive")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.markdown("### 💡 Quick Start")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("**1.** Upload documents in **Upload Docs**")
with c2:
    st.info("**2.** Ask questions in **Chat Q&A** with citations")
with c3:
    st.info("**3.** Extract data & **Export to Excel**")
