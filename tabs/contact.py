import streamlit as st
from PIL import Image
from tabs.home import set_bg

def app():
        set_bg("tabs/images/background.jpg")
        # header and image
        st.title('Let\'s Connect!')
        image = Image.open("tabs/images/contact.png")
        col1, col2, col3, col4 = st.columns(4)
        with col2:
                st.image(image, width=400)
        
        # description
        st.markdown(""":orange[Please fill in the form below for any enquiries or feedback.]""")

        # contact form
        contact_form = """
        <form action="https://formsubmit.co/yourownemail@email.com" method="POST" enctype="multipart/form-data">
                <input type="text" name="Name" placeholder="John Doe" required>
                <input type="email" placeholder="johndoe@email.com" name="Email" required>
                <textarea name="Message" placeholder="Hello!"></textarea>
                <input type="file" name="attachment">
                <button type="submit">Send</button>
                <input type="hidden" name="_template" value="table">
                <input type="hidden" name="_subject" value="New submission!">
        </form>        
        """
        
        st.markdown(contact_form, unsafe_allow_html=True)

        def local_css(file_name):
                with open(file_name) as f:
                        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        local_css("tabs/css/aboutme.css")