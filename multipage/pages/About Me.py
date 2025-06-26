import streamlit as st
import webbrowser
import re
import requests

# External profile links
linkedin = "https://www.linkedin.com/in/shuvam-chattopadhyay-b5a07733a/"
github = "https://github.com/Shuvam45"

# Replace with your actual webhook URL (e.g., from FormSubmit or other services)
WEBHOOK_URL = "https://hook.pabbly.com/api/webhook/6857bb7f40b0ca2e49819248/6857bbad5e434afb5db87cde"


def is_valid_email(email):
    """Basic regex pattern for email validation"""
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


# 📩 Contact Form Dialog
@st.dialog("Contact Me")
def show_contact_form():
    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not WEBHOOK_URL:
                st.error("Email service is not set up. Please try again later.", icon="📧")
                st.stop()

            if not name:
                st.error("Please provide your name.", icon="🧑")
                st.stop()

            if not email:
                st.error("Please provide your email address.", icon="📨")
                st.stop()

            if not is_valid_email(email):
                st.error("Please provide a valid email address.", icon="📧")
                st.stop()

            if not message:
                st.error("Please provide a message.", icon="💬")
                st.stop()

            # Send form data to the webhook
            data = {"email": email, "name": name, "message": message}
            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 200:
                st.success("Your message has been sent successfully! 🎉", icon="🚀")
            else:
                st.error("There was an error sending your message.", icon="😨")


# 🔹 Layout
col1, col2 = st.columns(2, gap="small")

with col1:
    st.image(r"C:\Users\HP\Desktop\Coding\Python\StreamLit\Project\download.jpg", width=230)

    st.title("Education:")
    st.write("South Point High School — Passed out in 2024")
    st.write("VIT AP UNIVERSITY (2024-2028) — BTech in Computer Science")

    st.title("Skills:")
    st.write("Programming Languages: C, Java, Python")
    st.write("Frameworks: NumPy, Pandas, Matplotlib, Seaborn, Streamlit, Plotly")

    st.title("My Socials:")
    if st.button("Open LinkedIn Profile"):
        webbrowser.open_new_tab(linkedin)
    if st.button("Open GitHub Profile"):
        webbrowser.open_new_tab(github)

with col2:
    st.title("Shuvam Chattopadhyay")
    st.write("""
    Hi, I'm Shuvam Chattopadhyay, a passionate Computer Science student with a keen interest in coding, web development, and AI integration.
    I enjoy building interactive projects using Python and Streamlit, and I'm always eager to explore new technologies.
    
    Currently, I'm learning data analytics tools and working on projects. In my free time, I love cricket, tech tinkering, and sharing what I learn with others.
    """)

    if st.button("Contact Me"):
        show_contact_form()
