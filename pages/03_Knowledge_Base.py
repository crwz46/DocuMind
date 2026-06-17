import streamlit as st

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Knowledge Base", page_icon="📚", layout="wide")
st.markdown("# 📚 Knowledge Base")

pipeline = QAPipeline()

stats = pipeline.stats()
st.metric("Total Chunks Indexed", stats["total_chunks"])
st.metric("Documents", stats["documents"])

col1, col2 = st.columns([3, 1])
with col1:
    docs = pipeline.list_documents()
    if docs:
        st.markdown("### 📋 Document List")
        for doc in docs:
            with st.container(border=True):
                cc1, cc2, cc3 = st.columns([4, 1, 1])
                with cc1:
                    st.markdown(f"**{doc['source']}**")
                    st.caption(f"Type: {doc['type']} | Chunks: {doc['chunks']}")
                with cc3:
                    if st.button("🗑️ Delete", key=f"del_{doc['source']}"):
                        if pipeline.delete_document(doc["source"]):
                            st.success(f"Deleted: {doc['source']}")
                            st.rerun()
                        else:
                            st.error("Delete failed")
    else:
        st.info("📭 Knowledge base is empty. Upload documents to get started.")

with col2:
    st.markdown("### ⚙️ Actions")
    if st.button("🗑️ Clear All", type="primary", use_container_width=True):
        pipeline.vector_store.clear()
        st.success("Knowledge base cleared!")
        st.rerun()
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.divider()
st.markdown("### 🧠 System Info")
ci1, ci2, ci3 = st.columns(3)
ci1.info(f"**Embedding Model**\n\n`{stats['embedding_model']}`")
ci2.info(f"**LLM Provider**\n\n`{stats['llm_provider']}`")
ci3.info(f"**Vector Store**\n\nChromaDB (persistent)")
