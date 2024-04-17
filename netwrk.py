import speech_recognition as sr
import main
import subprocess
import pyowm


def get_ping_status():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("MizBee: Please say the IP address or hostname you want to ping.")
        main.speak(f"Please say the IP address or hostname you want to ping.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        target = recognizer.recognize_google(audio)
        #speak("Or please type it here: ")
        #target = input("Or please type it here:")
        print(f"MizBee: Pinging {target}...")
    except sr.UnknownValueError:
        print("MizBee: Sorry, I did not hear the target. Please try again.")
        return
    except sr.RequestError as e:
        print(f"MizBee: Could not request results from Google Speech Recognition service; {e}")
        return
    # Run the ping command
    try:
        result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True, timeout=10)
        if "0% packet loss" in result.stdout:
            print(f"MizBee: {target} is reachable.")
            main.speak(f"{target} is reachable.")
        else:
            print(f"MizBee: {target} is unreachable.")
            main.speak(f"{target} is unreachable.")
    except subprocess.TimeoutExpired:
        print("MizBee: Timeout. The ping request took too long.")
        main.speak("Timeout. The ping request took too long.")
    except Exception as e:
        print(f"MizBee: An error occurred: {e}")
        main.speak(f"An error occurred: {e}")

def get_weather_forecast():
    # Replace "YOUR_API_KEY" with your OpenWeatherMap API key
    owm = pyowm.OWM('your own api key')

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        ask = "Which city do you want the weather forecast for?"
        print(f"MizBee: {ask}")
        main.speak(ask)
        audio = recognizer.listen(source, timeout = 5)

    try:
        place = recognizer.recognize_google(audio)
        if place == sr.UnknownValueError:
            place = input("Type:")
        print(f"MizBee: Fetching weather forecast for {place}...")
    except sr.UnknownValueError:
        print("MizBee: Sorry, I did not hear the target. Please try again.")
        return
    except sr.RequestError as e:
        print(f"MizBee: Could not request results from Google Speech Recognition service; {e}")
        return
    try:
        weather_mgr = owm.weather_manager()
        observation = weather_mgr.weather_at_place(place)
        temperature = observation.weather.temperature("celsius")["temp"]
        humidity = observation.weather.humidity
        wind = observation.weather.wind()
        T = f'Temperature: {temperature}°C'
        H = f"Humidity: {humidity}%"
        W = f'Wind Speed: {wind["speed"]} m/s'
        print(f"{T}\n{H}\n{W}")
        main.speak(T)
        main.speak(H)
        main.speak(W)
    except Exception as e:
        print(f"MizBee: An error occurred while fetching the weather report: {e}")
        main.speak(f"An error occurred while fetching the weather report: {e}")
