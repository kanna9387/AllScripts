:: This for test purpose
:: Created by Kannan.P

::Creating Folder based on time
echo "Creating Folder"
set data=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DIR="Xmlcreation\Spk\%data%"
IF not exist "Xmlcreation\Spk\%data%" (md "Xmlcreation\Spk\%data%")

:: Arugments for python Script

set fw_version_high_Value=180
set fw_version_low_Value=22
set fw_version_Value=73
set firm_link_Value=https://s3.ap-south-1.amazonaws.com/vood-ota-test/VOOD-LC_ENG_Spk/VOOD_LC_ENG_NB73_I688_D687_A700_SPEAKER/alexa.bin


:: wrong link

set firm_link_wrong_Value=https://s3.ap-south-1.amazonaws.com/vood-ota-test/VOOD_LC_ENG_NB69_I660_D666_A669_SPEAKER/alexa1.bin

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_high_Value% %firm_link_Value% >> %DIR%\firmware_download_Spk_T.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_Value% %firm_link_Value% >> %DIR%\firmware_download_Spk_T_org.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_low_Value% %firm_link_Value% >> %DIR%\firmware_download_Spk_T_low.xml

echo Proper value test case
python xmlcreation_Sample1.py %fw_version_low_Value% %firm_link_wrong_Value% >> %DIR%\firmware_download_Spk_T_wrong.xml

pause
