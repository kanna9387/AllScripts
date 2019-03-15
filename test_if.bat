
set SSID=test
set Passphrase=sathish9387

:: set Security as NONE,WPA-PSK,WPA2-PSK,WEP128,WEP64
set Security=WEP128
:: Enter the WEP key of WEP 128
set WEP128PK=9EA04D743618797CE464445B57
:: Enter the WEP key of WEP 128
set WEP64PK=EE1424E191


if %Security% == "WPA2-PSK"(
adb shell wpa_cli -iwlan0 remove_network 0
adb shell wpa_cli -iwlan0 add_network 0
adb shell wpa_cli -iwlan0 set_network 0 ssid "%SSID%"
adb shell wpa_cli -iwlan0 set_network 0 scan_ssid 1
adb shell wpa_cli -iwlan0 set_network 0 key_mgmt %Security%
adb shell wpa_cli -iwlan0 set_network 0 psk "%Passphrase%"
adb shell wpa_cli -iwlan0 select_network 0
adb shell wpa_cli -iwlan0 enable_network 0
adb shell wpa_cli -iwlan0 save_config
adb shell wpa_cli -iwlan0 reassociate

adb shell wpa_cli status
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
)
else if %Security% == "WPA-PSK"(
adb shell wpa_cli -iwlan0 remove_network 0
adb shell wpa_cli -iwlan0 add_network 0
adb shell wpa_cli -iwlan0 set_network 0 ssid "%SSID%"
adb shell wpa_cli -iwlan0 set_network 0 scan_ssid 1
adb shell wpa_cli -iwlan0 set_network 0 key_mgmt %Security%
adb shell wpa_cli -iwlan0 set_network 0 psk "%Passphrase%"
adb shell wpa_cli -iwlan0 select_network 0
adb shell wpa_cli -iwlan0 enable_network 0
adb shell wpa_cli -iwlan0 save_config
adb shell wpa_cli -iwlan0 reassociate

adb shell wpa_cli status
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
)
else if %Security% == "NONE"(
adb shell wpa_cli -iwlan0 remove_network 0
adb shell wpa_cli -iwlan0 add_network 0
adb shell wpa_cli -iwlan0 set_network 0 ssid "%SSID%"
adb shell wpa_cli -iwlan0 set_network 0 scan_ssid 1
adb shell wpa_cli -iwlan0 set_network 0 key_mgmt %Security%
adb shell wpa_cli -iwlan0 select_network 0
adb shell wpa_cli -iwlan0 enable_network 0
adb shell wpa_cli -iwlan0 save_config
adb shell wpa_cli -iwlan0 reassociate

adb shell wpa_cli status
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
) 
else if %Security% == "WEP128"(
adb shell wpa_cli -iwlan0 remove_network 0
adb shell wpa_cli -iwlan0 add_network 0
adb shell wpa_cli -iwlan0 set_network 0 auth_alg OPEN
adb shell wpa_cli -iwlan0 set_network 0 wep_key0 %WEP128PK%
adb shell wpa_cli -iwlan0 set_network 0 key_mgmt NONE
adb shell wpa_cli -iwlan0 set_network 0 mode 0
adb shell wpa_cli -iwlan0 set_network 0 ssid "%SSID%"
adb shell wpa_cli -iwlan0 select_network 0
adb shell wpa_cli -iwlan0 enable_network 0
adb shell wpa_cli -iwlan0 save_config
adb shell wpa_cli -iwlan0 reassociate

adb shell wpa_cli status
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
)  
else %Security% == "WEP64"(
adb shell wpa_cli -iwlan0 remove_network 0
adb shell wpa_cli -iwlan0 add_network 0
adb shell wpa_cli -iwlan0 set_network 0 auth_alg OPEN
adb shell wpa_cli -iwlan0 set_network 0 wep_key0 %WEP64PK%
adb shell wpa_cli -iwlan0 set_network 0 key_mgmt NONE
adb shell wpa_cli -iwlan0 set_network 0 mode 0
adb shell wpa_cli -iwlan0 set_network 0 ssid "%SSID%"
adb shell wpa_cli -iwlan0 select_network 0
adb shell wpa_cli -iwlan0 enable_network 0
adb shell wpa_cli -iwlan0 save_config
adb shell wpa_cli -iwlan0 reassociate

adb shell wpa_cli status
pause

adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
) 