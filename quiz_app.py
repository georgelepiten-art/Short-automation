import streamlit as st
from moviepy.editor import *
from gtts import gTTS
import os

st.set_page_config(page_title="Quiz Shorts Maker", layout="centered")
st.title("🎬 Auto Quiz Short Generator")

# --- INPUT FIELDS ---
question = st.text_input("🧮 Enter your question (e.g., 12 + 8 = ?)")
col1, col2 = st.columns(2)
with col1:
    choice_A = st.text_input("A:")
    choice_B = st.text_input("B:")
with col2:
    choice_C = st.text_input("C:")
    choice_D = st.text_input("D:")

correct = st.selectbox("✅ Select correct answer:", ["A", "B", "C", "D"])

# --- BUTTON ---
if st.button("🎥 Generate Video"):
    st.info("⏳ Generating your quiz short... please wait 30–60 seconds.")

    countdown_seconds = 10
    output_name = "quiz_output.mp4"

    # === 1. Black background ===
    background = ColorClip(size=(720, 1280), color=(0, 0, 0)).set_duration(countdown_seconds + 4)

    # === 2. Question text ===
    question_clip = TextClip(
        question, fontsize=70, color='white', font="Arial-Bold"
    ).set_position(("center", "center")).set_duration(background.duration)

    # === 3. Choices ===
    lines = {
        "A": f"A. {choice_A}",
        "B": f"B. {choice_B}",
        "C": f"C. {choice_C}",
        "D": f"D. {choice_D}"
    }
    y_start, spacing = 800, 100
    choices = []
    for i, key in enumerate(["A", "B", "C", "D"]):
        txt = TextClip(lines[key], fontsize=55, color='white', font="Arial-Bold")
        txt = txt.set_position(("center", y_start + i * spacing)).set_duration(countdown_seconds)
        choices.append(txt)

    # === 4. Highlight correct ===
    highlights = []
    for i, key in enumerate(["A", "B", "C", "D"]):
        color = "green" if key == correct else "white"
        txt = TextClip(lines[key], fontsize=55, color=color, font="Arial-Bold")
        txt = txt.set_position(("center", y_start + i * spacing)).set_duration(2).set_start(countdown_seconds)
        highlights.append(txt)

    # === 5. Countdown ===
    countdowns = []
    for i in range(countdown_seconds, 0, -1):
        num = TextClip(str(i), fontsize=100, color='red', font="Arial-Bold")
        num = num.set_duration(1).set_position(('right', 'top')).set_start(countdown_seconds - i)
        countdowns.append(num)
    countdown = concatenate_videoclips(countdowns)

    # === 6. "Correct Answer!" text ===
    correct_text = TextClip("✅ Correct Answer!", fontsize=80, color='green', font="Arial-Bold")
    correct_text = correct_text.set_duration(1.5).fadein(0.5).set_start(countdown_seconds)
    correct_text = correct_text.set_position(("center", y_start - 150))

    # === 7. Text-to-speech ===
    tts_text = f"{question}. A. {choice_A}. B. {choice_B}. C. {choice_C}. D. {choice_D}."
    tts = gTTS(tts_text, lang='en')
    tts.save("voice.mp3")
    voice_audio = AudioFileClip("voice.mp3")

    # === 8. Combine everything ===
    clips = [background, question_clip, countdown, correct_text] + choices + highlights
    final = CompositeVideoClip(clips).set_audio(voice_audio)

    # === 9. Export video ===
    final.write_videofile(output_name, fps=30)

    st.success("✅ Done! Your video is ready below:")
    st.video(output_name)

    st.markdown("📂 Saved in your Pydroid folder as `quiz_output.mp4`")