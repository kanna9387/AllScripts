:: ################################################################################
:: ## This batch script is used to rename specific file 						 ##
:: ## 																		   	 ##
:: ## Created by Kannan.P													     ##
:: ################################################################################


::Appending the name in back side

::for %%i in (2*.pdf) do rename %%i %%~ni_diode.pdf

::Appending the name in front side

for %%i in (2*.pdf) do rename %%i diode_%%~ni.pdf

pause