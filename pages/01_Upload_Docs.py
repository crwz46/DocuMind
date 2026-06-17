import streamlit as st
from pathlib import Path

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Upload", page_icon="📄", layout="wide")
st.markdown("# 📄 Upload Documents")

pipeline = QAPipeline()

uploaded_files = st.file_uploader(
    "Choose documents (PDF, DOCX, TXT, MD)",
    type=["pdf", "docx", "txt", "md"],
    accept_multiple_files=True,
)

if uploaded_files:
    results = []
    for f in uploaded_files:
        data = f.read()
        result = pipeline.ingest_bytes(f.name, data)
        results.append((f.name, result))
        st.session_state.setdefault("uploaded", []).append(f.name)

    for name, result in results:
        if result["status"] == "success":
            st.success(f"✅ **{name}** — {result['message']}")
        else:
            st.error(f"❌ **{name}** — {result['message']}")

    if results:
        total = sum(r["chunks"] for _, r in results if r["status"] == "success")
        st.info(f"📊 **Total: {total} chunks** indexed into the knowledge base")

st.divider()
st.markdown("### 📋 Recently Uploaded")
if "uploaded" in st.session_state and st.session_state.uploaded:
    for doc in set(st.session_state.uploaded):
        st.write(f"- {doc}")
else:
    st.caption("No documents uploaded yet in this session.")

st.divider()
st.markdown("### ⚙️ Supported Formats")
cols = st.columns(4)
for i, (ext, desc) in enumerate([
    ("📕 PDF", "Multi-page with page numbers"),
    ("📘 DOCX", "Microsoft Word documents"),
    ("📄 TXT", "Plain text files"),
    ("📝 MD", "Markdown files"),
]):
    cols[i].info(f"**{ext}**\n\n{desc}")
