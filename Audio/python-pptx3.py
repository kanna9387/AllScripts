import pyttsx3
import time
engine = pyttsx3.init()
engine.say('Alexa,')
time.sleep(6)
engine.say('what is the time')
engine.runAndWait()