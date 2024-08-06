import hashlib
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as sns
from PIL import Image
from utils import validate_input
from model import predict_allergy_type
from dashboard import main_function
from user_profile import user_profile
from model_accuracies import model_accuracies
from test_train_accuracies import tt_accuracies
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split



def get_db_connection():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    return conn, c

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def create_usertable():
    conn, c = get_db_connection()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn, c = get_db_connection()
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()


def login_user(username, password):
    conn, c = get_db_connection()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

def create_predictiontable():
    conn, c = get_db_connection()
    c.execute('CREATE TABLE IF NOT EXISTS predictionstable(username TEXT, password TEXT, prediction TEXT)')
    conn.commit()
    conn.close()

def add_prediction(username, password, prediction):
    conn, c = get_db_connection()
    c.execute('INSERT INTO predictionstable(username,password,prediction) VALUES (?,?,?)', (username, password, prediction))
    conn.commit()
    conn.close()

def get_predictions(username):
    conn, c = get_db_connection()
    if username == 'admin':
        c.execute("SELECT * FROM predictionstable")
    else:
        c.execute("SELECT * FROM predictionstable WHERE username = ?", (username,))
    data = c.fetchall()
    conn.close()
    return data

df = pd.read_excel("Food Allergic.xlsx")

median_age = df['Age'].median()
df['Age'] = df['Age'].replace('Type B', median_age)

df['Age'] = df['Age'].astype(int)

sex_mapping = {'Male': 0, 'Female': 1}
df['Sex'] = df['Sex'].map(sex_mapping)

marital_status_mapping = {'single': 0, 'married': 1}
df['maritalstatus'] = df['maritalstatus'].map(marital_status_mapping)

education_mapping = {'University Level': 0, 'Primary': 1, 'Secondary': 2, 'illiterate': 3}
df['education'] = df['education'].map(education_mapping)

haveeverhadallegic_mapping = {'Yes': 1, 'No': 0}
df['haveeverhadallegic'] = df['haveeverhadallegic'].map(haveeverhadallegic_mapping)

diagnosisofallergic_mapping = {'Blood': 1}
df['diagnosisofallergic'] = df['diagnosisofallergic'].map(diagnosisofallergic_mapping)

clinicalpresentation_mapping = {'Conjuctivits': 0, 'Dermal': 1, 'Respiratory': 2, 'Tonsilits': 3}
df['clinicalpresentation'] = df['clinicalpresentation'].map(clinicalpresentation_mapping)


food_columns = [
                'banana', 'barley', 'corns', 'soya', 'dates', 'peanuts', 'onion', 'tomato', 'codfish', 'peach', 'eggplant', 'pumpkin', 
                'eggwhole', 'garlic', 'wheat', 'shrimp', 'carrot', 'cucumber', 'beef', 'white', 'whole', 'soyabean', 'orange', 'chocolate', 
                'sesem', 'celery', 'chilipowder', 'spinach', 'watermelon', 'rice', 'apple', 'milk', 'chicken', 'salmon', 'lobster', 'tea', 
                'mutton', 'inhalation', 'egg', 'potato', 'eggwhite', 'bean', 'pea', 'strawberry', 'coconut', 'grape', 'eggyolk', 'fish', 'mango', 
                'olive', 'almond', 'rye', 'oyster', 'scallop', 'clam', 'pistachione', 'trout', 'sweetchestnut', 'bluemussel', 'pacificsquid', 'hazelnut', 
                'kiwi', 'anchovy', 'plaice', 'eel', 'buckwheat', 'cacao', 'walnut', 'lambmeat', 'sunflower', 'pinenut', 'crab', 'pork', 'tuna', 'mackerel', 
                'mushroom', 'yeastbaker', 'citrusmixs'
                ]


for column in food_columns:
    food_mapping = {'Present': 1, 'Absent': 0}
    df[column] = df[column].map(food_mapping)
allergic_type_mapping = df['allergic_type'].unique()


df['allergic_type'] = df['allergic_type'].map({at: i for i, at in enumerate(allergic_type_mapping)})


