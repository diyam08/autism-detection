import streamlit as st
import pandas as pd
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

st.set_page_config(page_title="ASD Screening Tool", layout="centered")

st.title(" Autism Screening Tool ")
st.write("**This is a pre-diagnostic tool based on ISAA")

st.markdown("---")

# ---------- USER DETAILS ----------
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=100)
gender = st.selectbox("Gender", ["Select","Male","Female","Other"])

st.markdown("---")

st.header(" Screening Questionnaire")

# ---------- ISAA QUESTIONS ----------
questions = [
    "1. Child maintains eye contact while talking",
    "2. Child responds to their name",
    "3. Child shows interest in other children",
    "4. Child participates in group play",
    "5. Child understands simple instructions",
    "6. Child expresses emotions appropriately",
    "7. Child can communicate needs",
    "8. Child shows imaginative play",
    "9. Child shares interests with others",
    "10. Child reacts normally to sensory input",
    "11. Child can sit calmly when needed",
    "12. Child follows routines easily",
    "13. Child adapts to change",
    "14. Child reacts normally to noise",
    "15. Child reacts normally to touch",
    "16. Child reacts normally to light",
    "17. Child performs age-appropriate learning",
    "18. Child interacts socially",
    "19. Child responds when spoken to",
    "20. Child laughs and smiles appropriately",
    "21. Child uses gestures",
    "22. Child points to express interest",
    "23. Child copies actions",
    "24. Child engages in pretend play",
    "25. Child shows empathy",
    "26. Child understands others’ feelings",
    "27. Child uses appropriate language",
    "28. Child forms sentences",
    "29. Child uses language socially",
    "30. Child initiates conversation",
    "31. Child reacts normally to change",
    "32. Child plays normally with toys",
    "33. Child engages in normal activities",
    "34. Child explores environment normally",
    "35. Child expresses curiosity",
    "36. Child shows appropriate motor skills",
    "37. Child coordinates hand movements",
    "38. Child uses eye-hand coordination well",
    "39. Child imitates actions",
    "40. Child matches patterns",
    "41. Child interacts socially at home",
    "42. Child interacts socially outside",
    "43. Child behaves appropriately in groups",
    "44. Child maintains friendships",
    "45. Child behaves appropriately in school",
    "46. Child communicates with teachers",
    "47. Child follows classroom rules",
    "48. Child participates in activities",
    "49. Child displays age-appropriate behaviour",
    "50. Child seeks help when needed"
]

options = ["Never", "Rarely", "Sometimes", "Often"]

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = 0

if "answers" not in st.session_state:
    st.session_state.answers = [""] * len(questions)

# ---------- PROGRESS ----------
progress = (st.session_state.page+1) / len(questions)
st.progress(progress)
st.write(f"Question {st.session_state.page+1} of {len(questions)}")

# ---------- SHOW QUESTION ----------
q = questions[st.session_state.page]
ans = st.radio(q, options, index=options.index(st.session_state.answers[st.session_state.page]) if st.session_state.answers[st.session_state.page] else None)

st.session_state.answers[st.session_state.page] = ans

# ---------- NAVIGATION ----------
col1, col2 = st.columns(2)

with col1:
    if st.button(" Previous") and st.session_state.page > 0:
        st.session_state.page -= 1

with col2:
    if st.button("Next ➡") and st.session_state.page < len(questions)-1:
        st.session_state.page += 1

# ---------- SCORING ----------
score_map = {"Never":0,"Rarely":1,"Sometimes":2,"Often":3}

def compute_score():
    return sum(score_map.get(a,0) for a in st.session_state.answers)

# ---------- SUBMIT ----------
if st.session_state.page == len(questions)-1:
    if st.button("Submit & View Result"):
        total = compute_score()
        percent = round((total / (len(questions)*3)) * 100,2)

        st.subheader(" Your Screening Summary")
        st.write(f"**Total Score:** {total} / {len(questions)*3}")
        st.write(f"**Risk Percentage:** {percent}%")

        if percent >= 60:
            st.error(" High likelihood of autistic traits.\nPlease consult a professional.")
        elif percent >= 40:
            st.warning(" Moderate likelihood of autistic traits.\nProfessional screening recommended.")
        else:
            st.success(" Low likelihood of autistic traits.")

        st.info("This is a screening tool only — not a diagnosis.")

        # ---------- SAVE CSV ----------
        data = {
            "Name":[name],
            "Age":[age],
            "Gender":[gender],
            "Score":[total],
            "Risk %":[percent],
            "Date":[datetime.date.today()]
        }

        df = pd.DataFrame(data)
        df.to_csv("screening_results.csv", mode="a", header=not os.path.exists("screening_results.csv"), index=False)

        st.success(" Saved to CSV")

        # ---------- PDF DOWNLOAD ----------
        pdf_file = f"{name}_ASD_Report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100,700,"Autism Screening Report (ISAA Based)")
        c.drawString(100,670,f"Name: {name}")
        c.drawString(100,650,f"Age: {age}")
        c.drawString(100,630,f"Score: {total}")
        c.drawString(100,610,f"Risk: {percent}%")
        c.drawString(100,580,"Note: This is not a medical diagnosis.")
        c.save()

        with open(pdf_file,"rb") as file:
            st.download_button(" Download PDF Report", file, file_name=pdf_file)

        st.balloons()
