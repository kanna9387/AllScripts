
import serial
import thread
import time
#import crc16
from threading import Thread
from serial import SerialException
import os
from sys import getsizeof
import struct
import Queue
import threading





def LSInBSL(data = ""):
    print " Device is in BSL"

def hostpresent(data = ""):

	print "Host is present"

def CurrentPlayingStatus(data = ""):

	print "Current playing Status under MB 51 %s" %data
	if CurrentPlayingStatus == '0':
		print "Playing Now"
	elif CurrentPlayingStatus == '1':
		print "Stopped the Playback"
	elif CurrentPlayingStatus == '2':
		print "Paused the Playback"
	elif CurrentPlayingStatus == '3':
		print "Connecting status"
	elif CurrentPlayingStatus == '4':
		print "Receiving. Internet is slow"
	elif CurrentPlayingStatus == '5':
		print "Buffering"
	else:
		print "UnKnown status"


def CastStatus(data = ""):

	print "Cast Status under MB 224 %s" %data

def HostVersion(data = ""):

	print "HostVersion under MB 6 %s" %data

def CurrentSource(data = ""):

	print "Current source under MB 50 %s" %data

	global currentaudiosource
	currentaudiosource = data




def IsAllowed (data = "") :
    MID = 11
    commandtype = 2
    status = 0
    isallowed_packet = createlucipacket(MID,commandtype,status,data)
    write_port(isallowed_packet)
    write_port(data)

def Airplay(data = "") :
    MID = 12
    commandtype = 2
    status = 0
    #data = command
    airplycommand_packet = createlucipacket(MID,commandtype,status,data)
    write_port(airplycommand_packet)
    if data != "" :
    	write_port(data)



def DMRSTOP (data = "") :

    MID = 227

    commandtype = 2

    status = 0

    dmrstop_packet = createlucipacket(MID,commandtype,status,"STOP")

    write_port(dmrstop_packet)

    write_port("STOP")



def DMRSTART (data = "") :

    MID = 228

    commandtype = 2

    status = 0

    dmrstart_packet = createlucipacket(MID,commandtype,status,"START")

    write_port(dmrstart_packet)

    write_port("START")


def Bluetooth(data = "") :

    MID = 209

    commandtype = 2

    status = 0

    #data = command

    BTcommand_packet = createlucipacket(MID,commandtype,status,data)

    write_port(BTcommand_packet)

    if data != "" :

    	write_port(data)


def AllowPlayack(data = "") :

    allowed = "1"
    notallowed = "0"

    global currentaudiosource
    newsource = data

    print "Current Source %s" %currentaudiosource
    print "New Source %s" %newsource
	  
    if (currentaudiosource == "1") and (newsource != "1"):

        IsAllowed(allowed)
        Airplay("PREVENT")
        time.sleep(.2)
        Airplay("BUSY")
        time.sleep(.2)
        Airplay("ALLOW")


    elif (currentaudiosource != "1") and (newsource == "1"):
        IsAllowed(allowed)
        Airplay("AVAILABLE")


    elif currentaudiosource == "24":

        if newsource == "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            STOPPLay = createlucipacket(40, 2, 0, "STOP")
            write_port(STOPPLay)
            write_port("STOP")
            Airplay("AVAILABLE")

        elif newsource != "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            STOPPLay = createlucipacket(40, 2, 0, "STOP")
            write_port(STOPPLay)
            write_port("STOP")


    elif currentaudiosource == "14":

        if newsource == "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            AuxStop = createlucipacket(96, 2, 0, "0")
            write_port(AuxStop)
            Airplay("AVAILABLE")

        elif newsource != "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            AuxStop = createlucipacket(96, 2, 0, "0")
            write_port(STOPPLay)
            write_port("STOP")

    else :

        IsAllowed(allowed)

    currentaudiosource = data


def volumechange(data = ""):
	print " Volume changed : %s" %data

def IPADDR(data1 = ""):
	print " IPADDR is : %s" %data1

