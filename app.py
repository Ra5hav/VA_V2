import speech_recognition as sr
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play, VoiceSettings
import streamlit as st

# 🔐 API Keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

# 🔧 Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 🎤 Voice recognition
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# 💬 Send prompt to ChatGPT
def ask_chatgpt(prompt):
    print("🤖 Thinking...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    print(f"🤖 GPT says: {answer}")
    return answer

# 🔊 Speak response with ElevenLabs
def speak(text):
    audio = eleven_client.generate(
        text=text,
        voice="Rachel",  # You can change this to any voice you have access to
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.7, similarity_boost=0.75)
    )
    play(audio)

# 🚀 Main loop
def main():
    while True:
        query = listen().strip()
        if query.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting. Have a nice day!")
            break
        if query:
            response = ask_chatgpt(query)
            speak(response)

if __name__ == "__main__":
    main()
