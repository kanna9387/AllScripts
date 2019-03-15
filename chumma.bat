
:: test


for %%x in (3g2,3gp,aac,m4a) do (
set sourcepath=/data/system/%%~xx
set mainpath=C:\TestContents\BCOTestContents\aacfiles\aac-%%~xx


::
::adb shell mkdir %sourcepath%
::adb push "%mainpath%" "%sourcepath%"

::adb shell rm -rR "%sourcepath%"

adb shell ls %sourcepath%

::For %%j in (%mainpath1%\*.%Ext1%) do (
::adb shell LMPapp play %sourcepath1%/%%~nxj
::)
::adb shell ls %sourcepath%
::For %%j in (%mainpath%\*.%Ext%) do (
::adb shell LMPapp play %sourcepath%/%%~nxj

::)
)
pause