def Zonevolumechange(data = ""):
	print " Zone Volume changed : %s" %data

def PairStatus(data = ""):
	print " SharePair Status : %s" %data

def networkstatus(data = "") :    
    networkstatus = data.split('#')
    print "Network Status :%s" %networkstatus[0]

    if networkstatus[0] == "1":
        wifistatus = networkstatus[1].split(',')

        if wifistatus[1] == "1":
            print "WiFi is up"
            print "Read Wi-Fi ipaddress over MB 91"
            wifiip = createlucipacket(91, 2, 0, "IPADDR:wlan0")
            datawritten = write_port(wifiip)
            datawritten = write_port("IPADDR:wlan0")

        elif wifistatus[1] == "0":

            print "WiFi is down"

        else:

            print "Device Network Status Changed"

    elif networkstatus[0] == "3":

        wifistatus = networkstatus[3].split(',')

        if wifistatus[1] == "1":

            print "P2P is up"

            print "Read p2p0 ipaddress over MB 91"

            p2p0ip = createlucipacket(91, 2, 0, "IPADDR:p2p0")
            datawritten = write_port(p2p0ip)
            datawritten = write_port("IPADDR:p2p0")


        elif wifistatus[1] == "0":

            print "P2P is down"

        else:

            print "Device Network Status Changed"

                    #logfilewrite("Network has changed\n")

    elif networkstatus[0] == "2":

        print "Ethernet changed" 

        print "Read Ethernet ipaddress over MB 91"
 
        Ethip = createlucipacket(91, 2, 0, "IPADDR:eth0")
        datawritten = write_port(Ethip)
        datawritten = write_port("IPADDR:eth0")                   

     
    elif networkstatus[0] == "4":

        print "Configuration Mode changed" 
      
    else:

         print "NO network"



def DDMSSSID(data = ""):

	print "DDMSSSID is %s" %data


def SceneName(data = ""):

	print "SceneName is %s" %data


def QuerryDDMS(data = ""):

	print " DDMS State is %s"
	ntptrigger = createlucipacket(229, 2, 0, "ntp")
	datawritten = write_port(ntptrigger)
	datawritten = write_port("ntp")


def UARTReady (data = ""):

    print "LS UART Ready "

    print "Device UART is Up"

    print "Send Host Present Message over MB 9"

    deviceisup = True

    outluciheader = createlucipacket(9, 2, 0, "")
    datawritten = write_port(outluciheader)

    print "Send Host Version Message over MB 6"

    hostversion = createlucipacket(6, 2, 0, "103")
    datawritten = write_port(hostversion)
    datawritten = write_port("1234")

    
    print "Read Firmware Version Message over MB 5"
    fwversion = createlucipacket(5, 1, 0, "")
    datawritten = write_port(fwversion)

    readnvitem = createlucipacket(208, 2, 0, "READ_GoogleCast")
    datawritten = write_port(readnvitem)
    datawritten = write_port("READ_GoogleCast")

    readnvitem = createlucipacket(208, 2, 0, "READ_ssid")
    datawritten = write_port(readnvitem)
    datawritten = write_port("READ_ssid")


def RebootRequest (data = "reboot request") :
    print "Reboot Request from LS"
    print "Send reboot to LS MB 115"
    requestsent = createlucipacket(115, 2, 0, "")
    write_port(requestsent)


def SDStatus(data = "") :

    print "requested SDCard status"

    SDrequest = createlucipacket(71, 1, 0, "")

    write_port(SDrequest)
    
    
def ConfiugurationStatus(data) :
    networkconnectstatus = int(data)

    print "WAC Configuration Status-143:  %d " %networkconnectstatus



def DeviceDisconnected(data = "") :

	DeviceDisconnected = int(data)
	if DeviceDisconnected == "1":
		print "USB Disconnected"
	elif DeviceDisconnected == "2":
		print "iPod Disconnected"
	elif DeviceDisconnected == "3":
		print "SD-Card Disconnected"
	else:
		print "UnKnown status"


