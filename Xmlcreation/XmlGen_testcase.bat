:: This for test purpose
:: Created by Kannan.P

::Creating Folder based on time
echo "Creating Folder"
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DIR="Xmlcreation\%data%"
IF not exist "Xmlcreation\%data%" (md "Xmlcreation\%data%")

:: Arugments for python Script

set fw_version_high_Value=80
set fw_version_low_Value=22
set fw_version_Value=36
set firm_link_Value=https://s3.ap-south-1.amazonaws.com/vood-ota-test/POR_300_BETA/POR_300_REL_36_I688_D687_A689_ADAPTER/alexa.bin


:: wrong link

set firm_link_wrong_Value=https://s3.ap-south-1.amazonaws.com/vood-ota-test/POR_300_BETA/POR_300_ENG_NB26_I660_D654_A665_ADAPTER/alexa1.bin

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_high_Value% %firm_link_Value% >> Xmlcreation\%data%\firmware_download_Por300_T.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_Value% %firm_link_Value% >> Xmlcreation\%data%\firmware_download_Por300_T_org.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_low_Value% %firm_link_Value% >> Xmlcreation\%data%\firmware_download_Por300_T_low.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_low_Value% %firm_link_wrong_Value% >> Xmlcreation\%data%\firmware_download_Por300_T_wrong.xml

pause
