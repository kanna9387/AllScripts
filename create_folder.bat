SET FOL=60

mkdir %FOL%
For /L %%i in (1 1 %FOL%) do (
For %%j in (Vellai-Pookal.mp3) do (
copy %%j \%FOL%\%%i.mp3
echo Files copied as %%i.mp3
)
)
