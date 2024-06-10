import streamlit as st
import assemblyai as aai
import os

aai.settings.api_key = "7df7de372b53408b87adad8f4866456f"

def transcribe_audio(audio_path):
    upload_url = upload_audio_to_assemblyai(audio_path)
    config = aai.TranscriptionConfig(
        speaker_labels=True
    )
    transcript = aai.Transcriber().transcribe(upload_url, config)

    return transcript

def upload_audio_to_assemblyai(audio_path):
    return audio_path

def format_timestamp(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    return f"{int(hours):02}:{int(minutes % 60):02}:{int(seconds % 60):02}"

def main(audio_path):
    audio_output_dir = "audio_input"
    text_output_dir = "text_output"
    os.makedirs(audio_output_dir, exist_ok=True)
    os.makedirs(text_output_dir, exist_ok=True)
    output_audio_file = os.path.join(audio_output_dir, os.path.basename(audio_path))
    output_text_file = os.path.join(text_output_dir, os.path.splitext(os.path.basename(audio_path))[0] + ".txt")
    transcript = transcribe_audio(audio_path)

# Save the transcription to a file
    with open(output_text_file, 'w') as f:
        for utterance in transcript.utterances:
            start_time = format_timestamp(utterance.start)
            end_time = format_timestamp(utterance.end)
            f.write(f"Speaker {utterance.speaker} [{start_time} - {end_time}]: {utterance.text}\n")
    st.success(f"Transcription saved to: {output_text_file}")
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    with open(output_audio_file, "wb") as f:
        f.write(audio_data)
    st.success(f"Audio saved to: {output_audio_file}")

    return transcript
