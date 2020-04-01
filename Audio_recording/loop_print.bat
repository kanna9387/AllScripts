:: This for test purpose
:: Created by Kannan.P

::Creating Folder based on time
::echo "Creating Folder"

::set DIR="Recording\%data%"
::IF not exist "Recording\%data%" (md "Recording\%data%")

:: Arugments for python Script

set hr=%time:~0,2%
if "%hr:~0,1%" equ " " set hr=0%hr:~1,1%
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%hr%%time:~3,2%%time:~6,2%


@echo off
SETLOCAL
SET /A "index = 1"
SET /A "count = 1000"

:while
if %index% leq %count% (

set outputfilename=output_%data%
echo Filename is %outputfilename%_%index%.wav
timeout 10
   echo The Recorded of index is %index%
   SET /A "index = index + 1"
   goto :while
)



pause