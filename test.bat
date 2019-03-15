
set SSID=test
::AndroidWorld
set Passphrase=1234567890
::#IP6pGYS

:: set Security as NONE,WPA-PSK,WPA2-PSK,WEP128,WEP64
set Security=WPA-PSK
:: Enter the WEP key of WEP 128
set WEP128PK=9EA04D743618797CE464445B57
:: Enter the WEP key of WEP 128
set WEP64PK=EE1424E191



adb shell wpa_cli -i wlan0 remove_n 0
adb shell wpa_cli -i wlan0 add_n 0
pause
adb shell wpa_cli -i wlan0 set_n 0 ssid '"%SSID%"'
pause
adb shell wpa_cli -i wlan0 set_n 0 scan_ssid 1
adb shell wpa_cli -i wlan0 set_n 0 key_mgmt %Security%
adb shell wpa_cli -i wlan0 set_n 0 auth_alg OPEN
::adb shell wpa_cli -i wlan0 set_n 0 wep_key0 %WEP64PK%
adb shell wpa_cli -i wlan0 set_n 0 key_mgmt NONE
adb shell wpa_cli -i wlan0 set_n 0 psk '"%Passphrase%"'
adb shell wpa_cli -i wlan0 select_n 0
adb shell wpa_cli -i wlan0 enable_n 0
adb shell wpa_cli -i wlan0 save_c
adb shell wpa_cli -i wlan0 reassociate

adb shell wpa_cli stat
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
