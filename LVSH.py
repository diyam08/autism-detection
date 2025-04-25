import streamlit as st

# Scoring options
options = {
    "Rarely": 1,
    "Sometimes": 2,
    "Frequently": 3,
    "Mostly": 4,
    "Always": 5
}

# Classification thresholds
def classify_autism_score(score):
    if score < 70:
        return "No autism"
    elif 70 <= score <= 106:
        return "Low likelihood of autism"
    elif 107 <= score <= 153:
        return "Moderate autism"
    else:
        return "Severe autism"

# All 40 questions
question1 = [
    # I. SOCIAL RELATIONSHIP AND RECIPROCITY
    "1.Has poor eye contact", "2.Lacks social smile", "3.Remains aloof", "4.Does not reach out to others",
    "5.Unable to relate to people", "6.Unable to respond to social/environmental cues",
    "7.Engages in solitary and repetitive play activities", "8.Unable to take turns in social interaction",
    "9.Does not maintain peer relationships"]

    # II. EMOTIONAL RESPONSIVENESS
question2=["10.Shows inappropriate emotional response", "11.Shows exaggerated emotions",
    "12.Engages in self-stimulating emotions", "13.Lacks fear of danger",
    "14.Excited or agitated for no apparent reason"]

    # III. SPEECH-LANGUAGE AND COMMUNICATION
question3=["15.Acquired speech and lost it", "16.Has difficulty using non-verbal language or gestures",
    "17.Engages in stereotyped and repetitive use of language", "18.Engages in echolalic speech",
    "19.Produces infantile squeals or unusual noises", "20.Unable to initiate or sustain conversation",
    "21.Uses jargon or meaningless words", "22.Uses pronoun reversals",
    "23.Unable to grasp pragmatics of communication"]

    # IV. BEHAVIOUR PATTERNS
question4=["24.Engages in stereotyped and repetitive motor mannerisms", "25.Shows attachment to inanimate objects",
    "26.Shows hyperactivity or restlessness", "27.Exhibits aggressive behavior",
    "28.Throws temper tantrums", "29.Engages in self-injurious behavior",
    "30.Insists on sameness"]

    # V. SENSORY ASPECTS
question5=["31.Unusually sensitive to sensory stimuli", "32.Stares into space for long periods of time",
    "33.Has difficulty in tracking objects", "34.Has unusual vision",
    "35.Insensitive to pain", "36.Responds to objects/people unusually by smelling, touching or tasting"]

    # VI. COGNITIVE COMPONENT
question6=["37.Inconsistent attention and concentration", "38.Shows delay in responding",
    "39.Has unusual memory of some kind", "40.Has ‘savant’ ability"
]

st.title("Autism Assessment Tool")

st.markdown("### Please answer the following 40 questions by selecting how frequently each behavior occurs:")

total_score = 0

input("I. SOCIAL RELATIONSHIP AND RECIPROCITY")

for i, q in enumerate(question1, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )

input("II. EMOTIONAL RESPONSIVENESS")

for i, q in enumerate(question2, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )

input("III. SPEECH-LANGUAGE AND COMMUNICATION")

for i, q in enumerate(question3, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )

input("IV. BEHAVIOUR PATTERNS")

for i, q in enumerate(question4, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )

input("V. SENSORY ASPECTS")

for i, q in enumerate(question5, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )
  
input("VI. COGNITIVE COMPONENT")

for i, q in enumerate(question6, start=1):
    response = st.radio(
        f"{i}. {q}",
        list(options.keys()),
        key=f"q{i}"
    )
total_score += options[response]

 

# Final Score and Classification
if st.button("Submit Assessment"):
    result = classify_autism_score(total_score)
    st.success(f"Total Score: {total_score}/200")
    st.info(f"Assessment Result: **{result}**")
