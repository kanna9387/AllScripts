from multiprocessing import Process, Queue
import time
import serial
from serial import SerialException
import os
from threading import Thread
from sys import getsizeof
import struct



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
    writeserialport(isallowed_packet)
    writeserialport(data)

def Airplay(data = "") :
    MID = 12
    commandtype = 2
    status = 0
    #data = command
    airplycommand_packet = createlucipacket(MID,commandtype,status,data)
    writeserialport(airplycommand_packet)
    if data != "" :
    	writeserialport(data)



def DMRSTOP (data = "") :

    MID = 227

    commandtype = 2

    status = 0

    dmrstop_packet = createlucipacket(MID,commandtype,status,"STOP")

    writeserialport(dmrstop_packet)

    writeserialport("STOP")



def DMRSTART (data = "") :

    MID = 228

    commandtype = 2

    status = 0

    dmrstart_packet = createlucipacket(MID,commandtype,status,"START")

    writeserialport(dmrstart_packet)

    writeserialport("START")


def Bluetooth(data = "") :

    MID = 209

    commandtype = 2

    status = 0

    #data = command

    BTcommand_packet = createlucipacket(MID,commandtype,status,data)

    writeserialport(BTcommand_packet)

    if data != "" :

    	writeserialport(data)


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
            writeserialport(STOPPLay)
            writeserialport("STOP")
            Airplay("AVAILABLE")

        elif newsource != "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            STOPPLay = createlucipacket(40, 2, 0, "STOP")
            writeserialport(STOPPLay)
            writeserialport("STOP")


    elif currentaudiosource == "14":

        if newsource == "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            AuxStop = createlucipacket(96, 2, 0, "0")
            writeserialport(AuxStop)
            Airplay("AVAILABLE")

        elif newsource != "1":
            IsAllowed(allowed)    
            print "Stop to cast"
            AuxStop = createlucipacket(96, 2, 0, "0")
            writeserialport(STOPPLay)
            writeserialport("STOP")

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
            datawritten = writeserialport(wifiip)
            datawritten = writeserialport("IPADDR:wlan0")

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
            datawritten = writeserialport(p2p0ip)
            datawritten = writeserialport("IPADDR:p2p0")


        elif wifistatus[1] == "0":

            print "P2P is down"

        else:

            print "Device Network Status Changed"

                    #logfilewrite("Network has changed\n")

    elif networkstatus[0] == "2":

        print "Ethernet changed" 

        print "Read Ethernet ipaddress over MB 91"
 
        Ethip = createlucipacket(91, 2, 0, "IPADDR:eth0")
        datawritten = writeserialport(Ethip)
        datawritten = writeserialport("IPADDR:eth0")                   

     
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
	datawritten = writeserialport(ntptrigger)
	datawritten = writeserialport("ntp")


def UARTReady (data = ""):

    print "LS UART Ready "

    print "Device UART is Up"

    print "Send Host Present Message over MB 9"

    deviceisup = True

    outluciheader = createlucipacket(9, 2, 0, "")
    datawritten = writeserialport(outluciheader)

    print "Send Host Version Message over MB 6"

    hostversion = createlucipacket(6, 2, 0, "103")
    datawritten = writeserialport(hostversion)
    datawritten = writeserialport("1234")

    
    print "Read Firmware Version Message over MB 5"
    fwversion = createlucipacket(5, 1, 0, "")
    datawritten = writeserialport(fwversion)

    readnvitem = createlucipacket(208, 2, 0, "READ_GoogleCast")
    datawritten = writeserialport(readnvitem)
    datawritten = writeserialport("READ_GoogleCast")

    readnvitem = createlucipacket(208, 2, 0, "READ_ssid")
    datawritten = writeserialport(readnvitem)
    datawritten = writeserialport("READ_ssid")


def RebootRequest (data = "reboot request") :
    print "Reboot Request from LS"
    print "Send reboot to LS MB 115"
    requestsent = createlucipacket(115, 2, 0, "")
    writeserialport(requestsent)


def SDStatus(data = "") :

    print "requested SDCard status"

    SDrequest = createlucipacket(71, 1, 0, "")

    writeserialport(SDrequest)
    
    
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

    writeserialport(Upgradestart_packet)

    if data != "" :

    	writeserialport(data)


def ReqFwUpgrade (data = "") :
	print "Fwupgrade Request from LS %s" %data
	Upgradestart("start")



