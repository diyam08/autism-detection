import streamlit as st
import pandas as pd
import datetime
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ASD Screening Tool",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {background-color: #f0f4f8; font-family: 'Helvetica', sans-serif;}
h2 {color: #6C63FF; text-align:center;}
.stButton>button {background-color:#6C63FF; color:white; font-weight:bold; border-radius:8px; padding:8px 15px;}
.stRadio label {font-weight:bold;}
.card {background-color:white; padding:15px; border-radius:10px; margin-bottom:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    "<h2> Autism Screening Tool</h2>"
    "<p style='text-align:center;color:gray;'>This is a pre-dianostic tool only</p>",
    unsafe_allow_html=True
)

# ---------- USER INFO ----------
st.markdown("### Personal details:")
name = st.text_input("Child Name")
age = st.number_input("Age", min_value=1, max_value=100)
gender = st.selectbox("Gender", ["Select","Male","Female","Other"])
st.markdown("---")

# ---------- OPTIONS & SCORING ----------
options = ["Never","Rarely","Sometimes","Often"]
score_map = {"Never":3, "Rarely":2, "Sometimes":1, "Often":0}  # Correct risk scoring

# ---------- QUESTIONS & SECTIONS WITH EMOJIS ----------
sections = {
" Social Relationship & Responsiveness": [
"1.Child maintains eye contact while talking",
"2.Child responds to their name",
"3.Child shows interest in other children",
"4.Child participates in group play",
"5.Child understands simple instructions",
"6.Child expresses emotions appropriately",
"7.Child can communicate needs",
"8.Child shows imaginative play",
"9.Child shares interests with others",
"10.Child reacts normally to sensory input"
],
" Communication": [
"1.Child can sit calmly when needed",
"2.Child follows routines easily",
"3.Child adapts to change",
"4.Child reacts normally to noise",
"5.Child reacts normally to touch",
"6.Child reacts normally to light",
"7.Child performs age-appropriate learning",
"8.Child interacts socially",
"9.Child responds when spoken to",
"10.Child laughs and smiles appropriately"
],
" Emotional Responsiveness": [
"1.Child uses gestures",
"2.Child points to express interest",
"3.Child copies actions",
"4.Child engages in pretend play",
"5.Child shows empathy",
"6.Child understands others’ feelings",
"7.Child uses appropriate language",
"8.Child forms sentences",
"9.Child uses language socially",
"10.Child initiates conversation"
],
" Cognitive Component": [
"1.Child reacts normally to change",
"2.Child plays normally with toys",
"3.Child engages in normal activities",
"4.Child explores environment normally",
"5.Child expresses curiosity",
"6.Child shows appropriate motor skills"
],
" Sensory & Motor Behaviours": [
"1.Child coordinates hand movements",
"2.Child uses eye-hand coordination well",
"3.Child imitates actions",
"4.Child matches patterns",
"5.Child interacts socially at home",
"6.Child interacts socially outside"
],
" Behaviour Pattern": [
"1.Child behaves appropriately in groups",
"2.Child maintains friendships",
"3.Child behaves appropriately in school",
"4.Child communicates with teachers",
"5.Child follows classroom rules",
"6.Child participates in activities",
"7.Child displays age-appropriate behaviour",
"8.Child seeks help when needed"
]
}

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = [""]*50

section_names = list(sections.keys())
total_pages = len(section_names)

# ---------- DISPLAY PROGRESS ----------
progress = (st.session_state.page+1)/total_pages
st.progress(progress)
st.markdown(f"###  Section {st.session_state.page+1}: {section_names[st.session_state.page]}")

# ---------- DISPLAY QUESTIONS AS CARDS WITH UNIQUE KEYS ----------
start_index = sum(len(sections[n]) for n in section_names[:st.session_state.page])
for i, q in enumerate(sections[section_names[st.session_state.page]]):
    idx = start_index + i
    st.markdown(f"<div class='card'>{idx+1}. {q}</div>", unsafe_allow_html=True)
    st.session_state.answers[idx] = st.radio(
        label="",
        options=options,
        index=options.index(st.session_state.answers[idx]) if st.session_state.answers[idx] else None,
        key=f"q_{idx}"  # <<< UNIQUE KEY FIXED
    )

# ---------- NAVIGATION ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅ Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
with col2:
    if st.button("Next ➡") and st.session_state.page < total_pages-1:
        st.session_state.page += 1

# ---------- COMPUTE SCORE ----------
def compute_score():
    return sum(score_map.get(a,0) for a in st.session_state.answers)

# ---------- SUBMIT ----------
if st.session_state.page == total_pages-1:
    if st.button("✔ Submit & View Result"):
        total_score = compute_score()
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

        # ---------- VISUAL OVERALL RISK BAR ----------
        st.markdown("### Overall Autism Risk")
        st.progress(percent/100)

        # ---------- DOMAIN-WISE BAR CHART USING st.bar_chart ----------
        domain_scores = []
        domain_names = []
        for sec in section_names:
            idx_start = sum(len(sections[n]) for n in section_names[:section_names.index(sec)])
            idx_end = idx_start + len(sections[sec])
            domain_total = sum(score_map.get(a,0) for a in st.session_state.answers[idx_start:idx_end])
            domain_scores.append(domain_total)
            domain_names.append(sec)
        st.markdown("### Domain-wise Scores")
        domain_df = pd.DataFrame({"Domain":domain_names,"Score":domain_scores})
        domain_df = domain_df.set_index("Domain")
        st.bar_chart(domain_df)

        # ---------- DOWNLOAD REPORT ----------
        report = f"""
Autism Screening Report (Educational Tool)

Name: {name}
Age: {age}
Gender: {gender}
Date: {datetime.date.today()}

Total Score: {total_score} / {max_score}
Risk Percentage: {percent}%

Domain Scores:
"""
        for sec, s in zip(section_names, domain_scores):
            report += f"{sec}: {s}\n"

        report += "\nNote: This is NOT a diagnostic assessment."
        st.download_button("⬇ Download Report", report, file_name=f"{name}_ASD_Report.txt")

        st.balloons()
