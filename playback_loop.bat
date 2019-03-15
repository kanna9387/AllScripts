
:: test
set Ext=mp3
set sourcepath=/system/bin/
set mainpath=C:\TestContents\Cust\YamahaTestContents\FLAC\dBpoweramp

::
::adb shell mkdir %sourcepath%
::adb push "%mainpath%" "%sourcepath%"

::adb shell rm -rR "%sourcepath%"

adb shell ls "%sourcepath%"
For /L %%i in (0 1 20) do (
::For %%j in (%mainpath%\*.%Ext%) do (
adb shell LMPapp play %sourcepath%/test_mp3_44k_1min.mp3
::)
)
pause