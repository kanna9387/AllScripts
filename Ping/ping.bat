:: This for test purpose
:: Created by Kannan.P

::Creating Folder based on time
echo "Creating Folder"
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set tim=%time:~0,2%%time:~3,2%%time:~6,2%
set dataa=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set DIR="Ping_report\%dataa%"
IF not exist "Ping_report\%dataa%" (md "Ping_report\%dataa%")

:: Arugments for python Script
set Host_Ip=192.168.0.70

:: Command
python ping.py %Host_Ip% >>"Ping_report\%dataa%\Ping_Report_%Host_Ip%_%data%_%tim%.txt"

:: Send mail using SwitchMail.exe file
SwithMail.exe /s /from "sirenalabstest@gmail.com" /name "ping test" /pass "SirenaLabs@123" /server "smtp.gmail.com" /p "587" /SSL /to "SirenaLabsTest@gmail.com" /rt "sirenalabstest@gmail.com" /sub "ping test result of %Host_Ip%_%data%" /a "Ping_report\%dataa%\Ping_Report_%Host_Ip%_%data%_%tim%.txt" /rr

pause