# import libraries
import streamlit as st
from multiapp import MultiApp
from PIL import Image
# Title
st.set_page_config(page_title="Tradebotix", page_icon=":chart_with_upwards_trend:", layout="centered")
image = Image.open('./tabs/images/logo.png')

# Title
st.markdown("<h1 style='text-align: center;'>Tradebotix</h1>",
            unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    st.image(image, width=100)

st.markdown("<h5 style='text-align: center; font-style: italic;'>A web app for trading and investing</h5>",
            unsafe_allow_html=True)

# instantiate the MultiApp class
app = MultiApp()

# The main app
app.run()
