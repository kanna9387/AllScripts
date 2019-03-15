

for /d %%i in ("*") do (
"C:\Program Files\WinRAR\WinRAR.exe" a -r -df -x*.bat "%%~ni.rar" "%%i"

::del "%%~ni.log"
::del "%%~ni.txt"

)
pause