import streamlit as st
from PIL import Image
import base64
import io
import hashlib



def user_profile(username, password, user_image):
    st.markdown(f""" <div style="background-color: orange; padding: 10px; font-size: 40px; 
                color: black; border-radius: 5px;">User Profile</div> """, unsafe_allow_html=True)
  
    resized_image = user_image.resize((200, 200))

    with io.BytesIO() as buffer:
        resized_image.save(buffer, "PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    image_style = f"""
        <style>
            .circle-image {{
                margin-top: 20px;
                border-radius: 50%;
                width: 200px;
                height: 200px;
                object-fit: cover;

            }}
            .personal-info {{
                margin-top: 20px;
                margin-right: 20px;
            }}
        </style>
    """

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(f'<div><img class="circle-image" src="data:image/png;base64,{image_data}" alt="Profile Picture"></div>' + image_style, unsafe_allow_html=True)
    with col2:
        st.markdown(f""" <div style=" margin-top: 20px; font-size: 40px;">Personal Information</div>""", unsafe_allow_html=True)
        st.markdown(f'<div style="margin-top: 20px; font-size: 20px;" class="personal-info">Username: {username}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-top: 20px; font-size: 20px;" class="personal-info">Password: {password}</div>', unsafe_allow_html=True)
