import streamlit as st
import random
from gtts import gTTS
import sqlite3
import os

# ----------------------
# DATABASE
# ----------------------
conn = sqlite3.connect("math_buddy.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    points INTEGER,
    streak INTEGER,
    problems_completed INTEGER,
    difficulty INTEGER
)
""")
conn.commit()

# ----------------------
# SESSION STATE
# ----------------------
state_vars = ['points', 'streak', 'problems_completed', 'difficulty', 'question', 'answer', 'steps', 'hint', 'feedback', 'answered']
for var in state_vars:
    if var not in st.session_state:
        st.session_state[var] = 0 if var in ['points','streak','problems_completed','difficulty'] else '' if var in ['question','hint','feedback'] else []

if 'answered' not in st.session_state: st.session_state.answered = False

# ----------------------
# STYLING
# ----------------------
st.markdown("""
<style>
.stApp { background-color: #FFF3E0; } /* soft pastel background */
.question-card {
    background: #FFECB3;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}
.button-next {
    background-color: #FFD54F;
    color: #333;
    padding: 10px 25px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 18px;
    border: none;
    cursor: pointer;
}
.button-next:hover { background-color: #FFC107; }
.feedback { font-size:20px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# TOPIC SELECTION
# ----------------------
st.title("🧠 Math Buddy - Gamified & Fixed")
topic = st.selectbox("Choose a topic:", ["Addition", "Subtraction", "Multiplication", "Division"])

# ----------------------
# PROBLEM GENERATION
# ----------------------
def generate_problem(topic, difficulty):
    max_val = 10 + difficulty * 5
    a = random.randint(1, max_val)
    b = random.randint(1, max_val)
    
    if topic == "Addition":
        q = f"{a} + {b}"
        ans = a + b
        steps = [f"{a} + {b} = {ans}"]
    elif topic == "Subtraction":
        q = f"{a} - {b}"
        ans = a - b
        steps = [f"{a} - {b} = {ans}"]
    elif topic == "Multiplication":
        q = f"{a} × {b}"
        ans = a * b  # fixed multiplication
        steps = [f"{a} × {b} = {ans}"]
    elif topic == "Division":
        b = max(1, b)
        q = f"{a*b} ÷ {b}"
        ans = a
        steps = [f"{a*b} ÷ {b} = {ans}"]
    hint = "Try breaking the numbers into smaller parts!"
    return q, ans, steps, hint

# ----------------------
# GENERATE NEW PROBLEM ONLY IF NEEDED
# ----------------------
if st.session_state.question == '' or st.session_state.answered:
    q, ans, steps, hint = generate_problem(topic, st.session_state.difficulty)
    st.session_state.question = q
    st.session_state.answer = ans
    st.session_state.steps = steps
    st.session_state.hint = hint
    st.session_state.feedback = ''
    st.session_state.answered = False

# ----------------------
# DISPLAY QUESTION
# ----------------------
st.markdown(f"<div class='question-card'><b>Problem:</b> {st.session_state.question}</div>", unsafe_allow_html=True)
user_input = st.text_input("Your Answer:")

# ----------------------
# SUBMIT ANSWER
# ----------------------
if st.button("Submit Answer") and not st.session_state.answered:
    try:
        if int(user_input) == st.session_state.answer:
            st.session_state.points += 10
            st.session_state.streak += 1
            st.session_state.problems_completed += 1
            st.session_state.feedback = f"✅ Correct! +10⭐ Streak: {st.session_state.streak}🔥"
            st.session_state.answered = True
            st.balloons()
            if st.session_state.problems_completed % 5 == 0:
                st.session_state.difficulty += 1
        else:
            st.session_state.feedback = f"❌ Incorrect. Answer was {st.session_state.answer}."
            st.session_state.streak = 0
            st.session_state.answered = True
    except:
        st.session_state.feedback = "⚠️ Enter a valid number!"

st.markdown(f"<p class='feedback'>{st.session_state.feedback}</p>", unsafe_allow_html=True)

# ----------------------
# NEXT QUESTION
# ----------------------
if st.session_state.answered:
    if st.button("➡️ Next Question"):
        st.session_state.answered = True
        st.session_state.question = ''

# ----------------------
# HINTS & SOLUTIONS
# ----------------------
if st.button("💡 Show Hint"): st.info(st.session_state.hint)
if st.button("📖 Show Steps"): 
    for s in st.session_state.steps: st.write(s)

# ----------------------
# AUDIO READ-ALOUD
# ----------------------
if st.button("🔊 Read Problem Aloud"):
    tts = gTTS(text=st.session_state.question, lang='en')
    tts.save("problem.mp3")
    st.audio("problem.mp3")

# ----------------------
# PROGRESS & ACHIEVEMENTS
# ----------------------
st.markdown(f"<b>Points:</b> {st.session_state.points} ⭐️")
st.markdown(f"<b>Problems Solved:</b> {st.session_state.problems_completed}")
st.markdown(f"<b>Current Streak:</b> {st.session_state.streak} 🔥")

ACHIEVEMENTS = [(50,"Math Novice 🏅"),(100,"Math Apprentice 🥈"),(200,"Math Master 🏆"),(500,"Math Genius 🎖️")]
earned = [name for pts,name in ACHIEVEMENTS if st.session_state.points>=pts]
if earned: st.markdown(f"<b>Achievements:</b> {' | '.join(earned)}")

# ----------------------
# SAVE TO SQLITE
# ----------------------
c.execute("INSERT INTO progress (points, streak, problems_completed, difficulty) VALUES (?,?,?,?)",
          (st.session_state.points, st.session_state.streak, st.session_state.problems_completed, st.session_state.difficulty))
conn.commit()
