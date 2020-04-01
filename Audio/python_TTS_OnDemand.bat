:: This for test purpose
:: Created by Kannan.P

::TTS test
echo "TTS test for Alexa"

rem Song from saavn
python python-tts_test.py "play arjit singh song from saavn" "play arjit singh song from saavn.mp3" 
timeout 36
python python-tts_test.py "STOP" "Stop.mp3" 
timeout 22
python python-tts_test.py "Resume" "Resume.mp3" 
timeout 34
python python-tts_test.py "STOP" "Stop.mp3" 
timeout 60


rem Album from saavn
python python-tts_test.py "play the album three idiots on saavn" "play the album three idiots saavn.mp3"  
timeout 300
python python-tts_test.py "Next" "Next.mp3" 
timeout 50
python python-tts_test.py "Next" "Next.mp3" 
timeout 56
python python-tts_test.py  "Previous" "Previous.mp3"
timeout 45
python python-tts_test.py "skip" "skip.mp3"  
timeout 40
python python-tts_test.py  "Stop" "Stop.mp3" 
timeout 40


rem song from saavn
python python-tts_test.py "play songs by lucky ali on saavn" "play songs by lucky ali on saavn.mp3"  
timeout 30
python python-tts_test.py "Next" "Next.mp3" 
timeout 23
python python-tts_test.py  "Previous" "Previous.mp3"
timeout 25
python python-tts_test.py "skip" "skip.mp3" 
timeout 23
python python-tts_test.py  "Stop" "Stop.mp3" 
timeout 132


rem song from saavn
python python-tts_test.py "play classical music on saavn" "play classical music on saavn.mp3"  
timeout 45
python python-tts_test.py  "Stop" "Stop.mp3" 
timeout 26
python python-tts_test.py "Resume" "Resume.mp3" 
timeout 25
python python-tts_test.py  "Stop" "Stop.mp3" 
timeout 25


rem song from saavn
python python-tts_test.py "play the song zoobi doobi on saavn" "play the song zoobi doobi on saavn.mp3"  
timeout 370

rem song from saavn
python python-tts_test.py "play the playlist bollywood workout on saavn" "playlist bollywood workout on saavn.mp3"  
timeout 30
python python-tts_test.py "Next" "Next.mp3" 
timeout 26
python python-tts_test.py  "Previous" "Previous.mp3"
timeout 20
pause
