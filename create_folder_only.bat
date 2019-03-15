SET FOL=10000
mkdir %FOL%_folders
For /L %%i in (1 1 %FOL%) do (
mkdir %FOL%_folders\%%i
)
)
pause