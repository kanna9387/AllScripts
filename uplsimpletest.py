from playsound import playsound
from gtts import gTTS    ##install packge through command 'pip install gTTS"
import time
from pygame import mixer  # ##install packge through command 'pip install pygame"

filepath = "D:\\Testing\\AVS_Automation\\Voices\\"

alexa = filepath+"Alexa.mp3"
tts = gTTS(text="Alexaaa  ", lang='en-us')
tts.save(alexa)

distance = filepath+"distance.mp3"
tts = gTTS(text="How far is Alaska from Vegas", lang='en-us')
tts.save(distance)

timen = filepath+"time.mp3"
tts = gTTS(text="What is the time", lang='en-us')
tts.save(timen)

weather = filepath+"weather.mp3"
tts = gTTS(text="How is the weather in Bengaluru", lang='en-us')
tts.save(weather)

japan = filepath+"japan.mp3"
weather = filepath+"weather.mp3"
tts = gTTS(text="How is the weather in Bengaluru", lang='en-us')
tts.save(japan)

mixer.init()

while True:

    ##Query distance
    mixer.music.load(alexa)
    mixer.music.play()
    time.sleep(1)
    mixer.music.stop()
    mixer.music.load(distance)
    mixer.music.play()
    time.sleep(20)
    mixer.music.stop()

    ##Query time
    mixer.music.load(alexa)
    mixer.music.play()
    time.sleep(1)
    mixer.music.stop()
    mixer.music.load(timen)
    mixer.music.play()
    time.sleep(9)
    mixer.music.stop()

    ##Query Japan Capital
    mixer.music.load(alexa)
    mixer.music.play()
    time.sleep(1)
    mixer.music.stop()
    mixer.music.load(japan)
    mixer.music.play()
    time.sleep(9)
    mixer.music.stop()

    ##Query weather
    mixer.music.load(alexa)
    mixer.music.play()
    time.sleep()
    mixer.music.stop()
    mixer.music.load(weather)
    mixer.music.play()
    time.sleep(20)
    mixer.music.stop()