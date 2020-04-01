:: This for test purpose
:: Created by Kannan.P

::Creating Folder based on time
echo "Creating Folder"
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
::set DIR="Recording\%data%"
::IF not exist "Recording\%data%" (md "Recording\%data%")

:: Arugments for python Script

set outputfilename=output_%data%.wav
set duration=60
::set outputpath=Recording\%data%

python Audio_Record_new.py "%outputfilename%" %duration%

::python Audio_Record.py %outputfilename% Recording\%data%


pause