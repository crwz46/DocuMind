import streamlit as st

from documind.auth import register_user, login_user

st.set_page_config(
    page_title="DocuMind",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "user" in st.session_state:
    st.switch_page("pages/01_Home.py")

st.markdown("""
<style>
    .auth-container { max-width: 400px; margin: 4rem auto; text-align: center; }
    .auth-title { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .auth-subtitle { color: #888; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
st.markdown("<div class='auth-title'>🧠 DocuMind</div>", unsafe_allow_html=True)
st.markdown("<div class='auth-subtitle'>Document Intelligence Platform</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        if submitted:
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                try:
                    result = login_user(username, password)
                    if result:
                        st.session_state["user"] = result["user"]
                        st.session_state["token"] = result["access_token"]
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"Login failed: {e}")

with tab2:
    with st.form("register_form"):
        reg_username = st.text_input("Choose a username")
        reg_email = st.text_input("Email")
        reg_password = st.text_input("Password", type="password")
        reg_confirm = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Register", type="primary", use_container_width=True)
        if submitted:
            if not reg_username or not reg_email or not reg_password:
                st.error("Please fill in all fields")
            elif reg_password != reg_confirm:
                st.error("Passwords do not match")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                try:
                    user = register_user(reg_username, reg_email, reg_password)
                    st.success("Registration successful! Please login.")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Registration failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)
