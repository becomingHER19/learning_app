# utils/asr_tools.py
from pathlib import Path
try:
    import whisper
    HAS_WHISPER = True
except Exception:
    HAS_WHISPER = False

try:
    import speech_recognition as sr
    HAS_SR = True
except Exception:
    HAS_SR = False

WHISPER_MODEL = None

def transcribe_with_whisper(path):
    global WHISPER_MODEL
    if not HAS_WHISPER: return None
    if WHISPER_MODEL is None:
        WHISPER_MODEL = whisper.load_model("tiny")
    res = WHISPER_MODEL.transcribe(str(path))
    return res.get("text","").strip()

def transcribe_with_speechrec(path):
    if not HAS_SR: return None
    r = sr.Recognizer()
    with sr.AudioFile(str(path)) as src:
        audio = r.record(src)
    try:
        return r.recognize_google(audio)
    except Exception:
        return None
