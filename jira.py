import pyttsx3
import pyautogui
from vosk import Model, KaldiRecognizer
import pyaudio
import json

engine = pyttsx3.init()
engine.setProperty('rate', 150)

wake_words = ["hey gira", "bonjour gira", "salut gira"]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    model = Model("./models/vosk-model-small-fr-0.22")
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192, input_device_index=3)
    stream.start_stream()

    print("En attente de l'activation...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            print(f"Texte détecté : {text}")
            if any(wake_word in text for wake_word in wake_words):
                speak("Oui, je vous écoute.")
                print("Activation détectée!")
                listen_for_command(stream, recognizer)

def listen_for_command(stream, recognizer):
    print("En attente de la commande...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").lower()
            print(f"Commande reçue : {command}")
            execute_command(command)
            break

def execute_command(command):
    if "ouvre navigateur" in command:
        speak("Ouverture du navigateur.")
        pyautogui.hotkey('ctrl', 't')
    elif "ferme la fenêtre" in command:
        speak("Fermeture de la fenêtre.")
        pyautogui.hotkey('alt', 'f4')
    else:
        speak("Commande non reconnue.")

listen_for_wake_word()