import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


file_path = 'Food Allergic.xlsx'
data = pd.read_excel(file_path)

def tt_accuracies():

    label_encoder = LabelEncoder()
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = label_encoder.fit_transform(data[column])


    X = data.drop('allergic_type', axis=1)
    y = data['allergic_type']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier()


    rf_model.fit(X_train, y_train)


    train_preds = rf_model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_preds)


    test_preds = rf_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_preds)

    st.markdown(f"""<div style="font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;">Model Accuracies</div>""", unsafe_allow_html=True)
    st.markdown(
    '<p style="background-color: #f3e5f5; color: #000000; font-size: 20px; padding: 10px; margin-top: 10px;">Training Accuracy: {:.2f}%</p>'.format(train_accuracy * 100),
    unsafe_allow_html=True
    )

    st.markdown(
        '<p style="background-color: #f3e5f5; color: #000000; font-size: 20px; padding: 10px; ">Testing Accuracy: {:.2f}%</p>'.format(test_accuracy * 100),
        unsafe_allow_html=True
    )



if __name__ == '__main__':
    tt_accuracies()