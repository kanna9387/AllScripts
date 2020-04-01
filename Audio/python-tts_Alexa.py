from gtts import gTTS
from playsound import playsound
import os
import sys

argumentList = sys.argv 
print argumentList 
# define variables
#s = sys.argv[1]
s = 'Alexa'+","+'Alexa'
file =  Alexaalexa.mp3

print s
print file

# initialize tts, create mp3 and play
tts = gTTS(s, 'en')
tts.save(file)
playsound(file)
