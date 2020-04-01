:: This for test purpose
:: Created by Kannan.P

::TTS test
echo "TTS test for Alexa"
python python-tts_test.py  "loop on" "loopon.mp3"
timeout 10
@echo off
SET /A "index = 1"
SET /A "count = 10000"

:while
if %index% leq %count% (
python python-tts_test.py  "Next" "Next.mp3"
timeout 3
   echo The value of index is %index%
   SET /A "index = index + 1"
   goto :while
)
pause
