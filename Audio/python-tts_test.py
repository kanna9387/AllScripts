from gtts import gTTS
from playsound import playsound
import os
import sys

argumentList = sys.argv 
print argumentList 
# define variables
#s = sys.argv[1]
s = sys.argv[1]
file = sys.argv[2]

print s
print file

# initialize tts, create mp3 and play
tts = gTTS(s, 'en')
tts.save(file)
playsound(file)
