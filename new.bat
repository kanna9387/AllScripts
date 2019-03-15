@Echo off

adb shell wpa_cli -iwlan0 scan
pause
adb shell wpa_cli -iwlan0 scan_results > log.txt



Set _File=log.txt
Set /a _Lines=0
For /f %%j in ('Type %_File%^|Find "" /v /c') Do Set /a _Lines=%%j
Echo %_File% has %_Lines% lines.
Set /a Final=%_Lines%-1
Echo Total APs are scanned is %Final%