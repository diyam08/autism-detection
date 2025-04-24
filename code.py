import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

st.title("ASD Detection App")
st.subheader("Upload data or take the quiz")

# Upload CSV file
uploaded_file = st.file_uploader("Upload ASD dataset (.csv)", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.write("### Dataset Preview", data.head())

    # Assume target column is 'Class/ASD Traits '
    if 'Class/ASD Traits ' in data.columns:
        X = data.drop(columns=['Class/ASD Traits '])
        y = data['Class/ASD Traits '].apply(lambda x: 1 if x == 'YES' else 0)

        st.write(f"Shape: {X.shape}, Target Distribution: {y.value_counts()}")

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        # Save model
        joblib.dump(model, "model.pkl")

        # Accuracy
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        st.success(f"Model trained with accuracy: {acc:.2f}")

        # Prediction on uploaded data
        st.write("### Predict on the same data")
        preds = model.predict(X)
        data['Predicted'] = preds
        st.write(data[['Predicted']].value_counts())
    else:
        st.warning("Expected column 'Class/ASD Traits ' not found in the dataset.")

# QCHAT-10 manual screening
st.markdown("---")
st.header("Manual Screening (QCHAT-10/AQ-10)")
questions = [
    "Does your child look at you when you call his/her name?",
    "How easy is it for you to get eye contact with your child?",
    "Does your child point to indicate that s/he wants something?",
    "Does your child point to share interest with you?",
    "Does your child pretend?",
    "Does your child follow where you’re looking?",
    "Does your child show signs of wanting to comfort others?",
    "Are your child’s first words typical?",
    "Does your child use simple gestures?",
    "Does your child stare at nothing with no purpose?"
]
responses = []
for q in questions:
    responses.append(st.radio(q, [0, 1], horizontal=True))

if st.button("Predict from Manual Input"):
    score = sum(responses)
    st.write(f"Score: {score}/10")
    if score >= 6:
        st.error("⚠️ High risk of ASD. Consider professional evaluation.")
    else:
        st.success("✅ Low risk of ASD detected.")