def DeviceConnected(data = "") :

	DeviceConnected = int(data)
	if DeviceConnected == "1":
		print "USB Connected"
	elif DeviceConnected == "2":
		print "iPod Connected"
	elif DeviceConnected == "3":
		print "SD-Card Connected"
		SDStatus()
	else:
		print "UnKnown status"


def Upgradestart(data = "") :

    MID = 211

    commandtype = 2

    status = 0

    Upgradestart_packet = createlucipacket(MID,commandtype,status,data)

    write_port(Upgradestart_packet)

    if data != "" :

    	write_port(data)


def ReqFwUpgrade (data = "") :
	print "Fwupgrade Request from LS %s" %data
	Upgradestart("start")



def NVREAD (data = "") :

	print "Current NVREAD value: %s" %data
	
	if (data == "GoogleCast:false") and (data == "ssid:"):
		
		print "SSID is Empty, Trigger WAC"
		print "Send reboot to LS MB 142"
		WACtrigger = createlucipacket(142, 2, 0, "")
		write_port(WACtrigger)
	else:
		print "Speaker is already connected to Network"


def WPSConfigStatus (data):

	WPSConfigStatus = int(data)
	print "WPS Config Status %d " %WPSConfigStatus

	if WPSConfigStatus == "1":
		print "WPS Failed"
	elif WPSConfigStatus == "2":
		print "WPS Timeout"
	elif WPSConfigStatus == "3":
		print "WPS Success"
	else:
		print "No Status"


def iDeviceConfigStatus (data) :

    iDeviceConfigStatus = int(data)

    if iDeviceConfigStatus == "1":
            print "Waiting For connection"

    elif iDeviceConfigStatus == "2":
            print "User Declined"

    elif iDeviceConfigStatus == "3":
            print "Network Information Unavailable"

    elif iDeviceConfigStatus == "4":
            print "Configuration Success"

    elif iDeviceConfigStatus == "5":
            print "Configuration Failed"

    else:
            print "No Status"


def PWStatus(data) :

    PWStatus = int(data)

    if PWStatus == "1":
            print "PSM Deep Sleep / network standby End"

    elif PWStatus == "2":
            print "PSM Deep Sleep Start"

    elif PWStatus == "3":
            print "PSM Network Standby Start"

    else:
            print "No Status"


def NTPSTATUS(data = ""):

    print "Current NTP Status is %s" %data


def AppControl(data = ""):

    print "AppControl Status is %s" %data

def CastOTAStatus (data) :


    print " iOS Config Status %s " %data

 
def LS9FwStatus (data) :


    print " LS9FwStatus %s " %data
        
 
def ISPlayStatus (data) :


    print " Is Play Status is %s " %data

 
def CastSetupSatus (data) :


    print " CastSetupSatus is %s " %data
        
 
def RSSIIndicator(data) :


    print " RSSI Value is %s" %data

 
def BTStatus(data) :


    print " BT Status is %s " %data

        
messagebox = {6 : HostVersion,
	
		10 : AllowPlayack,

		24 : PWStatus,

		36 : DeviceDisconnected,

		38 : DeviceConnected,

		50 : CurrentSource,

		51 : CurrentPlayingStatus,

		54 : ISPlayStatus,

		64 : volumechange,

		69 : ReqFwUpgrade,

		70: AppControl,

		71: SDStatus,
		
		91 : IPADDR,

		#95 : AuxInStart,
		
		#96 : AuxInStop,

		103 : QuerryDDMS,

		105 : DDMSSSID,

		107 : SceneName,

		114 : RebootRequest,

		124 : networkstatus,

		126 : iDeviceConfigStatus,

		140 : WPSConfigStatus,

		143 : ConfiugurationStatus,

		151 : RSSIIndicator,

		208 : NVREAD,

		209 : BTStatus,

        219 : Zonevolumechange,

		221 : PairStatus,

		222 : CastOTAStatus,

		223 : LS9FwStatus,

		224 : CastStatus,

		494 : CastSetupSatus,

		43690 : UARTReady,

		43981 : LSInBSL,

            }



