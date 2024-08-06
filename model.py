import streamlit as st
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import streamlit as sns
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
        'mushroom', 'yeastbaker', 'citrusmixs'
        ]]
y = df['allergic_type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

def predict_allergy_type(age, sex, maritalstatus, education, haveeverhadallegic, diagnosisofallergic, clinicalpresentation, 
                         banana, barley, corns, soya, dates, peanuts, onion, tomato, codfish, peach, eggplant, pumpkin, eggwhole, 
                         garlic, wheat, shrimp, carrot, cucumber, beef, white, whole, soyabean, orange, chocolate, sesem, celery, 
                         chilipowder, spinach, watermelon, rice, apple, milk, chicken, salmon, lobster, tea, mutton, inhalation, 
                         egg, potato, eggwhite, bean, pea, strawberry, coconut, grape, eggyolk, fish, mango, olive, almond, rye, 
                         oyster, scallop, clam, pistachione, trout, sweetchestnut, bluemussel, pacificsquid, hazelnut, kiwi, anchovy, 
                         plaice, eel, buckwheat, cacao, walnut, lambmeat, sunflower, pinenut, crab, pork, tuna, mackerel, mushroom, yeastbaker, 
                         citrusmixs):

    input_data = np.array([[age, 
                           sex_mapping[sex],
                           marital_status_mapping[maritalstatus],
                           education_mapping[education],
                           haveeverhadallegic_mapping[haveeverhadallegic],
                           diagnosisofallergic_mapping[diagnosisofallergic],
                           clinicalpresentation_mapping[clinicalpresentation],
                           banana, barley, corns, soya, dates, peanuts, onion, tomato, codfish, peach, eggplant, pumpkin, eggwhole, 
                           garlic, wheat, shrimp, carrot, cucumber, beef, white, whole, soyabean, orange, chocolate, sesem, celery, 
                           chilipowder, spinach, watermelon, rice, apple, milk, chicken, salmon, lobster, tea, mutton, inhalation, 
                           egg, potato, eggwhite, bean, pea, strawberry, coconut, grape, eggyolk, fish, mango, olive, almond, rye, 
                           oyster, scallop, clam, pistachione, trout, sweetchestnut, bluemussel, pacificsquid, hazelnut, kiwi, anchovy, 
                           plaice, eel, buckwheat, cacao, walnut, lambmeat, sunflower, pinenut, crab, pork, tuna, mackerel, mushroom, yeastbaker, 
                           citrusmixs]])
    prediction = model.predict(input_data)
    return allergic_type_mapping[int(prediction[0])]