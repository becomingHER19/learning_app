import streamlit as st
import pyttsx3
import difflib
import tempfile
import speech_recognition as sr
import time
import json
import phonetics
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np
import av
import soundfile as sf

# ---------------------------
# PAGE CONFIG
st.set_page_config(page_title="Read & Learn", layout="centered")

# ---------------------------
# STYLING
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8f9fa, #e3f2fd);
    min-height: 100vh;
    color: #212529;
    font-family: 'Poppins', sans-serif;
}
.highlight { background-color: #fff176; border-radius: 5px; padding: 2px 4px; }
.correct { background-color: #c8e6c9; border-radius: 5px; padding: 2px 4px; }
.skipped { background-color: #ffcdd2; border-radius: 5px; padding: 2px 4px; }
.extra { background-color: #ffe082; border-radius: 5px; padding: 2px 4px; }
.feedback { background-color: #e0f7fa; padding: 10px; border-radius: 8px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD STORIES
try:
    with open("stories.json", "r") as f:
        stories = json.load(f)
except FileNotFoundError:
    st.error("❌ stories.json not found! Please make sure it exists in the same folder.")
    stories = {}

# ---------------------------
# AGE-BASED STORY SUGGESTIONS
st.title("📖 Read & Learn")
age = st.number_input("Enter your age:", min_value=3, max_value=18, value=8)

def suggest_stories(age):
    suggested = []
    for title in stories:
        if age <= 6 and "Magic" in title:
            suggested.append(title)
        elif 7 <= age <= 10 and "Clever" in title:
            suggested.append(title)
        elif age > 10:
            suggested.append(title)
    return suggested or list(stories.keys())

suggested_stories = suggest_stories(age)
st.info(f"🎯 Suggested stories for your age: {', '.join(suggested_stories)}")

# ---------------------------
# STORY SELECTION
story_title = st.selectbox("Choose a story:", list(stories.keys()) if stories else [])
if story_title:
    story_text = stories[story_title]
    st.write("### 🧩 Story")
    st.write(story_text)

    story_words = story_text.split()
    highlight_placeholder = st.empty()

    # ---------------------------
    # Create audio file
    def create_audio(text):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='en')
        tts.save(temp_file.name)
        return temp_file.name

    # ---------------------------
    # Gamification variables
    if "points" not in st.session_state: st.session_state["points"] = 0
    if "streak" not in st.session_state: st.session_state["streak"] = 0
    if "last_played" not in st.session_state: st.session_state["last_played"] = None

    # ---------------------------
    # Read aloud
    if st.button("🔊 Read Aloud"):
        audio_file = create_audio(story_text)
        st.audio(audio_file, format="audio/mp3")
        for i, word in enumerate(story_words):
            highlighted = " ".join(
                [f"<span class='highlight'>{w}</span>" if j==i else w for j,w in enumerate(story_words)]
            )
            highlight_placeholder.markdown(highlighted, unsafe_allow_html=True)
            time.sleep(0.3)
        highlight_placeholder.empty()

    # ---------------------------
    # Record user reading (cloud-compatible)
    st.write("🎤 Record yourself reading the story")
    duration = st.slider("Recording duration (seconds)", 5, 60, 20)

    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.frames = []
        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            pcm = frame.to_ndarray()
            self.frames.append(pcm)
            return frame

    if st.button("Record Reading"):
        st.info("Recording... Click Stop when finished.")
        webrtc_ctx = webrtc_streamer(key="audio", audio_processor_factory=AudioProcessor, media_stream_constraints={"audio": True, "video": False})

        if webrtc_ctx.audio_processor and webrtc_ctx.state.playing:
            st.warning("Recording in progress...")
        elif webrtc_ctx.audio_processor and not webrtc_ctx.state.playing:
            frames = webrtc_ctx.audio_processor.frames
            if frames:
                audio_data = np.concatenate(frames, axis=1)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                sf.write(temp_file.name, audio_data.T, 48000)
                st.success("Recording saved!")
                st.audio(temp_file.name, format='audio/wav')

                # ---------------------------
                # Transcribe
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_file.name) as source:
                    audio_data = recognizer.record(source)
                    try:
                        child_text = recognizer.recognize_google(audio_data)
                        st.write("🗣️ You said:")
                        st.write(child_text)

                        # ---------------------------
                        # Phonics-aware comparison
                        def check_words(story_words, child_words, threshold=0.8):
                            comparison_html = ""
                            skipped_words, extra_words = [], []
                            i,j = 0,0
                            while i < len(story_words) and j < len(child_words):
                                word_story = story_words[i].lower()
                                word_child = child_words[j].lower()
                                ratio = difflib.SequenceMatcher(None, word_story, word_child).ratio()
                                phonetic_match = phonetics.metaphone(word_story) == phonetics.metaphone(word_child)
                                if ratio > threshold or phonetic_match:
                                    comparison_html += f"<span class='correct'>{story_words[i]} </span>"
                                    i+=1
                                    j+=1
                                else:
                                    comparison_html += f"<span class='skipped'>{story_words[i]} </span>"
                                    skipped_words.append(story_words[i])
                                    i+=1
                            for w in story_words[i:]:
                                comparison_html += f"<span class='skipped'>{w} </span>"
                                skipped_words.append(w)
                            for w in child_words[j:]:
                                comparison_html += f"<span class='extra'>{w} </span>"
                                extra_words.append(w)
                            return comparison_html, skipped_words, extra_words

                        child_words = child_text.split()
                        comparison_html, skipped_words, extra_words = check_words(story_words, child_words)

                        st.markdown("### Word-by-word comparison:")
                        st.markdown(comparison_html, unsafe_allow_html=True)

                        # ---------------------------
                        # Feedback + gamification
                        feedback_msg = "<div class='feedback'><h4>Reading Feedback:</h4>"
                        if skipped_words:
                            feedback_msg += "<b>Skipped/Misread words:</b> " + ", ".join(skipped_words) + "<br>"
                            feedback_msg += "<b>Tip:</b> Practice these words slowly and clearly.<br>"
                        if extra_words:
                            feedback_msg += "<b>Extra words:</b> " + ", ".join(extra_words) + "<br>"
                        if not skipped_words and not extra_words:
                            feedback_msg += "✅ Excellent! You read all words correctly! 🎉"
                            st.balloons()
                            st.session_state["points"] += len(story_words)
                            feedback_msg += f"<br>🎯 Points earned: {st.session_state['points']}"
                        else:
                            st.session_state["points"] += max(0, len(story_words) - len(skipped_words))
                            feedback_msg += f"<br>🎯 Points earned: {st.session_state['points']}"
                        feedback_msg += "</div>"
                        st.markdown(feedback_msg, unsafe_allow_html=True)

                        # Update streak
                        from datetime import date
                        today = date.today()
                        if st.session_state.get("last_played") != today:
                            st.session_state["streak"] += 1
                            st.session_state["last_played"] = today
                        st.info(f"🔥 Current streak: {st.session_state['streak']} days")

                    except Exception as e:
                        st.write("⚠️ Could not transcribe audio. Try again.")
                        st.write(e)

    # ---------------------------
    # Next Story button
    if st.button("➡️ Next Story"):
        story_keys = list(stories.keys())
        idx = story_keys.index(story_title)
        next_idx = (idx+1)%len(story_keys)
        story_title = story_keys[next_idx]
        st.rerun()
