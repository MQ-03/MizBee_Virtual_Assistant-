import pyttsx3
import speech_recognition as sr
import random
from datetime import datetime
import sys
import webbrowser
import openai
from googlesearch import search
import os
import database, sysop, netwrk, gmail
from colorama import Fore

lang = 'en'

openai.api_key = "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" #change ChatGPT api key 

assistant_id = "asst_XE6iV93gn2klrG9PMYD1w0IW" 

def speak(text):
    engine = pyttsx3.init()

    # Check if running on Mac
    if "darwin" in sys.platform:
        # On Mac, set the voice to a suitable one
        voices = engine.getProperty('voices')
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    else:
        # For other platforms, you can keep the existing voice setting
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 160)
"""
def type():

    usrinput = input("Type: ")
    query = usrinput
    print(f"You: {query}")
    database.insert_qry(query)
    return query
"""
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("MizBee: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("MizBee: Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You: {query}")
        database.insert_qry(query)
        return query.lower()
    except sr.UnknownValueError as uve:
        print("MizBee: Sorry, I did not hear your request. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"MizBee: Could not request results from Google Speech Recognition service; {e}")
        return ""
    
def chat_with_gpt3(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
        )
        reply = response['choices'][0]['text'].strip()
        return reply
    except Exception as e:
        return str(e)

def user_ai():
    print(Fore.GREEN)
    database.greet()
    
    while True:
        query = listen()

        if query in ['stop', 'ok bye', 'exit', 'nothing']:
            print("Goodbye!")
            speak("Goodbye!")
            break
        else:
            conversation_history = f"You: {query}\nMizBee:"
            response = chat_with_gpt3(conversation_history)
            database.insert_gpt(response, query)
            print(f"MizBee: {response}")
            speak(response)

def ai_assistant():
    print(Fore.MAGENTA)
    database.greet()
    
    while True:
        query = listen()

        if query in ['stop', 'ok bye', 'exit', 'nothing']:
            print("Goodbye!")
            speak("Goodbye!")
            break
        elif "time" in query:
            print(f"MizBee: The current time is " + datetime.now().strftime("%I:%M:%S %p") )
            speak("The current time is " + datetime.now().strftime("%I:%M:%S %p"))
        elif "date" in query:
            print(f"MizBee: Today's date is " + datetime.now().strftime("%d/%m/%Y"))
            speak("Today's date is " + datetime.now().strftime("%m/%d/%Y"))
        elif query in ['hello', 'Hello' 'hi', 'Hi' 'ok', 'Ok']:
            responses = ["how can i help you?", "tell me ur wish", "what i want to do?"]
            speak(random.choice(responses))
        elif query in ['mizbee', 'MSB', 'bixby', 'miss me']:
            ai_assistant()
        elif "your name" in query:
            speak("My name is MizBee!")
        elif query in ["who are you","What are you"]:
            print("MizBee: I'm MizBee! An AI Assistant.")
            speak("I'm MizBee! An AI Assistant.")
        elif "old" in query:
            speak("I'm like a new born baby!, I'm try learn from this world")
        elif query in ["i am fine", "good", "fine"]:
            speak("Happy to hear that. Anything else sir?")
        elif "joke" in query:
            database.joke()
        elif "weather" in query:
            netwrk.get_weather_forecast()
        elif query in ["what is your purpose","what's your purpose"]:
            speak("I'm here to help you and assist you for some task completion.")
        elif query in ["what you can do"]:
            speak("I can do anything you want.")
        elif "open browser" in query:
            webbrowser.open("https://www.google.com")
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open flipkart" in query:
            webbrowser.open("https://www.flipkart.com")
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open amazon" in query:
            webbrowser.open("https://www.amazon.in")
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open spotify" in query:
            sysop.open_spotify()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open photos" in query:
            sysop.open_photos()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open safari" in query:
            sysop.open_safari()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "open settings" in query:
            sysop.open_settings()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "close safari" in query:
            os.system("pkill -x Safari")
            print("MizBee: Safari is closing..!")
            speak("Safari is closing..!")
        elif "close settings" in query:
            os.system("pkill -x 'System Settings'")
            print("MizBee: System Settings is closing..!")
            speak("System Settings is closed")
        elif "open chrome" in query:
            sysop.open_chrome()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "close chrome" in query:
            os.system("pkill -x 'Google Chrome'")
            print("MizBee: Google Chrome is closing..!")
            speak("Google Chrome is closed")
        elif "open whatsapp" in query:
            sysop.open_whatsapp()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "close whatsapp" in query:
            os.system("pkill -x WhatsApp")
            print("MizBee: WhatsApp is closing..!")
            speak("WhatsApp is closed")
        elif "open terminal" in query:
            sysop.open_terminal()
            print("MizBee: Opening...!")
            speak("opening...")
        elif "check network connection" in query:
            netwrk.get_ping_status()
        elif "ping my database" in query:
            database.database()
        elif "events" in query:
            sysop.cal_events()
        elif query in ["fetch","my data"]:
            database.fetch_data()
        elif query in ['edit user document']: 
            database.edit()
        elif "edit username" in query:
            database.uname_edit()
        elif "create user" in query:
            database.create()
        elif query in ["my mails", "my mail"]:
            gmail.get_mail()
        else:
            conversation_history = f"You: {query}\nMizBee:"
            response = chat_with_gpt3(conversation_history)
            database.insert_gpt(response, query)
            print(f"MizBee: {response}")
            speak(response)
            
if __name__ == "__main__":
    header = """
 ---------------------------------------------------------------------------
| ✺✺✺✺       ✺✺✺✺ ✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺✺✺  ✺✺✺✺✺✺✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺✺✺  |
| ✺✺ ✺✺     ✺✺ ✺✺   ✺✺         ✺✺    ✺✺        ✺✺ ✺✺           ✺✺            |
| ✺✺  ✺✺   ✺✺  ✺✺   ✺✺        ✺✺     ✺✺        ✺✺ ✺✺           ✺✺            |
| ✺✺   ✺✺ ✺✺   ✺✺   ✺✺       ✺✺      ✺✺✺✺✺✺✺✺✺✺✺  ✺✺✺✺✺✺✺✺     ✺✺✺✺✺✺✺✺      |
| ✺✺    ✺✺     ✺✺   ✺✺      ✺✺       ✺✺        ✺✺ ✺✺           ✺✺            | 
| ✺✺           ✺✺   ✺✺     ✺✺        ✺✺        ✺✺ ✺✺           ✺✺            |
| ✺✺           ✺✺ ✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺✺✺  ✺✺✺✺✺✺✺✺✺✺✺✺ ✺✺✺✺✺✺✺✺✺✺✺✺  |
 ----------------------------------------------------------------------------
"""
    print(Fore.CYAN + header)
    print(Fore.BLUE + "\nWelcome MizBee's Authentication Panel\n")
    speak("Welcome MizBee's Authentication Panel")
    database.auth()