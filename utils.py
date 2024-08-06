import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as sns
import pickle
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


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

def validate_input(age, sex, maritalstatus, education, haveeverhadallegic, diagnosisofallergic, clinicalpresentation, **food_columns):
    """
    
    """

    
    try:
        if age not in [1, 2, 3, 4]:
            return False
        if sex not in ["Male", "Female"]:
            return False
        if maritalstatus not in ["married", "single"]:
            return False
        if education not in ["University Level", "Primary", "Secondary", "illiterate"]:
            return False
        if haveeverhadallegic not in ["Yes", "No"]:
            return False
        if diagnosisofallergic not in ["Blood"]:
            return False
        if clinicalpresentation not in ["Conjuctivits", "Dermal", "Respiratory", "Tonsilits"]:
            return False

        
        if age == 1 and maritalstatus == "married":
            st.warning("You cannot select 'Married or 'University Level' and 'Secondary' while you are not an adult.")
            return False
        
        if age == 1 and education in ["University Level", "Secondary"]:
            st.warning("You cannot select 'University Level' or 'Secondary' as education level while you are not an adult.")
            return False
        
       
        if not all(food in food_columns for food in food_columns):
            st.warning("Please select at least one food item before predicting.")
            return False

        return True
    except ValueError:
        return True