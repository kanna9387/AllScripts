:: This for test purpose
:: Created by Kannan.P

::TTS test
echo "TTS test for Alexa"

rem Song from my music library
python python-tts_test.py "play the song hello by adele from my music library" "play adele from my library.mp3" 
timeout 30
python python-tts_Alexa.py "STOP" "Stop.mp3" 
timeout 20
python python-tts_test.py "Resume" "Resume.mp3" 
timeout 300

rem Album from my music library
python python-tts_test.py "play the album twenty five by adele from my music library" "play twenty five album from my library.mp3"  
timeout 50
python python-tts_test.py "STOP" "Stop.mp3" 
timeout 20
python python-tts_test.py "Resume" "Resume.mp3"  
timeout 40
python python-tts_test.py  "Next" "Next.mp3" 
timeout 70
python python-tts_test.py  "Previous" "Previous.mp3" 
timeout 400

rem playlist compilation from my music library
python python-tts_test.py "play the playlist compilation from my music library" "playlist compilation from my library.mp3"  
timeout 120
python python-tts_test.py "STOP" "Stop.mp3" 
timeout 30
python python-tts_test.py "Resume" "Resume.mp3"  
timeout 70
python python-tts_test.py  "Next" "Next.mp3" 
timeout 60
python python-tts_test.py  "Previous" "Previous.mp3" 
timeout 600

pause
