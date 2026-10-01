
import streamlit as st
import pickle
import re


st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🎓",
    layout="centered"
)



@st.cache_resource
def load_models():

    with open("tfidf_vectorizer.pkl", "rb") as f:
        tfidf = pickle.load(f)

    with open("label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)

    with open("svm.pkl", "rb") as f:
        svm_model = pickle.load(f)

    with open("bot_response_mapping.pkl", "rb") as f:
        bot_response_mapping = pickle.load(f)

    return (
        tfidf,
        label_encoder,
        svm_model,
        bot_response_mapping
    )


tfidf, label_encoder, svm_model, bot_response_mapping = load_models()




def clean_text(text):

    text = str(text)

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9\s]',
        '',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text


greetings = {

    "hi":
    "Hello! How can I help you?",

    "hello":
    "Hi! How can I assist you?",

    "hey":
    "Hey! What can I do for you?",

    "good morning":
    "Good morning! How can I help you?",

    "good afternoon":
    "Good afternoon! How can I help you?",

    "good evening":
    "Good evening! How can I help you?"

}



def predict_intent(message):

    message = clean_text(message)

    message_tfidf = tfidf.transform(
        [message]
    )

    prediction = svm_model.predict(
        message_tfidf
    )

    intent = label_encoder.inverse_transform(
        prediction
    )[0]

    return intent




st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)




if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",
            "content":
            "Hello! 👋 How can I help you today?"
        }

    ]


if "recent_questions" not in st.session_state:

    st.session_state.recent_questions = []



st.markdown(
    '<div class="main-title">🎓 AI ChatBot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask me anything about your campus</div>',
    unsafe_allow_html=True
)




st.subheader("💡 Common Questions")

common_questions = [

    "What are the college timings?",

    "How can I contact the college office?",

    "Where is the library?",

    "What are the admission requirements?"

]

cols = st.columns(2)

for i, question in enumerate(common_questions):

    with cols[i % 2]:

        if st.button(
            question,
            key=f"common_{i}"
        ):

            st.session_state.selected_question = question




st.subheader("🔥 Most Asked")

most_asked = [

    "What is the fee structure?",

    "What are the exam dates?",

    "How can I apply for leave?"

]

cols = st.columns(2)

for i, question in enumerate(most_asked):

    with cols[i % 2]:

        if st.button(
            question,
            key=f"asked_{i}"
        ):

            st.session_state.selected_question = question







st.divider()

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )




def process_message(message):

    if not message:
        return

    

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )



    if message in st.session_state.recent_questions:

        st.session_state.recent_questions.remove(
            message
        )

    st.session_state.recent_questions.insert(
        0,
        message
    )

    st.session_state.recent_questions = (
        st.session_state.recent_questions[:5]
    )



    cleaned_message = clean_text(
        message
    )


    if cleaned_message in greetings:

        response = greetings[
            cleaned_message
        ]

    else:

    

        intent = predict_intent(
            message
        )


        response = bot_response_mapping.get(

            intent,

            "Sorry, I could not understand your question."

        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )



if "selected_question" in st.session_state:

    question = st.session_state.selected_question

    del st.session_state.selected_question

    process_message(
        question
    )

    st.rerun()




message = st.chat_input(
    "Type your question..."
)


if message:

    process_message(
        message
    )

    st.rerun()

