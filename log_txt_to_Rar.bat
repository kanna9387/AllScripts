:: ###################################################################################
:: This batch script is used to rar the .log & .txt files and delete the log file.	##
:: This is used for cleanup purpose										   			##
:: Created by Kannan.P													   			##
:: ###################################################################################



for %%i in (*.log, *.txt) do (
"C:\Program Files\WinRAR\WinRAR.exe" a -r "%%~ni.rar" "%%i"

del "%%~ni.log"
del "%%~ni.txt"

)
pause