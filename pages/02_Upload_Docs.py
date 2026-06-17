import streamlit as st

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Upload", page_icon="📄", layout="wide")

if "user" not in st.session_state:
    st.switch_page("main.py")

user = st.session_state["user"]
pipeline = QAPipeline(user_id=user["id"])

st.markdown("# 📄 Upload Documents")

col1, col2 = st.columns([3, 1])
with col1:
    uploaded_files = st.file_uploader(
        "Choose documents (PDF, DOCX, TXT, MD)",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )
with col2:
    force_ocr = st.checkbox("🔍 Force OCR", value=False, help="Enable OCR for scanned PDFs (auto-detected for textless PDFs)")

if force_ocr:
    st.info("🔍 OCR mode enabled — all PDFs will be processed with optical character recognition")

if uploaded_files:
    results = []
    for f in uploaded_files:
        data = f.read()
        result = pipeline.ingest_bytes(f.name, data, force_ocr=force_ocr)
        results.append((f.name, result))
        st.session_state.setdefault("uploaded", []).append(f.name)

    for name, result in results:
        if result["status"] == "success":
            st.success(f"**{name}** — {result['message']}")
        else:
            st.error(f"**{name}** — {result['message']}")

    if results:
        total = sum(r["chunks"] for _, r in results if r["status"] == "success")
        st.info(f"**Total: {total} chunks** indexed into the knowledge base")

st.divider()
st.markdown("### Recently Uploaded")
if "uploaded" in st.session_state and st.session_state.uploaded:
    for doc in set(st.session_state.uploaded):
        st.write(f"- {doc}")
else:
    st.caption("No documents uploaded yet in this session.")
