'''
API Description :PCTT for WIFI Network Scan, Wifi Network Connection, Communication With Module over TCP
Version: V1.0
Company: LibreWireless Technologies

API Details:
1) ScanWifi
Usage:     ScanWifi("Wifi [Prefix / Name] to which the PC / Laptop has to be connected")  

If True:     Returns   (WifiSSID, (List of WiFi and  Signal Strength))  
If False:    Returns   (False,"Could Not Find WiFi With Prefix / Name  <WiFi SSID>")

2) ConnectToWifi
Usage:   ConnectToWifi("Wifi [Prefix / Name] to which the PC / Laptop has to be connected")

If True:     Returns   (True, 'Laptop Connected To <WiFi SSID>')  
If False:    Returns   (False, 'Could not find wifi with prefix <WiFi SSID>') if ScanToWiFi was failed 
   False:    Returns   (False, 'Could Not Connect Laptop To <WiFi SSID>') if Profiling of WiFi failed


3) ConnectToDevice
Usage:    ConnectToDevice("IP of Device For Tcp Connection",PortNumber<Int>)

If True:  Returns (True,"Connected to <IP of Device>")
   False: Returns (False, 'Socket Connection Exception!!!')

'''

import time        
import sys        
import socket        
import os
import subprocess 
import struct        
import math        
#import statistics
#import numpy as np        
s=""        
connection_status=0        
f=""        
store_mic_data=[]
maximum_sample_value=32768.0        
sample_size=4000


def AddNetworkProfile(ssid):
	fp =open("WiFi_Profile_Template.xml",'r')
	lines = fp.read()
	fp.close()
	ssid_hex_temp = []
	for h in list(ssid):
		ssid_hex_temp.append((hex(ord(h))[-2:].upper()))
		
	ssid_hex = "".join(ssid_hex_temp)
	finalLines1 = lines.replace("SSID_TEMPLATE",ssid)
	finalLines = finalLines1.replace("HEX_TEMPLATE",ssid_hex)
	curPath = os.getcwd()
	fp = open("WiFi_Profile.xml","w")
	fp.write(finalLines)
	fp.close()
	os.system("netsh wlan add profile filename="+curPath+"\WiFi_Profile.xml")
	
