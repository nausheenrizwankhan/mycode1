import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import random
import os

# 🎨 Custom CSS Styling

st.markdown("""
    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(270deg, #f6d365, #fda085, #fbc2eb, #a18cd1);
        background-size: 800% 800%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Arial', sans-serif;
        color: #333;
    }

    h1 {
        color: #fff;
        text-align: center;
        font-size: 3.5rem;
        animation: bounce 2s infinite;
        margin-top: 40px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    h2, h3 {
        color: #4CAF50;
        text-align: center;
    }

    .flashcard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 16px rgba(30,40,50,0.1);
        margin: 10px 0;
        text-align: center;
    }

    .button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        margin: 10px !important;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .button:hover {
        background-color: #45a049 !important;
        transform: scale(1.05);
    }

    .footer {
        text-align: center; 
        margin-top: 40px; 
        font-size: 14px; 
        color: #000;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }

    .linkedin-logo {
        width: 35px;
        height: 35px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        animation: glow 2s infinite;
    }

    @keyframes glow {
        0% { box-shadow: 0 0 5px #0077b5; }
        50% { box-shadow: 0 0 20px #0077b5; }
        100% { box-shadow: 0 0 5px #0077b5; }
    }

    .home-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 50px;
    }

    </style>
""", unsafe_allow_html=True)


# 🎓 Bouncing Animated App Title

st.markdown("<h1>🎓 Flashcard Quiz App</h1>", unsafe_allow_html=True)


# 📂 Load or Initialize Flashcards

FLASHCARDS_FILE = "flashcards.csv"

def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        return pd.read_csv(FLASHCARDS_FILE).to_dict(orient='records')
    return []

def save_flashcards(flashcards):
    df = pd.DataFrame(flashcards)
    df.to_csv(FLASHCARDS_FILE, index=False)

# Initialize flashcards
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = load_flashcards()

# Initialize other states
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False

# ===========================
# 🏠 Home Page with Navigation Buttons
# ===========================
st.markdown("<h2>Welcome to  Flashcard Frenzy Quiz Time!</h2>", unsafe_allow_html=True)
st.markdown("<h3> Brain Power Challenge Lets Get Started!</h3>", unsafe_allow_html=True)

st.markdown("<div class='home-container'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Flashcards", key="add", use_container_width=True):
        st.session_state.menu_selection = "add"

with col2:
    if st.button("📝 Take Quiz", key="quiz", use_container_width=True):
        st.session_state.menu_selection = "quiz"
        st.session_state.quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_active = True

with col3:
    if st.button("📊 View Flashcards", key="view", use_container_width=True):
        st.session_state.menu_selection = "view"

st.markdown("</div>", unsafe_allow_html=True)

# ===========================
# 🚀 Menu Logic
# ===========================
menu = st.session_state.get("menu_selection", "home")

# ➕ Add Flashcards Page
if menu == "add":
    st.header("➕ Add a New Flashcard")
    with st.form(key='add_flashcard_form'):
        question = st.text_input("Enter your Question")
        answer = st.text_input("Enter the Answer")
        submit = st.form_submit_button("Add Flashcard", type="primary")
        if submit:
            if question and answer:
                st.session_state.flashcards.append({'question': question, 'answer': answer})
                save_flashcards(st.session_state.flashcards)
                st.success("✅ Flashcard Added!")
                st.balloons()
            else:
                st.error("⚠️ Both fields are required.")

# 📊 View Flashcards Page
if menu == "view":
    st.header("📚 Your Flashcards")
    if st.session_state.flashcards:
        df_flashcards = pd.DataFrame(st.session_state.flashcards)
        st.dataframe(df_flashcards, use_container_width=True)
    else:
        st.warning("⚠️ No flashcards available. Add some first!")

# 📝 Take Quiz Page - ALL QUESTIONS AT ONCE!
if menu == "quiz":
    st.header("📝 Flashcard Quiz")

    if not st.session_state.flashcards:
        st.warning("⚠️ No flashcards to quiz! Add some first.")
    else:
        st.info("Answer all questions below and click **Submit Answers** to see your score!")

        # Dictionary to hold user answers
        user_answers = {}

        # Generate input fields for each question
        for idx, card in enumerate(st.session_state.flashcards):
            st.subheader(f"Question {idx + 1}: {card['question']}")
            answer_key = f"user_answer_{idx}"
            user_answers[answer_key] = st.text_input("Your Answer:", key=answer_key)

        # Submit button to evaluate all answers
        if st.button("✅ Submit Answers"):
            score = 0
            total = len(st.session_state.flashcards)

            # Evaluate answers
            for idx, card in enumerate(st.session_state.flashcards):
                correct_answer = card['answer'].strip().lower()
                user_answer = user_answers[f"user_answer_{idx}"].strip().lower()

                if user_answer == correct_answer:
                    score += 1

            # Show result
            st.success(f"🎉 You got {score} out of {total} correct!")
            st.balloons()

            # Optional: Show correct answers for review
            with st.expander("🔍 See Correct Answers"):
                for idx, card in enumerate(st.session_state.flashcards):
                    st.write(f"✅ {idx + 1}. {card['question']}")
                    st.write(f"   Correct Answer: **{card['answer']}**")



# 📝 Footer:
st.markdown("""
    <div class="footer">
        <p>Made by <strong>Nausheen Rizwan</strong></p>
        <a href="https://www.linkedin.com/in/nausheen-khan-5026b3276/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" class="linkedin-logo">
        </a>
    </div>
""", unsafe_allow_html=True)