import os
import tempfile

import streamlit as st

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Summarize", page_icon="📝", layout="wide")
st.markdown("# 📝 Summarize Documents")

pipeline = QAPipeline()

tab1, tab2 = st.tabs(["📄 From Knowledge Base", "🆕 Upload & Summarize"])

with tab1:
    docs = pipeline.list_documents()
    if docs:
        doc_names = [d["source"] for d in docs]
        selected = st.selectbox("Select document from knowledge base", doc_names, key="kb_summarize")
        style = st.selectbox(
            "Summary style",
            ["bullet", "short", "detailed", "executive"],
            format_func=lambda x: {"bullet": "🔹 Bullet Points", "short": "📏 Short (2-3 sentences)", "detailed": "📖 Detailed", "executive": "📊 Executive Summary"}[x],
        )
        if st.button("Summarize", type="primary", use_container_width=True):
            with st.spinner("Generating summary..."):
                try:
                    result = pipeline.summarize(source=selected, style=style)
                    st.markdown("### Summary")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("No documents in knowledge base. Upload documents first.")

with tab2:
    uploaded = st.file_uploader(
        "Upload a document to summarize",
        type=["pdf", "docx", "txt", "md"],
        key="summarize_upload",
    )
    style2 = st.selectbox(
        "Summary style",
        ["bullet", "short", "detailed", "executive"],
        key="summarize_style2",
        format_func=lambda x: {"bullet": "🔹 Bullet Points", "short": "📏 Short (2-3 sentences)", "detailed": "📖 Detailed", "executive": "📊 Executive Summary"}[x],
    )
    if uploaded and st.button("Summarize Uploaded", type="primary", use_container_width=True):
        with st.spinner("Processing and summarizing..."):
            try:
                data = uploaded.read()
                result = pipeline.ingest_bytes(uploaded.name, data)
                if result["status"] == "success":
                    docs2 = pipeline.list_documents()
                    if docs2:
                        summary = pipeline.summarize(source=docs2[-1]["source"], style=style2)
                        st.markdown("### Summary")
                        st.markdown(summary)
                else:
                    st.error(result["message"])
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.markdown("### 💡 Summary Styles")
cols = st.columns(4)
styles_info = [
    ("🔹 Bullet Points", "Quick overview with key points"),
    ("📏 Short", "Concise 2-3 sentence summary"),
    ("📖 Detailed", "Comprehensive coverage"),
    ("📊 Executive", "Business-ready summary"),
]
for col, (name, desc) in zip(cols, styles_info):
    col.info(f"**{name}**\n\n{desc}")
