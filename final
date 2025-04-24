import streamlit as st
import pandas as pd

# Title
st.title("Diagnosis Of ASD")

# Description
st.markdown("""
This app screens for Autism Spectrum Disorder (ASD) based on a questionnaire.The Questionnaire consists of 20 compulsory questions that help in detecting any signs of ASD.
""")

# Question list for QCHAT-10 or AQ-10 (Yes = 1, No = 0)
questions = [
    '1.I prefer to do things on my own, rather than with others.',
'2.I prefer doing things the same way and repeating them over and over.', 
'3.I find myself becoming strongly absorbed in something',
'4.I am very sensitive to noise and will wear earplugs or cover my ears in certain situations',
'5.I find it hard to maintain eye contact with others',
'6.Sometimes people say I am being rude or uninterested, even though I think I am being polite',
'7.I find it hard to imagine what characters from a book might look like.',
'8.I like to follow a fixed routine each day',
'9.I find it upsetting if my daily routine is changed',
'10.I find it hard to frame a sentence and often repeat certain phrases.',
'11.It’s difficult for me to understand other people’s facial expression and body language',
'12.It’s difficult for me to express my feelings ',
'13.I notice very small changes in a person’s appearance',
'14.I like collecting and categorizing things of my interest',
'15.I don’t prefer meeting new people and socializing',
'16.New social situations make me feel anxious',
'17.I am often the last person to understand a joke or sarcasm',
'18.I find it hard to talk in groups of people',
'19.I find numbers, dates and strings of information fascinating',
'20.I notice patterns in things all the time'
]

# Collect answers
st.markdown("For each statement below, choose a response that best describes how strongly that statement applies to you")
responses = []
for q in questions:
    responses.append(st.radio(q, ['yes','no'], horizontal=True))
    
# Compute score
score =responses.count('yes')
st.markdown(f"### Total Score: {score}/20")

# Predict ASD
if st.button("Check ASD Risk"):
    if score >= 11:
        st.error("⚠️ High risk of ASD detected. Please consult a professional.")
    else:
        st.success("✅ Low risk of ASD detected.")

# Footer
st.markdown("---")
st.caption("Any scores of 11 or greater indicate the presence of autistic traits; the higher the score, the more autistic traits you have.Please note that no single test is conclusive")
