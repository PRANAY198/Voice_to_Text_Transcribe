import streamlit as st
from main import main
import os
from main import format_timestamp
def main_app():
    st.title("Audio Transcription App")

    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav","aac","mp4"])
    if uploaded_file is not None:
        audio_path = os.path.join("audio_input", uploaded_file.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.audio(uploaded_file, format='audio/wav')

        if st.button("Transcribe"):
            transcript = main(audio_path)
            st.write("Transcription:")
            for utterance in transcript.utterances:
                start_time = format_timestamp(utterance.start)
                end_time = format_timestamp(utterance.end)
                st.write(f"Speaker {utterance.speaker} [{start_time} - {end_time}]: {utterance.text}")

if __name__ == "__main__":
    main_app()