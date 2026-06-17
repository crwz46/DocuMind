import streamlit as st

from documind.qa_pipeline import QAPipeline
from documind.database import ConversationDB

st.set_page_config(page_title="DocuMind — Chat", page_icon="💬", layout="wide")

if "user" not in st.session_state:
    st.switch_page("main.py")

user = st.session_state["user"]
pipeline = QAPipeline(user_id=user["id"])
conv_db = ConversationDB()

st.markdown("# 💬 Chat Q&A")

conv_sidebar = st.sidebar.container()
with conv_sidebar:
    st.markdown("### Conversations")
    if st.button("+ New Chat", use_container_width=True, type="primary"):
        conv = conv_db.create(user["id"])
        st.session_state["current_conv"] = conv["id"]
        st.rerun()

    convs = conv_db.list_by_user(user["id"])
    if convs:
        for c in convs:
            col1, col2 = st.columns([4, 1])
            with col1:
                active = st.session_state.get("current_conv") == c["id"]
                if st.button(
                    f"{'💬' if active else '🔹'} {c['title'][:35]}",
                    key=f"conv_{c['id']}",
                    use_container_width=True,
                    type="secondary" if not active else "primary",
                ):
                    st.session_state["current_conv"] = c["id"]
                    st.rerun()
            with col2:
                if st.button("🗑", key=f"del_{c['id']}"):
                    conv_db.delete(c["id"])
                    if st.session_state.get("current_conv") == c["id"]:
                        st.session_state.pop("current_conv", None)
                    st.rerun()

current_conv_id = st.session_state.get("current_conv")

messages_placeholder = st.container()

if current_conv_id:
    messages = conv_db.get_messages(current_conv_id)
    with messages_placeholder:
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and msg.get("sources"):
                    with st.expander("Sources", expanded=False):
                        for src in msg["sources"]:
                            page_info = f", Page {src['page']}" if src.get("page") else ""
                            st.markdown(f"**{src['source']}**{page_info}")
                            st.caption(src["content"][:200] + ("..." if len(src["content"]) > 200 else ""))
else:
    with messages_placeholder:
        st.info("Start a new conversation or select one from the sidebar.")

if question := st.chat_input("Ask a question about your documents..."):
    if not current_conv_id:
        conv = conv_db.create(user["id"], title=question[:50])
        current_conv_id = conv["id"]
        st.session_state["current_conv"] = current_conv_id

    conv_db.add_message(current_conv_id, "user", question)
    with messages_placeholder:
        with st.chat_message("user"):
            st.markdown(question)

    with st.spinner("Searching documents and generating answer..."):
        result = pipeline.query(question)

    answer = result["answer"]
    sources = result.get("sources", [])

    conv_db.add_message(current_conv_id, "assistant", answer, sources=sources)

    if len(conv_db.get_messages(current_conv_id)) <= 2:
        title = question[:50] + ("..." if len(question) > 50 else "")
        conv_db.update_title(current_conv_id, title)

    with messages_placeholder:
        with st.chat_message("assistant"):
            st.markdown(answer)
            if sources:
                with st.expander(f"Sources ({len(sources)})", expanded=True):
                    for src in sources:
                        page_info = f", Page {src['page']}" if src.get("page") else ""
                        st.markdown(f"**{src['source']}**{page_info}")
                        st.caption(src["content"][:200] + ("..." if len(src["content"]) > 200 else ""))

    st.rerun()