def ScanWifi(ssid_prefix):

        global ssid
        ret = subprocess.Popen("netsh wlan show all",stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out,err = ret.communicate()
        SSID_list1 = []
        ssidlist = out.split("\n")
        for line in ssidlist:
		if "SSID" in line and ssid_prefix in line:
			strength = ssidlist[ssidlist.index(line)+5]
			SSID_list1.append(line)
			SSID_list1.append(strength)
	SSID_list = {}
	for i in SSID_list1:
		if "%" in i:
			ind = SSID_list1.index(i)
			s = SSID_list1[ind-1].split(":")[1].strip()
			per =  SSID_list1[ind].split(":")[1].strip()
			SSID_list[s] = per
	try:
		topStrength = sorted(SSID_list.items(), key=lambda x: x[1])[-1]
		ssid = topStrength[0]
		return ssid,topStrength
		
	except:

		return False,"Could Not Find WiFi With Prefix / Name "+ssid_prefix
def ConnectToWifi(prefix, retries=8):        
	global s        
	global connection_status        
	if(retries<0):        
		return False, "Timeout"        
	ssid,ts = ScanWifi(prefix)
	if ssid == False:
		return False,ts
	print "Connecting to "+ssid
        try:        
		ret1 = subprocess.Popen('netsh wlan connect ssid="'+str(ssid)+'" name="'+str(ssid)+'"',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		out,err = ret1.communicate()
		time.sleep(5)
		if "successfully" not in out:
			print "Could not connect laptop to "+ssid
			print"Trying to create new profile for"+ssid
			AddNetworkProfile(ssid)
			ConnectToWifi(prefix, retries-1)
		begin=time.time()        
		try:        
			if(connection_status==1):        
				connection_status=0        
				s.close()        
		except Exception, e:        
			print(e)
		while((time.time()-begin)<10):        
			ret3 = subprocess.Popen("Netsh WLAN show interfaces",stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			st,errr = ret3.communicate()
		        if(ssid in st):
				print "Connected..."
				return True,"Laptop Connected To "+ssid        
		        time.sleep(0.1)        
		print("Error")        
		return False,"Could Not Connect Laptop To "+ssid        
	except Exception, e:        
		print(e)        
		return False,e

def ConnectToDevice(TCP_IP, TCP_PORT):
	global s        
	global connection_status        
	try:        
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
		s.settimeout(2)        
		s.connect((TCP_IP, TCP_PORT))
		s.setblocking(0)        	
		connection_status=1        
		print("connected")        
		return True,"Connected to "+TCP_IP        
	except Exception, e:
		print (e)
		return False,"Socket Connection Exception!!!"
def receive_reply(expected_reply="", timeout=10):
	global connection_status        
	global s
	global mic_test
	global mic_test_type
	global f
	begin_time=time.time()        
        while((time.time()-begin_time)<timeout):                
		try:        
                    st=s.recv(1000)        
                    if(len(st)>0):        
                        if(len(st)<100):        
                            print("DUT REPLY:''"+st+"''")
                        if(expected_reply==""):
                            return True, st        
                        if(expected_reply in st or st in expected_reply):
                            return True, st        
		except:        
                    time.sleep(0.001)        		
                    pass
        return False        
	
def receive_mic_data(bytes=384000, timeout=20):
    mic_data=""        
    received_bytes=0        
    begin=time.time()        
    while(received_bytes<bytes and (time.time()-begin)<timeout):
        try:        
            st=s.recv(10000)
            if(len(st)>0):
                mic_data=mic_data+st
                received_bytes=len(mic_data)
                print("Received "+str(received_bytes)+" bytes")        
        except:        
			time.sleep(0.01)        
			pass        
    return mic_data[:bytes]        
def calculate_mic_power(data):        
	mic_power=[]        
	try:        
		print(len(data))
		for i in range(len(data)/sample_size):        
			#sample_data=(np.array(data[i*sample_size:(i+1)*sample_size]))/maximum_sample_value        
			sample_data=0.0        
			for sample in list(data[i*sample_size:(i+1)*sample_size]):        
				sample=sample[0]        
				sample_data=sample_data+((sample/maximum_sample_value)*(sample/maximum_sample_value))
			mic_power.append(20*math.log10(math.sqrt(sample_data/sample_size)))        
		#mic_power=statistics.median(mic_power)        
		mic_power.sort()        
		mic_power=mic_power[len(mic_power)/2]
	except Exception, e:        
		print(e)        
		mic_power=20*math.log10(1.0/maximum_sample_value)
	return mic_power        
def save_mic_data(filename):        
	global mic_data        
	try:
		f=open(filename, "wb")
		f.write(mic_data)        
		f.close()        
		return True        
	except Exception, e:        
		print(e)        
		return False         
def send_command(command):        
	try:        
		s.send(command)        
		return True        
	except Exception, e:        
		print(e)        
		return False        
def check_shared_mics(m1, m2):        
	if(len(m1)!=len(m2)):        
		return False, "Error"        
	j=0        
	for i in range(len(m1)):        
		if(m1[i]==m2[i]):        
			j=j+1        
	return True, (100.0*j)/len(m1)        
def verify_mics(minimum_mic_data=960000, timeout=20):        
	global mic_data        
	try:        
		send_command("LFT_MFT_Start")        
		status=receive_reply("LFT_MFT_Start_Done")        
		if(status[0]==False):        
			return False, "Error Starting Mic Test"        
		send_command("LFT_MFT_M123")        
		status=receive_reply("OK")        
		mic_data=receive_mic_data(minimum_mic_data, timeout)        
		send_command("LFT_MFT_M123_END")        
		send_command("LFT_MFT_Stop")        
		if(len(mic_data)!=minimum_mic_data):        
			return False, "Could not receive minimum number of mic samples"        
		raw_mic_data=[]        
		for i in range(0, len(mic_data)/2):        
			raw_mic_data.append(struct.unpack("<h", mic_data[i*2:(i*2)+2]))        
		mic_samples=list(raw_mic_data)        
		mic_status={}        
		mic_status["Mic1 Power"]=calculate_mic_power(mic_samples[0::3])        
		mic_status["Mic2 Power"]=calculate_mic_power(mic_samples[1::3])        
		mic_status["Mic3 Power"]=calculate_mic_power(mic_samples[2::3])        
		status=check_shared_mics(mic_samples[1::3], mic_samples[2::3])
		mic_status["Shared Mic"]=status        
		return True, mic_status
	except Exception, e:        
		print(e)        
		return False, str(e)        
		
