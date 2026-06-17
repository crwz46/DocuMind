import streamlit as st

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Chat", page_icon="💬", layout="wide")
st.markdown("# 💬 Chat with Your Documents")

pipeline = QAPipeline()

stats = pipeline.stats()
st.caption(f"📚 Knowledge Base: **{stats['documents']}** documents | **{stats['total_chunks']}** chunks | 🤖 LLM: **{stats['llm_provider']}**")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Upload documents first, then ask me anything about them."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            result = pipeline.query(question, top_k=5)

        if result["sources"]:
            with st.expander(f"📎 Retrieved from {len(result['sources'])} source(s)"):
                for i, src in enumerate(result["sources"]):
                    st.markdown(f"**[{i+1}]** `{src['source']}`" + (f" (Page {src['page']})" if src.get("page") else ""))
                    st.caption(src["content"][:200] + "...")
                    st.metric("Distance", f"{src['distance']:.4f}")
        else:
            st.info("No relevant documents found. Upload documents first.")

        st.markdown(result["answer"])
        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

st.sidebar.markdown("### 💡 Tips")
st.sidebar.info(
    "**Good questions:**\n"
    "- What is the main topic of this document?\n"
    "- Summarize the key findings\n"
    "- What are the conclusions?\n\n"
    "Be specific for best results!"
)