def NVREAD (data = "") :

	print "Current NVREAD value: %s" %data
	
	if (data == "GoogleCast:false") and (data == "ssid:"):
		
		print "SSID is Empty, Trigger WAC"
		print "Send reboot to LS MB 142"
		WACtrigger = createlucipacket(142, 2, 0, "")
		writeserialport(WACtrigger)
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

messagebox = {
        6 : HostVersion,

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

def readSerialPort() :
    print ("\n inside read port \n")
    headerLength = 10
    bytesRead = 0
    if serialport :
        print "portobjcreated \n"
    while True:
        try :
            luciheader = serialport.read(1)
        except :
            print "got Exception"
            return
        bytesRead = 1

        while True:
            
            checkheadstart = luciheader.encode('hex')
            if (checkheadstart == "aa"):
                #print "Got the header"
                bytesRead = 1
                break
            else :
                luciheader = serialport.read(1)
                bytesRead = 0

        readtempbuffer = serialport.read(headerLength - bytesRead)
        if (len(readtempbuffer) != (headerLength - bytesRead) ):
            
            print " LUCI Header Read Error. Skipping this packet\n"
        else :
            luciheader = luciheader+readtempbuffer
            luciheader_unpacked = struct.unpack(">HBHBHH",luciheader)
            datalength = luciheader_unpacked[5]
            data = serialport.read(datalength)
            if (len(data) != datalength):
                print "Data not read completely. Printing Partial Data\n"
            #q.put((luciheader_unpacked,data))
            print "CommandType : %d " %luciheader_unpacked[1]
            print "Command : %d " % luciheader_unpacked[2]            
            print "Commandstatus : %d " %luciheader_unpacked[3]
            print "data : %s " % data
                        #logfilewrite("Data : %s \n" % data)
            print "-------------------------------------------------------------"

def writeserialport(data):
    print"Writing Serial Port\n"
    byteswritten  = serialport.write(data)
    serialport.flushOutput()
    return byteswritten

def createlucipacket(mid,commandtype,status, data):
    remoteid = 43690 ##int value 0XAAAA
    crc = 0
    #print len(data)
    luciheader = struct.pack('>HBHBHH',remoteid,commandtype,mid,status,crc,len(data))
    #print "writing data :%s" %luciheader.encode('hex')
    return luciheader

def configureserialport(portnumber,baudrate) :
    #print "Configuring Serial port %s with Baudrate %d" %portnumber,%baudrate
    serialport = serial.Serial()
    serialport.baudrate = baudrate
    serialport.port = portnumber
    serialport.bytesize = serial.EIGHTBITS
    serialport.parity = serial.PARITY_NONE
    serialport.stopbits = serial.STOPBITS_ONE
    serialport.timeout = 1
    serialport.rtscts = False
    serialport.dsrdtr = False
    serialport.xonxoff = False
    return serialport

def uartinit(port,baud,writequeue) :
    global serialport
    serialport = configureserialport(port,baud,)
    try :
      serialport.close()
      time.sleep(.1)
      serialport.open()
    except SerialException:
      print 'port already open. Terminating the program\n'
      exit()

    readthread = Thread(target = readSerialPort, args = ())
    readthread.daemon = True
    readthread.start()
    while True :
        luciwrite = writequeue.get()
        newmb = luciwrite.split('#')
        newheader = createlucipacket(int(newmb[0]),int(newmb[1]),0, newmb[2])
        writeserialport(newheader)
        if newmb[2] != "":
            writeserialport(newmb[2])

def main() :
    print "LUCI Simulator started"
    global deviceisup
    global ipaddress
    global currentaudiosource
    global ethip1
    global ethip
    currentaudiosource = "0"
    port = raw_input("Enter the port number :")
    baud = int(raw_input("Ener buad rate :"))
    writeq = Queue()
    p = Process(target=uartinit, args=(port,baud,writeq))
    p.start()
    while True :
        dataentry = ""
        data = ""
        charinput = raw_input("")
        mbid = raw_input("Enter the MB number :")
        commandtype = raw_input("Enter the command type. 1. for set and 2 for Get :")
        if (int(commandtype) == 2) :
            dataentry = raw_input("Do you want to send data Y/y for yes and N/n for No :")
            if dataentry == 'Y' or dataentry == 'y' :
                data = raw_input("Enter the data :")
        newmb = mbid+"#"+commandtype+"#"+data
        writeq.put(newmb)
        n=raw_input("Press key to continue\n")
    p.join()

if __name__ == "__main__":
    main()