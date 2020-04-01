:: This for test purpose
:: Created by Kannan.P

::TTS test
echo "TTS test for Alexa"


python python-tts_test.py "what is the time" "what is the time.mp3" 
timeout 20
python python-tts_test.py "play arjit singh song from saavn" "play arjit singh song from saavn.mp3" 
timeout 20
python python-tts_test.py "Pause" "Pause.mp3" 
timeout 10
python python-tts_test.py "play" "play.mp3"  
timeout 20
python python-tts_test.py "Pause" "Pause.mp3" 
timeout 10
python python-tts_test.py "Resume" "Resume.mp3"  
timeout 20
python python-tts_test.py "Stop" "Stop.mp3" 
timeout 10
python python-tts_test.py "play" "play.mp3"  
timeout 20
python python-tts_test.py  "Next" "Next.mp3" 
timeout 20
python python-tts_test.py  "Next" "Next.mp3" 
timeout 20
python python-tts_test.py  "Next" "Next.mp3" 
timeout 20
python python-tts_test.py  "Next" "Next.mp3" 
timeout 2
python python-tts_test.py  "Previous" "Previous.mp3" 
timeout 20
python python-tts_test.py  "Previous" "Previous.mp3" 
timeout 20
pause
