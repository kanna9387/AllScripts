
set SSID=LibreG
set Passphrase=#IP6pGYS

:: set Security as NONE,WPA-PSK,WPA2-PSK,WEP128,WEP64
set Security=WPA-PSK
:: Enter the WEP key of WEP 128
set WEP128PK=9EA04D743618797CE464445B57
:: Enter the WEP key of WEP 128
set WEP64PK=EE1424E191

adb shell

wpa_cli -p /data/misc/wifi/sockets/ -i wlan0

remove_network 0
add_network 0
set_network 0 ssid "%SSID%"
set_network 0 scan_ssid 1
set_network 0 key_mgmt %Security%
set_network 0 psk "%Passphrase%"
select_network 0
enable_network 0
save_config
reassociate

status
pause
quit
pause
adb shell cat /data/misc/wifi/wpa_supplicant.conf
pause
