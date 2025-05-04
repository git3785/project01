import streamlit as st
import random
import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

from datetime import datetime

# -------------------- App Setup --------------------
st.set_page_config(page_title="Growth Mindset Challenge", layout="centered")

# -------------------- Data --------------------
quotes = [
    "Mistakes are proof that you're trying.",
    "Your brain is like a muscle—the more you use it, the stronger it gets.",
    "Failure is not the opposite of success, it's part of success.",
    "Effort is the path to mastery.",
    "I can learn anything I want to.",
    "I grow when I challenge myself."
]

quiz_questions = {
    "I believe intelligence can be developed.": 1,
    "When I fail, I see it as a chance to grow.": 1,
    "I avoid challenges because I'm afraid to fail.": 0,
    "Effort is more important than talent.": 1,
    "I take criticism personally.": 0
}

# -------------------- Sidebar Navigation --------------------
st.sidebar.title("📚 Growth Mindset Challenge")
page = st.sidebar.radio("Go to", ["🏠 Home", "💡 Daily Motivation", "🧠 Mindset Quiz", "📊 Your Results", "📓 Mindset Journal"])

# -------------------- Home --------------------
if page == "🏠 Home":
    st.title("🌱 Growth Mindset Challenge")
    st.markdown("""
    Welcome to the Growth Mindset Challenge app!  
    This app is designed to help you:
    - Understand what a growth mindset is
    - Track your mindset habits
    - Reflect through journaling
    - Stay motivated daily

    ### What is a Growth Mindset?
    A belief that abilities and intelligence can be developed through dedication and effort.
    """)

# -------------------- Daily Motivation --------------------
elif page == "💡 Daily Motivation":
    st.title("💡 Today's Growth Mindset Quote")
    st.success(random.choice(quotes))

# -------------------- Mindset Quiz --------------------
elif page == "🧠 Mindset Quiz":
    st.title("🧠 Self-Assessment: Growth Mindset")
    st.write("Answer the following questions honestly:")

    scores = []
    for question, is_growth in quiz_questions.items():
        response = st.radio(question, ['Agree', 'Disagree'], key=question)
        if response == 'Agree':
            scores.append(1 if is_growth else 0)
        else:
            scores.append(0 if is_growth else 1)

    if st.button("Get My Score"):
        total = sum(scores)
        percentage = round((total / len(scores)) * 100, 2)
        st.session_state['quiz_score'] = percentage
        st.success(f"Your Growth Mindset Score: {percentage}%")
        if percentage >= 70:
            st.balloons()
            st.markdown("🎉 You're cultivating a strong growth mindset!")
        else:
            st.markdown("✨ Keep learning and reflecting to shift your mindset!")

# -------------------- Results --------------------
elif page == "📊 Your Results":
    st.title("📊 Growth Mindset Score")

    if 'quiz_score' not in st.session_state:
        st.warning("Please take the quiz first!")
    else:
        score = st.session_state['quiz_score']
        st.metric("Your Score", f"{score}%")
        fig, ax = plt.subplots()
        ax.bar(["Growth Mindset"], [score], color="green")
        ax.set_ylim(0, 100)
        st.pyplot(fig)

        if score < 70:
            st.info("📌 Tip: Focus on embracing challenges and seeing effort as growth.")

# -------------------- Journal --------------------
elif page == "📓 Mindset Journal":
    st.title("📓 Reflect in Your Mindset Journal")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = st.text_area("Write about a challenge you faced and what you learned:")

    if 'journal' not in st.session_state:
        st.session_state.journal = []

    if st.button("Save Entry"):
        st.session_state.journal.append({"date": date, "entry": entry})
        st.success("✅ Entry saved!")

    if st.session_state.journal:
        st.markdown("### 📝 Past Entries")
        df = pd.DataFrame(st.session_state.journal)
        st.table(df)

        if st.button("📥 Download Journal"):
            csv = df.to_csv(index=False).encode()
            st.download_button("Download CSV", csv, "growth_journal.csv", "text/csv")
