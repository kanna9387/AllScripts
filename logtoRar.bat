:: ##########################################################################
:: This batch script is used to rar the .log files and delete the log file.##
:: This is used for cleanup purpose										   ##
:: Created by Kannan.P													   ##
:: ##########################################################################


for %%i in (*.log) do (
"C:\Program Files\WinRAR\WinRAR.exe" a -r %%~ni.rar %%~ni.log

del %%~ni.log

)
pause