def packetanalyser_test() :

    while True :

        global q

        global lock

        global responsewaitlist

        global responselist

        responsewaitlist = []

        responselist = {}

        queuemessage = q.get()

        luciheader =  queuemessage[0]

        data = queuemessage[1]

        remoteid = int(luciheader[0])

        commandtype = int(luciheader[1])

        command = int(luciheader[2])

        commandstatus = int(luciheader[3])

        crc = int(luciheader[4])

        datalength = int(luciheader[5])

        print "CommandType : %d " %commandtype

        print "Command : %d " % command

        print "Commandstatus : %d " %commandstatus

        print "data : %s " %data

        functioncall = messagebox.get(command)
	#print functioncall
        if command in responsewaitlist :

                position = responsewaitlist.index(command)

                responsewaitlist.remove[position]

                responselist[command]= commandstatus+"#"+data          

        else :

            messageboxthread = Thread(target = functioncall,args=(data,))

            messageboxthread.start()

            messageboxthread.join()

        print "-----------------------------------------------------------------"



def createlucipacket(mid,commandtype,status,data):
    remoteid = 43690 ##int value 0XAAAA
    crc = 0
    #print len(data)
    luciheader = struct.pack('>HBHBHH',remoteid,commandtype,mid,status,crc,len(data))
    #print "writing data :%s" %luciheader.encode('hex')
    return luciheader



def write_port(data):

    print "Write port Called"

    byteswritten  = port.write(data)

    port.flushOutput()

    return byteswritten

    

def read_serialPort():

    global q

    print ("\n inside read port \n")

    headerLength = 10

    bytesRead = 0

    

    while True:

        luciheader = port.read(1)

        bytesRead = 1

        while True :

            checkheadstart = luciheader.encode('hex')

            if (checkheadstart == "aa"):

                #print "Got the header"

                bytesRead = 1

                break

            else :

                luciheader = port.read(1)

                bytesRead = 0



        readtempbuffer = port.read(headerLength - bytesRead)

        if (len(readtempbuffer) != (headerLength - bytesRead) ):

            

            print " LUCI Header Read Error. Skipping this packet"

        else :

            luciheader = luciheader+readtempbuffer

            luciheader_unpacked = struct.unpack(">HBHBHH",luciheader)

            datalength = luciheader_unpacked[5]

            data = port.read(datalength)

            if (len(data) != datalength):

                print "Data not read completely. Printing Partial Data"

            q.put((luciheader_unpacked,data))



         

def main():

    comport = raw_input('Enter the COM port name ')

    print ("Opening COM port %s" %comport)

    global port

    global deviceisup

    global ipaddress

    global restartcount

    global q

    global lock

    global currentaudiosource
    global ethip1
    global ethip

    currentaudiosource = "0"

    lock = threading.Lock()

    q = Queue.Queue(maxsize =0)

    ipaddress = "0.0.0.0"

    restartcount = 0

    deviceisup = False 

    port = serial.Serial()

    port.baudrate = 115200

    port.port = comport

    port.bytesize = serial.EIGHTBITS

    port.parity = serial.PARITY_NONE

    port.stopbits = serial.STOPBITS_ONE

    port.timeout = 1

    port.rtscts = False

    port.dsrdtr = False

    port.xonxoff = False

    try :

      port.close()

      time.sleep(.1)

      port.open()

    except SerialException:

      print 'port already open. Terminating the program'

      exit()



    port.flushInput()

    port.flushOutput()

    readthread = Thread(target = read_serialPort, args = ())

    readthread.daemon = True

    readthread.start()    

    packetparser = Thread(target = packetanalyser_test,args = ())

    packetparser.daemon = True

    packetparser.start()

    readthread.join()

    packetparser.join()



if __name__ == "__main__" :

    main()
