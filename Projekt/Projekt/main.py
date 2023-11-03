import streamlit as st
import log_in
import pages


if "current_user" not in st.session_state:
    st.session_state["current_user"] = None


st.set_page_config(initial_sidebar_state="collapsed", page_title="Aktien-App", page_icon="📈")
st.title("Aktien-App")


with st.sidebar:
    st.subheader("Menu")
    if st.session_state["current_user"] == None:
        st.session_state["current_user"] = log_in.login()
        log_in.signup()
        if st.session_state["current_user"] is not None:
            st.experimental_rerun()
    else:
        st.write("Hallo", st.session_state["current_user"])
        if st.button("LogOut"):
            st.session_state["current_user"] = None


if st.session_state["current_user"] == None:
    tab_main, tab_search = st.tabs(["Menu", "Search"])

    with tab_main:
        pages.main_page()

    with tab_search:
        pages.tab_search()

else:
    tab_main, tab_search, tab_port = st.tabs(["Menu", "Search", "Portfolio"])

    with tab_main:
        pages.main_page()

    with tab_search:
        pages.tab_search()

    with tab_port:
        pages.tab_port()