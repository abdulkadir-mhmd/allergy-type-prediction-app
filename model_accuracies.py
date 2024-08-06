import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

file_path = 'Food Allergic.xlsx'
data = pd.read_excel(file_path)

def model_accuracies():
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = pd.Categorical(data[column])
            data[column] = data[column].cat.codes

    X = data.drop('allergic_type', axis=1)
    y = data['allergic_type']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logistic_model = LogisticRegression(max_iter=1000)
    decision_tree_model = DecisionTreeClassifier()
    random_forest_model = RandomForestClassifier()
    svm_model = SVC()
    nn_model = MLPClassifier(max_iter=1000)
    naive_bayes_model = GaussianNB()
    gradient_boosting_model = GradientBoostingClassifier()

    logistic_model.fit(X_train, y_train)
    decision_tree_model.fit(X_train, y_train)
    random_forest_model.fit(X_train, y_train)
    svm_model.fit(X_train, y_train)
    nn_model.fit(X_train, y_train)
    naive_bayes_model.fit(X_train, y_train)
    gradient_boosting_model.fit(X_train, y_train)

    logistic_preds = logistic_model.predict(X_train)
    decision_tree_preds = decision_tree_model.predict(X_train)
    random_forest_preds = random_forest_model.predict(X_train)
    svm_preds = svm_model.predict(X_train)
    nn_preds = nn_model.predict(X_train)
    naive_bayes_preds = naive_bayes_model.predict(X_train)
    gradient_boosting_preds = gradient_boosting_model.predict(X_train)

    logistic_accuracy = accuracy_score(y_train, logistic_preds)
    decision_tree_accuracy = accuracy_score(y_train, decision_tree_preds)
    random_forest_accuracy = accuracy_score(y_train, random_forest_preds)
    svm_accuracy = accuracy_score(y_train, svm_preds)
    nn_accuracy = accuracy_score(y_train, nn_preds)
    naive_bayes_accuracy = accuracy_score(y_train, naive_bayes_preds)
    gradient_boosting_accuracy = accuracy_score(y_train, gradient_boosting_preds)

    st.markdown(f"""<div style="font-size: 36px;
        color: #4CAF50;
        font-weight: bold;
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;">Model Accuracies</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 24px;
        color: #2196F3;
        font-weight: bold;
        background-color: #e0f7fa;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;">Training Accuracies:</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Logistic Regression: {logistic_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Decision Tree: {decision_tree_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Random Forest: {random_forest_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">SVM: {svm_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Neural Network: {nn_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Naive Bayes: {naive_bayes_accuracy:.4f}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">Gradient Boosting: {gradient_boosting_accuracy:.4f}</div>""", unsafe_allow_html=True)

    y_pred = random_forest_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    st.markdown(f"""<div style="font-size: 24px;
        color: #2196F3;
        font-weight: bold;
        background-color: #e0f7fa;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;">Accuracy on the Test Set (Random Forest):</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 16px;
        color: #000000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;">{test_accuracy*100:.2f}%</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style="font-size: 24px;
        color: #2196F3;
        font-weight: bold;
        background-color: #e0f7fa;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;">Detailed Classification Report for Random Forest:</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size: 14px;
        color: #FF0000;
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        margin-top: 20px;">{classification_report(y_test, y_pred)}</div>""", unsafe_allow_html=True)

if __name__ == '__main__':
    model_accuracies()
