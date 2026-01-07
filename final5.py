import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Autism Pre-Diagnostic Screening Tool", layout="centered")

# ---------------- INTRO ----------------
st.title(" Autism Pre-Diagnostic tool")

st.markdown("""
###  About this Tool:  
This is a pre-diagnostic screening questionnaire divided into 6 sections
to help estimate whether a child may be showing traits associated with Autism Spectrum Disorder (ASD).
""")
st.divider()


# ---------------- SECTIONS & QUESTIONS ----------------
SECTIONS = {
    "Communication": [
        "1. Child maintains eye contact while talking",
        "2. Child responds to their name",
        "3. Child shows interest in other children",
        "4. Child participates in group play",
        "5. Child understands simple instructions",
        "6. Child expresses emotions appropriately",
        "7. Child can communicate needs",
        "8. Child shows imaginative play",
        "9. Child shares interests with others",
        "10. Child reacts normally to sensory input"
    ],

    "Social Responsiveness": [
        "11. Child can sit calmly when needed",
        "12. Child follows routines easily",
        "13. Child adapts to change",
        "14. Child reacts normally to noise",
        "15. Child reacts normally to touch",
        "16. Child reacts normally to light",
        "17. Child performs age-appropriate learning",
        "18. Child interacts socially",
        "19. Child responds when spoken to",
        "20. Child laughs and smiles appropriately"
    ],

    "Emotional Responsiveness": [
        "21. Child uses gestures",
        "22. Child points to express interest",
        "23. Child copies actions",
        "24. Child engages in pretend play",
        "25. Child shows empathy",
        "26. Child understands others’ feelings",
        "27. Child uses appropriate language",
        "28. Child forms sentences",
        "29. Child uses language socially",
        "30. Child initiates conversation"
    ],

    "Behavior Patterns": [
        "31. Child reacts normally to change",
        "32. Child plays normally with toys",
        "33. Child engages in normal activities",
        "34. Child explores environment normally",
        "35. Child expresses curiosity",
        "36. Child shows appropriate motor skills",
        "37. Child coordinates hand movements",
        "38. Child uses eye-hand coordination well",
        "39. Child imitates actions",
        "40. Child matches patterns"
    ],

    "Cognitive Component": [
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
}

OPTIONS = ["Never", "Sometimes", "Often", "Always"]
SCORES = {"Never": 0, "Sometimes": 1, "Often": 2, "Always": 3}

if "answers" not in st.session_state:
    st.session_state.answers = {}

st.header(" Questionnaire")

q = 0
for section, questions in SECTIONS.items():
    st.subheader(section)
    for question in questions:
        st.radio(
            question,
            OPTIONS,
            key=f"q{q}",
            index=None   # ensures nothing is pre-selected
        )
        q += 1


# ---------------- SUBMIT ----------------
if st.button(" Submit Responses"):

    unanswered = [k for k in st.session_state if k.startswith("q") and st.session_state[k] is None]

    if unanswered:
        st.error("⚠ Please answer all questions.")
    else:
        total_score = 0
        section_scores = {}

        q = 0
        for section, questions in SECTIONS.items():
            s_total = 0
            for _ in questions:
                ans = st.session_state[f"q{q}"]
                s_total += SCORES[ans]
                total_score += SCORES[ans]
                q += 1
            section_scores[section] = s_total

        # ------ RISK LEVEL ------
        if total_score < 50:
            risk = "Low"
        elif total_score < 90:
            risk = "Moderate"
        else:
            risk = "High"

        st.success("Results generated ✔")

        st.write(f"###  Total Score: `{total_score}` / 150")
        st.write(f"###  Risk Level: `{risk}`")

        df = pd.DataFrame({
            "Section": list(section_scores.keys()),
            "Score": list(section_scores.values())
        })

        st.table(df)

        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(x="Section", y="Score", tooltip=["Section", "Score"])
        )

        st.altair_chart(chart, use_container_width=True)

        st.caption("This tool does not replace professional diagnosis.")

        # -------- SAVE RESULTS --------
        row = {"Total Score": total_score, "Risk": risk}
        for s, sc in section_scores.items():
            row[f"{s} Score"] = sc

        results = pd.DataFrame([row])

        if os.path.exists("results.csv"):
            results.to_csv("results.csv", mode="a", header=False, index=False)
        else:
            results.to_csv("results.csv", index=False)

        st.success(" Results saved (results.csv)")
