
:: test
set Ext=aac
set sourcepath=/data/system/%Ext%
set mainpath=C:\TestContents\BCOTestContents\aacfiles\aac-aac

::
adb shell mkdir %sourcepath%
adb push "%mainpath%" "%sourcepath%"

::adb shell rm -rR "%sourcepath%"

adb shell ls "%sourcepath%"

For %%j in (%mainpath%\*.%Ext%) do (
adb shell LMPapp play /data/system/%Ext%/%%~nxj

)
pause