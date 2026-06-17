import streamlit as st
from pathlib import Path

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Knowledge Base", page_icon="📚", layout="wide")

if "user" not in st.session_state:
    st.switch_page("main.py")

user = st.session_state["user"]
pipeline = QAPipeline(user_id=user["id"])

st.markdown("# 📚 Knowledge Base")

docs = pipeline.list_documents()
if docs:
    st.markdown(f"### {len(docs)} Document(s) Indexed")
    for doc in docs:
        with st.container():
            cols = st.columns([3, 1, 1, 1])
            with cols[0]:
                st.markdown(f"**{Path(doc['source']).name}**")
                st.caption(f"`{doc['source']}`")
            with cols[1]:
                st.markdown(f"Chunks: **{doc['chunks']}**")
            with cols[2]:
                st.markdown(f"Type: `{doc['type']}`")
            with cols[3]:
                if st.button("Delete", key=f"del_{doc['source']}"):
                    pipeline.delete_document(doc["source"])
                    st.rerun()
        st.divider()
else:
    st.info("No documents in your knowledge base. Upload documents first.")

st.divider()
if st.button("Clear All Documents", type="secondary", use_container_width=True):
    for doc in docs:
        pipeline.delete_document(doc["source"])
    st.rerun()
