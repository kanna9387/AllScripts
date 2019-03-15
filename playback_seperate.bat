
:: test
set Ext=wav
set sourcepath=/data/system/wav/24bit
set mainpath=C:\TestContents\Fileformat\wav\24bit\Mono

::
adb shell mkdir %sourcepath%
adb push "%mainpath%" "%sourcepath%"
::adb shell mkdir %sourcepath1%
::adb push "%mainpath1%" "%sourcepath1%"

::adb shell rm -rR "%sourcepath%"

adb shell ls %sourcepath%

For %%j in ("%mainpath%\*.%Ext%") do (
adb shell LMPapp play "%sourcepath%/%%~nxj"

)

pause