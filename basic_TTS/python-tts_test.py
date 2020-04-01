
'''import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate',80)
engine.setProperty('volume', 1.0)
engine.say("Alexa")

engine.setProperty('rate',150)
engine.setProperty('volume', 1.0)
engine.say("what's time")
engine.runAndWait()##
import time
import pyttsx3 

def onStart(): 
	print('starting') 

def onWord(name, location, length): 
	print('word', name, location, length) 

def onEnd(name, completed): 
	print('finishing', name, completed) 

engine = pyttsx3.init() 

engine.connect('started-utterance', onStart) 
engine.connect('started-word', onWord) 
time.sleep(2)
engine.connect('finished-utterance', onEnd) 

sen = 'Alexa, what is time'


engine.say(sen) 
engine.runAndWait() 
# Python program to convert 
# text to speech 
  
# import the required module from text to speech conversion 
import win32com.client 
  
# Calling the Disptach method of the module which  
# interact with Microsoft Speech SDK to speak 
# the given input from the keyboard 
  
speaker = win32com.client.Dispatch("SAPI.SpVoice") 
print "Ctrl+Z then enter to exit."
while 1: 
    print("Enter the word you want to speak it out by computer") 
    s = raw_input()
    speaker.Speak(s) 


import pyttsx
rate_value
engine = pyttsx.init()
engine.setProperty('rate', 120)

voices = engine.getProperty('voices')
for voice in voices:
    print "Using voice:", repr(voice)
    engine.setProperty('voice', voice.id)
    engine.say("Alexa")
    engine.say("what's time")
engine.runAndWait()

from gtts import gTTS
from playsound import playsound
import os

# define variables
s = "escape with plane"
file = "file.mp3"

# initialize tts, create mp3 and play
tts = gTTS(s, 'en')
tts.save(file)
playsound(file)
os.system("mpg123 " + file)
'''

from gtts import gTTS
from playsound import playsound
import os
import sys

argumentList = sys.argv 
print argumentList 
# define variables
#s = sys.argv[1]
s = 'Alexa'+","+sys.argv[1]
file = sys.argv[2]

print s
print file

# initialize tts, create mp3 and play
tts = gTTS(s, 'en')
tts.save(file)
playsound(file)
