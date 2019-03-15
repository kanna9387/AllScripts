SET FOL=10
mkdir %FOL%
For /L %%i in (1 1 %FOL%) do (
::mkdir 
For %%j in (Vellai-Pookal.mp3) do (
copy %%j .\%FOL%\%%i.mp3
echo Files copied as \%FOL%\%%i.mp3
)
)
pause