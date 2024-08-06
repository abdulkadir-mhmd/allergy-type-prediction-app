import hashlib
import sqlite3
import pandas as pd
import streamlit as st
import plotly_express as pe
import pickle
from pathlib import Path
import streamlit_authenticator as sta
from streamlit_option_menu import option_menu


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    existing_user = c.fetchone()
    if existing_user:
        st.warning("User already exists. Please choose a different username.")
    else:
        c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        st.success("You have successfully created an Account")
        st.info("Go to Login Menu to login")

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def create_predictiontable():
    c.execute('CREATE TABLE IF NOT EXISTS predictionstable(username TEXT, prediction TEXT)')
    conn.commit()

def add_prediction(username, prediction):
    c.execute('INSERT INTO predictionstable(username, prediction) VALUES (?, ?)', (username, prediction))
    conn.commit()

def main():
    st.set_page_config(page_title="Food Allergy Prediction Dashboard", page_icon="📊")
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'password' not in st.session_state:
        st.session_state['password'] = ''

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        selected = option_menu(
            menu_title=None,  
            options=["Home", "About", "Contact"],
            icons=["house", "book", "envelope"],  
            menu_icon="cast",  
            default_index=0,  
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#0083B8"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )


        if selected == "Home":
            st.markdown("""
                <div style="padding: 5px; text-align: center;">
                    <h1>Welcome to the Food Allergy Type Prediction Website</h1>
                    <p style="font-size: 18px;">
                        This application helps individuals predict and manage food allergies more effectively using machine learning algorithms.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.header("Purpose and Goals")
            st.write("""
                The primary goal of this application is to provide users with a tool to predict the type of food allergy they might have based on their symptoms. By using advanced machine learning algorithms, we aim to offer accurate and timely predictions to help users take appropriate actions.
            """)

            st.header("Features")
            st.write("""
                - **Symptom Analysis:** Input your symptoms and get a prediction of possible food allergies.
                - **Historical Data:** Track and analyze past allergy incidents to identify patterns.
                - **Resource Links:** Access a collection of resources and articles related to food allergies.
            """)

            st.header("How to Use")
            st.write("""
                Navigate through the menu options to access different features of the application. Start by entering your symptoms and information in the 'Prediction Analysis' section to get a prediction of possible type of the allergies.
            """)

            st.header("Benefits")
            st.write("""
                Using this application, you can gain valuable insights into your food allergies, manage your symptoms more effectively, and access helpful resources to improve your quality of life.
            """)

            st.header("Get Started")
            st.write(""" 
                     To get started you must follow these instaructions.
                - **Menu:** Click on the menu at the left side of the page in the sidebar.
                - **Login:** Enter your username and password.
                - **Registration:** You can create a new account if are new on the website.
                - **Input Form:** Enter your Medical History, Symptoms and required fields and then click the predict button.
            """)
        elif selected == "About":
            st.title("About Us")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.image("image1.png", width=140, caption="Abdulkadir Mohamed")
            with col2:
                st.image("image2.jpeg", width=140, caption="Abdifitah Maow Sufi")
            with col3:
                st.image("image3.jpeg", width=140, caption="Abdullahi Muhumed")
            with col4:
                st.image("image4.jpeg", width=140, caption="Omar Abdirisaq")
            st.markdown("""
                # About This Website

                Welcome to the Food Allergy Type Prediction Dashboard. This application was created to help individuals predict and manage food allergies more effectively.

                ## Purpose and Goals
                The primary goal of this application is to provide users with a tool to predict the type of food allergy they might have based on their symptoms. By using machine learning algorithms, the application aims to offer accurate and timely predictions to help users take appropriate actions.

                ## Features
                - **Symptom Analysis:** Input your symptoms and get a prediction of possible food allergies.
                - **Historical Data:** Track and analyze past allergy incidents to identify patterns.
                - **Resource Links:** Access a collection of resources and articles related to food allergies.

                ## Technology Used
                This application is built using:
                - **Streamlit:** For the web interface.
                - **Scikit-Learn:** For machine learning models.
                - **Pandas:** For data manipulation and analysis.

                ## Future Plans
                We are constantly working to improve this application. Future updates may include:
                - Integration with medical databases for more accurate predictions.
                - Enhanced data visualization tools.
                - Mobile application version.

                ## Acknowledgments
                Special thanks to all contributors and supporters who helped make this project possible. We also appreciate the valuable feedback from our users.

                ## Contact Information
                If you have any questions, feedback, or need support, please feel free to reach out:
                - **Email:** abdulkadir00b@gmail.com
                - **GitHub:** https://github.com/abdulkadir-mhmd
                - **Phone:** +252612537535

                Thank you for using our application!
            """, unsafe_allow_html=True)
        elif selected == "Contact":
            st.title(f"Contact Us")
            st.title(f"Jamhuriya University edu.jamhuriya@edu.so")
            st.title(f"You can reach us at {selected}")
            st.write("Get in touch with us!")
            st.write("Email: abdulkadir00b@gmail.com")
            st.write("GitHub: https://github.com/abdulkadir-mhmd")
            st.write("Phone: +252612537535")
    
    elif choice == "Login":
        if not st.session_state['logged_in']:
            st.subheader("Login Section")

            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                hashed_pswd = make_hashes(password)
                result = login_user(username, check_hashes(password, hashed_pswd))

                if result:
                    st.success("Logged In as {}".format(username))
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.warning("Incorrect Username/Password")
        else:
            prediction_form(st.session_state['username'], st.session_state['password'])

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            add_userdata(new_user, make_hashes(new_password))
            
    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['password'] = ''
            st.rerun()

def prediction_form(username, password):
    from prediction_form import main as prediction_form_main
    prediction_form_main(username, password)

if __name__ == '__main__':
    main()