X = df[['Age', 'Sex', 'maritalstatus', 'education', 'haveeverhadallegic', 'diagnosisofallergic', 'clinicalpresentation', 
        'banana', 'barley', 'corns', 'soya', 'dates', 'peanuts', 'onion', 'tomato', 'codfish', 'peach', 'eggplant', 'pumpkin', 
        'eggwhole', 'garlic', 'wheat', 'shrimp', 'carrot', 'cucumber', 'beef', 'white', 'whole', 'soyabean', 'orange', 'chocolate', 
        'sesem', 'celery', 'chilipowder', 'spinach', 'watermelon', 'rice', 'apple', 'milk', 'chicken', 'salmon', 'lobster', 'tea', 
        'mutton', 'inhalation', 'egg', 'potato', 'eggwhite', 'bean', 'pea', 'strawberry', 'coconut', 'grape', 'eggyolk', 'fish', 'mango', 
        'olive', 'almond', 'rye', 'oyster', 'scallop', 'clam', 'pistachione', 'trout', 'sweetchestnut', 'bluemussel', 'pacificsquid', 'hazelnut', 
        'kiwi', 'anchovy', 'plaice', 'eel', 'buckwheat', 'cacao', 'walnut', 'lambmeat', 'sunflower', 'pinenut', 'crab', 'pork', 'tuna', 'mackerel', 
        'mushroom', 'yeastbaker', 'citrusmixs']]

