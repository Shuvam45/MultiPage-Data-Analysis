import streamlit as st

st.set_page_config(
    page_title="Student Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


pages = {
    "Info": [
        st.Page("./pages/About Me.py", title="About Me"),
    ],
    "Resources": [
        st.Page("./pages/Page_1.py", title="Social Media Addiction Analysis"),
        st.Page("./pages/Page_2.py", title="Students Habits Analysis"),
    ],
}

pg = st.navigation(pages)
pg.run()
