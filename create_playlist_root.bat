SET FOL=10
For /L %%i in (1 1 %FOL%) do (
::mkdir 
For %%j in (Vellai-Pookal.mp3) do (
copy %%j .\%%i.mp3
echo Files copied as %%i.mp3
)
)
pause