y = df['allergic_type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

def main(username=None, password=None):

    df = pd.read_excel("Food Allergic.xlsx")

    if username == "admin":
        navigation_options = ["Dashboard", "Prediction", "View Prediction", "Model Accuracies", "T & T Model Accuracies", "Admin Profile"]
    else:
        navigation_options = ["Prediction", "View Prediction", "User Profile"]

    navigation = st.sidebar.radio("Start", navigation_options)

    if navigation == "Dashboard":
        if username == "admin":
            main_function()
        else:
            st.write("You do not have permission to access the Dashboard.")


    elif navigation == "Prediction":
        st.title("Food Allergy Type Prediction App")
        st.subheader("Input Features")
        age = st.selectbox("Age", [1, 2, 3,  4])
        sex = st.selectbox("Sex", ["Male", "Female"])
        maritalstatus = st.selectbox("Marital Status", ["married", "single"])
        education = st.selectbox("Education", ["University Level", "Primary", "Secondary", "illiterate"])
        haveeverhadallegic = st.selectbox("Have Ever Had Allergic", ["Yes", "No"])
        diagnosisofallergic = st.selectbox("Have Ever Diagnosed Allergic", ["Blood"])
        clinicalpresentation = st.selectbox("Clinical Presentation", ["Conjuctivits", "Dermal", "Respiratory", "Tonsilits"])

        food_options = ['banana', 'barley', 'corns', 'soya', 'dates', 'peanuts', 'onion', 'tomato', 'codfish', 'peach', 'eggplant', 'pumpkin',
                        'eggwhole', 'garlic', 'wheat', 'shrimp', 'carrot', 'cucumber', 'beef', 'white', 'whole', 'soyabean', 'orange', 'chocolate',
                        'sesem', 'celery', 'chilipowder', 'spinach', 'watermelon', 'rice', 'apple', 'milk', 'chicken', 'salmon', 'lobster', 'tea',
                        'mutton', 'inhalation', 'egg', 'potato', 'eggwhite', 'bean', 'pea', 'strawberry', 'coconut', 'grape', 'eggyolk', 'fish', 'mango',
                        'olive', 'almond', 'rye', 'oyster', 'scallop', 'clam', 'pistachione', 'trout', 'sweetchestnut', 'bluemussel', 'pacificsquid', 'hazelnut',
                        'kiwi', 'anchovy', 'plaice', 'eel', 'buckwheat', 'cacao', 'walnut', 'lambmeat', 'sunflower', 'pinenut', 'crab', 'pork', 'tuna', 'mackerel',
                        'mushroom', 'yeastbaker', 'citrusmixs']

        select_all = st.checkbox("Select All")

        if select_all:
            selected_foods = st.multiselect("Select Foods", food_options, default=food_options)
        else:
            selected_foods = st.multiselect("Select Foods", food_options)

        if select_all and not selected_foods:
            st.warning("Please select at least one food item")

        if select_all and not food_columns:
            st.checkbox("Select All", value=False)

        if st.button("Predict"):
            if not selected_foods:
                st.warning("Please select at least one food item before predicting.")
            else:
                food_dict = {food: 1 if food in selected_foods else 0 for food in food_options}
                data_input = {
                    "Age": age,
                    "Sex": 0 if sex == "Male" else 1,
                    "maritalstatus": 0 if maritalstatus == "single" else 1,
                    "education": ["University Level", "Primary", "Secondary", "illiterate"].index(education),
                    "haveeverhadallegic": 1 if haveeverhadallegic == "Yes" else 0,
                    "diagnosisofallergic": 1,
                    "clinicalpresentation": ["Conjuctivits", "Dermal", "Respiratory", "Tonsilits"].index(clinicalpresentation),
                    **food_dict
                }

                if validate_input(age=age, sex=sex, maritalstatus=maritalstatus, education=education,
                        haveeverhadallegic=haveeverhadallegic, diagnosisofallergic=diagnosisofallergic,
                        clinicalpresentation=clinicalpresentation, **food_dict):
                    input_df = pd.DataFrame([data_input])
                    result = model.predict(input_df)[0]

                    if result is not None:
                        predicted_allergy_type = allergic_type_mapping[result]
                        st.success(f"The Predicted Allergy Type is: {predicted_allergy_type}")
                        add_prediction(username, password, allergic_type_mapping[result])
                        allergy_type_counts = df["allergic_type"].value_counts()
                        predicted_type_count = allergy_type_counts.get(predicted_allergy_type, 0)

                        fig, ax = plt.subplots(figsize=(6, 4))
                        ax.bar([predicted_allergy_type], [predicted_type_count], color='steelblue', width=0.5)
                        ax.set_title("Distribution of Allergy Types")
                        ax.set_xlabel("Allergy Type")
                        ax.set_ylabel("Count")
                        ax.bar_label(ax.containers[0])
                        st.pyplot(fig)
                # else:
                #     st.warning("Input validation failed. Please check your inputs.")

    elif navigation == "View Prediction":
        st.markdown(f""" 
                    <div style="background-color: #fd08; color: black; font-size: 50px; 
                    text-align: center; fornt-weight: 600; border-radius: 5px;"> View Prediction </div>
         """, unsafe_allow_html=True)
        predictions = get_predictions(username)
        if predictions:
            st.markdown(f""" <div style="background-color: #ec11;  margin: 5px 0; padding: 10px;
                              border-radius: 5px; font-size: 20px;">All User Predictions</div> """, unsafe_allow_html=True)
            for row in predictions:
                st.markdown(f"""
                    <div style="display: flex; margin-bottom: 10px; border-radius: 5px; overflow: hidden;">
                        <div style="background-color: #4682B4; padding: 10px; flex-grow: 1;">
                            <strong style="color: black; font-size: 20px;">Username:</strong> {row[0]}
                        </div>
                        <div style="background-color: #CD5C5C; padding: 10px; ">
                            <strong style="color: black; font-size: 20px;">Predicted Allergy Type:</strong> {row[2]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No predictions found.")



    elif navigation == "Model Accuracies":
        if username == "admin":
            model_accuracies()

        else:
            st.write("You do not have permission to access the Model Results.")
    
    elif navigation == "T & T Model Accuracies":
        if username == "admin":
            tt_accuracies()
        else:
            st.write("You do not have permission to access the Model Results.")

    if navigation == "Admin Profile":
        if username == "admin":
            admin_image_path = "admin-pic.jpg"
            admin_image = Image.open(admin_image_path)
            user_profile(username, password, admin_image)

        else:
            st.write("You do not have permission to access the Profile.")

    if navigation == "User Profile":
        user_image_path = "user-pic.jpg" 
        user_image = Image.open(user_image_path)
        user_profile(username, password, user_image)



# if __name__ == '__main__':
#     main()