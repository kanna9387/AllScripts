::set ip=10.0.9.176
::set port=23
::%exepath% /TELNET %%i %port%
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

set exepath="C:\Users\kannan\AppData\Local\VanDyke Software\Clients\SecureCRT.exe"
set Scriptname=D:\MultiSessionsSend.py

FOR /L %%i in (1,1,10) do ( 

%exepath% /SCRIPT "%Scriptname%"


TIMEOUT /t 900

)

pause