
set Source='/data/system/''
set adb='adb shell'
set path=C:\TestContents\Fileformat\mp3\frequencies\
set Ext=mp3


%adb% mkdir %Source%%Ext%
pause
pause
adb push "%path%" "%Source%%Ext%/"
pause
For %%j in (%path%*.%Ext%) do 
%adb% LMPapp play %Source%%Ext%%Ext%/~%nj.%Ext%


