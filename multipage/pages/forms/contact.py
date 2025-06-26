import streamlit as st

with st.form("contact_form"):
    fname= st.text_input("First Name")
    lname=st.text_input("Last Name")
    email=st.text_input("Email Adress")
    message=st.text_area("Your Message")
    submit_button= st.form_submit_button("Submit")

    if submit_button:
        st.success("Response Submitted")
