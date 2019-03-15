
For /L %%i in (1 1 60) do (
mkdir 
For %%j in (Vellai-Pookal.mp3) do (
copy %%j \60\%%i.mp3
echo Files copied as %%i.mp3
)
)
