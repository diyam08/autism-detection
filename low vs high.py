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
questions = [
    # I. SOCIAL RELATIONSHIP AND RECIPROCITY
    "Has poor eye contact", "Lacks social smile", "Remains aloof", "Does not reach out to others",
    "Unable to relate to people", "Unable to respond to social/environmental cues",
    "Engages in solitary and repetitive play activities", "Unable to take turns in social interaction",
    "Does not maintain peer relationships",

    # II. EMOTIONAL RESPONSIVENESS
    "Shows inappropriate emotional response", "Shows exaggerated emotions",
    "Engages in self-stimulating emotions", "Lacks fear of danger",
    "Excited or agitated for no apparent reason",

    # III. SPEECH-LANGUAGE AND COMMUNICATION
    "Acquired speech and lost it", "Has difficulty using non-verbal language or gestures",
    "Engages in stereotyped and repetitive use of language", "Engages in echolalic speech",
    "Produces infantile squeals or unusual noises", "Unable to initiate or sustain conversation",
    "Uses jargon or meaningless words", "Uses pronoun reversals",
    "Unable to grasp pragmatics of communication",

    # IV. BEHAVIOUR PATTERNS
    "Engages in stereotyped and repetitive motor mannerisms", "Shows attachment to inanimate objects",
    "Shows hyperactivity or restlessness", "Exhibits aggressive behavior",
    "Throws temper tantrums", "Engages in self-injurious behavior",
    "Insists on sameness",

    # V. SENSORY ASPECTS
    "Unusually sensitive to sensory stimuli", "Stares into space for long periods of time",
    "Has difficulty in tracking objects", "Has unusual vision",
    "Insensitive to pain", "Responds to objects/people unusually by smelling, touching or tasting",

    # VI. COGNITIVE COMPONENT
    "Inconsistent attention and concentration", "Shows delay in responding",
    "Has unusual memory of some kind", "Has ‘savant’ ability"
]

st.title("Autism Assessment Tool")

st.markdown("### Please answer the following 40 questions by selecting how frequently each behavior occurs:")

total_score = 0

for i, q in enumerate(questions, start=1):
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
