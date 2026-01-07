import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Autism Pre-Diagnostic Screening Tool",
    layout="centered"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.title-center {text-align:center; color:#6C63FF;}
.subtitle-center {text-align:center; color:#444;}
.card {
    background:#ffffff;
    padding:16px;
    border-radius:14px;
    border:1px solid #e6e6e6;
    margin-bottom:10px;
}
.section-title{
    color:#6C63FF;
    font-weight:700;
    font-size:22px;
    margin-top:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 class='title-center'> Autism Pre-Diagnostic Screening Tool</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle-center'>A pre-diagnostic tool only</h4>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INTRO ----------------
st.info("""
### ℹ This is a pre-diagnostic screening questionnaire designed for awareness and early observation guidance.
The questionnaire is divided into 6 sections based on behavioural & developmental domains.
Caregivers should answer based on how often the child shows each behaviour.
""")

st.markdown("---")

# ---------------- USER DETAILS ----------------
name = st.text_input("Child's Name")
age = st.number_input("Age", min_value=1, max_value=100)
gender = st.selectbox("Gender", ["Select","Male","Female","Other"])

st.markdown("---")

# ---------------- QUESTION SECTIONS ----------------
sections = {
"Social Interaction & Responsiveness": [
"Maintains eye contact while talking",
"Responds to their name",
"Shows interest in other children",
"Participates in group play",
"Interacts socially at home",
"Interacts socially outside",
"Maintains friendships",
"Behaves appropriately in groups"
],
"Communication & Language": [
"Understands simple instructions",
"Expresses emotions appropriately",
"Communicates needs",
"Uses gestures",
"Forms sentences",
"Uses language socially",
"Initiates conversation",
"Communicates with teachers"
],
"Behaviour & Adaptability": [
"Follows routines easily",
"Adapts to change",
"Follows classroom rules",
"Participates in activities",
"Sits calmly when needed",
"Displays age-appropriate behaviour",
"Reacts normally to change",
"Seeks help when needed"
],
"Sensory Response": [
"Reacts normally to noise",
"Reacts normally to touch",
"Reacts normally to light",
"Reacts normally to sensory input"
],
"Cognitive & Learning Skills": [
"Performs age-appropriate learning",
"Understands others’ feelings",
"Shows empathy",
"Matches patterns",
"Copies actions",
"Explores environment normally",
"Expresses curiosity",
"Shows imaginative or pretend play"
],
"Motor & Coordination": [
"Shows appropriate motor skills",
"Coordinates hand movements",
"Uses hand-eye coordination well",
"Engages in normal activities",
"Laughs or smiles appropriately",
"Responds when spoken to",
"Uses appropriate language",
"Plays normally with toys"
]
}

options = ["Select","Never","Rarely","Sometimes","Often"]

# ---------------- SESSION STATE ----------------
if "answers" not in st.session_state:
    st.session_state.answers = {}

total_questions = sum(len(q) for q in sections.values())

# ---------------- PROGRESS ----------------
answered = len([a for a in st.session_state.answers.values() if a!="Select"])
st.progress(answered/total_questions)
st.write(f"Progress: **{answered}/{total_questions} answered**")

st.markdown("---")

# ---------------- DISPLAY QUESTIONS ----------------
q_index = 0
for section, qs in sections.items():
    st.markdown(f"<div class='section-title'> {section}</div>", unsafe_allow_html=True)

    for q in qs:
        q_index += 1
        key = f"q{q_index}"

        st.markdown(f"<div class='card'><b>{q_index}. {q}</b></div>", unsafe_allow_html=True)

        if key not in st.session_state.answers:
            st.session_state.answers[key] = "Select"

        st.session_state.answers[key] = st.selectbox(
            f"Select answer for {q_index}",
            options,
            key=key,
            label_visibility="collapsed"
        )

st.markdown("---")

# ---------------- REVERSED RISK SCORING ----------------
score_map = {
    "Never":3,
    "Rarely":2,
    "Sometimes":1,
    "Often":0,
    "Select":0
}

def compute_score():
    return sum(score_map[a] for a in st.session_state.answers.values())

# ---------------- SUBMIT ----------------
if st.button("✔ Submit & View Result", type="primary"):

    if "Select" in st.session_state.answers.values():
        st.error("Please answer ALL questions before submitting.")
    else:
        total = compute_score()
        percent = round((total/(total_questions*3))*100,2)

        st.subheader(" Screening Summary")
        st.write(f"**Risk Score:** {total} / {total_questions*3}")
        st.write(f"**Risk Level:** {percent}%")

        # --- Feedback ---
        if percent >= 60:
            st.error(" Higher likelihood of autistic behavioural traits. Professional assessment recommended.")
        elif percent >= 40:
            st.warning(" Mild-moderate likelihood. Monitoring recommended.")
        else:
            st.success(" Low likelihood of autistic behavioural traits.")

        st.info("This screening tool is for awareness only.")

        # ---------------- CSV SAVE ----------------
        df = pd.DataFrame([{
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Risk Score": total,
            "Risk %": percent,
            "Date": datetime.date.today()
        }])

        df.to_csv(
            "screening_results.csv",
            mode="a",
            header=not os.path.exists("screening_results.csv"),
            index=False
        )

        st.success(" Result saved")

        # ---------------- GRAPHS ----------------
        st.subheader(" Risk Distribution")

        section_scores = []
        section_labels = []

        start = 0
        for sec, qs in sections.items():
            end = start + len(qs)
            ans = list(st.session_state.answers.values())[start:end]
            sec_score = sum(score_map[a] for a in ans)
            section_scores.append(sec_score)
            section_labels.append(sec)
            start = end

        # ---- BAR GRAPH ----
        fig1 = plt.figure()
        plt.bar(section_labels, section_scores)
        plt.xticks(rotation=70)
        plt.title("Section-wise Risk Scores")
        st.pyplot(fig1)

        # ---- PIE CHART ----
        fig2 = plt.figure()
        plt.pie(section_scores, labels=section_labels, autopct='%1.1f%%')
        plt.title("Risk Contribution by Section")
        st.pyplot(fig2)

        st.balloons()
