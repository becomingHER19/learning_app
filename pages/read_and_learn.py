import streamlit as st
import json
import time
from gtts import gTTS
import tempfile
from datetime import date

# --------------------------
# PAGE CONFIG
st.set_page_config(page_title="Read & Learn", layout="wide")

# --------------------------
# SESSION STATE INIT
if "points" not in st.session_state: st.session_state["points"] = 0
if "streak" not in st.session_state: st.session_state["streak"] = 0
if "last_played" not in st.session_state: st.session_state["last_played"] = None
if "dyslexia_mode" not in st.session_state: st.session_state["dyslexia_mode"] = False
if "font" not in st.session_state: st.session_state["font"] = "Arial"
if "bg_color" not in st.session_state: st.session_state["bg_color"] = "#f8f9fa"

# --------------------------
# STYLING FUNCTION
def apply_styles():
    font = st.session_state["font"]
    bg = st.session_state["bg_color"]
    st.markdown(f"""
    <style>
    .stApp {{
        background: {bg};
        font-family: '{font}', sans-serif;
        min-height: 100vh;
        color: #212529;
    }}
    .highlight {{ background-color: #fff176; border-radius: 5px; padding: 2px 4px; }}
    .vocab-box {{ background-color: #e0f7fa; padding: 10px; border-radius: 8px; margin-top: 10px; }}
    .story-box {{ padding: 20px; border-radius: 10px; background-color: #ffffffcc; }}
    .points-box {{ background-color: #c8e6c9; padding: 8px; border-radius: 5px; }}
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# --------------------------
# DYSLEXIA MODE & CUSTOMIZATION
with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state["dyslexia_mode"] = st.checkbox("Dyslexia-Friendly Mode", value=st.session_state["dyslexia_mode"])
    if st.session_state["dyslexia_mode"]:
        st.session_state["font"] = st.selectbox("Choose Font", ["OpenDyslexic", "Comic Sans MS", "Arial", "Verdana"])
        st.session_state["bg_color"] = st.color_picker("Background Color", value=st.session_state["bg_color"])
        apply_styles()

# --------------------------
# LOAD STORIES
try:
    with open("stories.json", "r") as f:
        stories = json.load(f)
except FileNotFoundError:
    st.error("❌ stories.json not found! Make sure it exists in the same folder.")
    stories = {}

# --------------------------
# STORY SELECTION
st.title("📖 Read & Learn")
story_title = st.selectbox("Choose a story:", list(stories.keys()) if stories else [])
if story_title:
    story_text = stories[story_title]
    story_words = story_text.split()
    
    st.markdown('<div class="story-box">', unsafe_allow_html=True)
    story_placeholder = st.empty()
    story_placeholder.markdown(story_text)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------
    # READ ALOUD FUNCTION
    def read_aloud(text):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang="en")
        tts.save(temp_file.name)
        return temp_file.name

    if st.button("🔊 Read Aloud"):
        audio_file = read_aloud(story_text)
        st.audio(audio_file, format="audio/mp3")
        # Live highlighting
        for i, word in enumerate(story_words):
            highlighted = " ".join([f"<span class='highlight'>{w}</span>" if j==i else w for j,w in enumerate(story_words)])
            story_placeholder.markdown(highlighted, unsafe_allow_html=True)
            time.sleep(0.3)
        story_placeholder.markdown(story_text, unsafe_allow_html=True)

    # --------------------------
    # VOCABULARY PANEL
    st.write("📚 Click a word to see its meaning, synonym, antonym, and example.")
    word_click = st.text_input("Enter word to look up:", "")
    if word_click:
        # Static example dictionary
        vocab = {
            "magic": {"meaning":"Something supernatural", "synonym":"sorcery", "antonym":"science", "example":"The magician performed magic tricks."},
            "clever":{"meaning":"Quick-witted", "synonym":"smart","antonym":"dull","example":"She is a clever student."}
        }
        word_info = vocab.get(word_click.lower(), {"meaning":"N/A","synonym":"N/A","antonym":"N/A","example":"N/A"})
        st.markdown(f"""
        <div class='vocab-box'>
        <b>Word:</b> {word_click}<br>
        <b>Meaning:</b> {word_info['meaning']}<br>
        <b>Synonym:</b> {word_info['synonym']}<br>
        <b>Antonym:</b> {word_info['antonym']}<br>
        <b>Example:</b> {word_info['example']}<br>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------
    # GAMIFICATION
    st.markdown(f"<div class='points-box'>🎯 Points: {st.session_state['points']} | 🔥 Streak: {st.session_state['streak']} days</div>", unsafe_allow_html=True)
    if st.button("I finished reading!"):
        st.session_state["points"] += len(story_words)
        today = date.today()
        if st.session_state["last_played"] != today:
            st.session_state["streak"] += 1
            st.session_state["last_played"] = today
        st.balloons()
        st.success(f"You earned points! Total: {st.session_state['points']} | Streak: {st.session_state['streak']} days")
