import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="ASD Screening Tool", layout="centered")

# ---------- HEADER ----------
st.markdown(
    """
    <h2 style='text-align:center;color:#4A6FA5;'> Autism Screening Tool</h2>
    <p style='text-align:center;color:gray;'>
    This is only a pre-diagnostic tool inspired by the standards from ISAA
    </p>
    """,
    unsafe_allow_html=True
)

# ---------- USER INFO ----------
st.markdown("###  Participant Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=100)
gender = st.selectbox("Gender", ["Select","Male","Female","Other"])

st.markdown("---")

# ---------- OPTIONS ----------
options = ["Never", "Rarely", "Sometimes", "Often"]
score_map = {"Never":0,"Rarely":1,"Sometimes":2,"Often":3}

# ---------- QUESTION BANK (6 SECTIONS) ----------

sections = {
"Social Relationship & Responsiveness": [
"Child maintains eye contact while talking",
"Child responds to their name",
"Child shows interest in other children",
"Child participates in group play",
"Child understands simple instructions",
"Child expresses emotions appropriately",
"Child can communicate needs",
"Child shows imaginative play",
"Child shares interests with others",
"Child reacts normally to sensory input"
],

"Communication": [
"Child can sit calmly when needed",
"Child follows routines easily",
"Child adapts to change",
"Child reacts normally to noise",
"Child reacts normally to touch",
"Child reacts normally to light",
"Child performs age-appropriate learning",
"Child interacts socially",
"Child responds when spoken to",
"Child laughs and smiles appropriately"
],

"Emotional Responsiveness": [
"Child uses gestures",
"Child points to express interest",
"Child copies actions",
"Child engages in pretend play",
"Child shows empathy",
"Child understands others’ feelings",
"Child uses appropriate language",
"Child forms sentences",
"Child uses language socially",
"Child initiates conversation"
],

"Cognitive Component": [
"Child reacts normally to change",
"Child plays normally with toys",
"Child engages in normal activities",
"Child explores environment normally",
"Child expresses curiosity",
"Child shows appropriate motor skills"
],

"Sensory & Motor Behaviours": [
"Child coordinates hand movements",
"Child uses eye-hand coordination well",
"Child imitates actions",
"Child matches patterns",
"Child interacts socially at home",
"Child interacts socially outside"
],

"Behaviour Pattern": [
"Child behaves appropriately in groups",
"Child maintains friendships",
"Child behaves appropriately in school",
"Child communicates with teachers",
"Child follows classroom rules",
"Child participates in activities",
"Child displays age-appropriate behaviour",
"Child seeks help when needed"
]
}

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = [""]*50

section_names = list(sections.keys())

# ---------- PROGRESS ----------
total_pages = len(section_names)
progress = (st.session_state.page+1)/total_pages
st.progress(progress)

st.markdown(f"###  Section {st.session_state.page+1}: {section_names[st.session_state.page]}")

# ---------- DISPLAY QUESTIONS ----------
start_index = sum(len(sections[n]) for n in section_names[:st.session_state.page])
for i, q in enumerate(sections[section_names[st.session_state.page]]):
    idx = start_index + i
    st.session_state.answers[idx] = st.radio(
        q,
        options,
        index=options.index(st.session_state.answers[idx]) if st.session_state.answers[idx] else None
    )

# ---------- NAVIGATION ----------
col1, col2 = st.columns(2)
with col1:
    if st.button(" Previous") and st.session_state.page > 0:
        st.session_state.page -= 1

with col2:
    if st.button("Next ➡") and st.session_state.page < total_pages-1:
        st.session_state.page += 1


# ---------- SUBMIT ----------
if st.session_state.page == total_pages-1:
    if st.button("✔ Submit & View Result"):

        total_score = sum(score_map.get(a,0) for a in st.session_state.answers)
        max_score = 50*3
        percent = round((total_score/max_score)*100,2)

        st.markdown("---")
        st.subheader(" Screening Summary")
        st.write(f"**Total Score:** {total_score} / {max_score}")
        st.write(f"**Risk Percentage:** {percent}%")

        if percent >= 60:
            st.error(" High likelihood of autistic traits — professional evaluation recommended.")
        elif percent >= 40:
            st.warning(" Moderate likelihood — consider consulting a specialist.")
        else:
            st.success(" Low likelihood of autistic traits.")

        st.info("This screening is for educational purposes only and is not a diagnosis.")

        # ---------- SAVE CSV ----------
        df = pd.DataFrame({
            "Name":[name],
            "Age":[age],
            "Gender":[gender],
            "Score":[total_score],
            "Risk %":[percent],
            "Date":[datetime.date.today()]
        })

        df.to_csv("results.csv", mode="a", header=not os.path.exists("results.csv"), index=False)

        st.success(" Result saved to CSV")

        # ---------- DOWNLOAD TEXT REPORT ----------
        report = f"""
Autism Screening Report (Educational Tool)

Name: {name}
Age: {age}
Gender: {gender}
Date: {datetime.date.today()}

Total Score: {total_score} / {max_score}
Risk Percentage: {percent}%

Note: This is NOT a diagnostic assessment.
"""

        st.download_button(" Download Report", report, file_name=f"{name}_ASD_Report.txt")

        st.balloons()
