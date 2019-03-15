
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


def LSInBSL(data = "") :
    print " Device is in BSL"

def hostpresent(data = ""):
    print "Host is present"
    
def CurrentSource(data = "") :
	print "Current source under MB 50 %s" %data
	global currentaudiosource
	currentaudiosource = data
	return

    
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
    
def AuxStart(data = "") :
    print " In Aux Start"
    
    
def AllowPlayack(data = "") :
    allowed = "1"
    notallowed = "0"
    global currentaudiosource
    newsource = data
    print "Current Source %s" %currentaudiosource
    print "New Source %s" %newsource
	  
    if (currentaudiosource == "1") and (newsource != "1"):
        IsAllowed(allowed)
        #createlucipacket(MID,allowdata)
        Airplay("PREVENT")
        time.sleep(.2)
        Airplay("BUSY")
        time.sleep(.2)
        Airplay("ALLOW")
    elif (currentaudiosource != "1") and (newsource == "1"):
        IsAllowed(allowed)
        Airplay("AVAILABLE")
    else :
        IsAllowed(allowed)
    currentaudiosource = data
def volumechange(data = "") :
    print " Volume changed : %s" %data

def networkstatus(data = "") :    
    networkstatus = data.split('#')
    print "Network Status :%s" %networkstatus[0]
    if networkstatus[0] == "1":
        wifistatus = networkstatus[1].split(',')
        if wifistatus[1] == "1":
            print "WiFi is up"
        elif wifistatus[1] == "0":
            print "WiFi is down"
        else:
            print "Device Network Status Changed"
    elif networkstatus[0] == "3":
        wifistatus = networkstatus[3].split(',')
        if wifistatus[1] == "1":
            print "P2P is up"
        elif wifistatus[1] == "0":
            print "P2P is down"
        else:
            print "Device Network Status Changed"
                    #logfilewrite("Network has changed\n")
    elif networkstatus[0] == "2":
        print "Ethernet changed"                    
                
    else:
         print "Network has changed"
def DDMSSSID(data = "") :
    print "DDMSSSID"
def SceneName(data = "") :
    print "SceneName is"

def QuerryDDMS(data = "") :
    print " DDMS Name"
def UARTReady (data = "") :
    print "LS UART Ready "
    print "Device UART is Up"
    print "Send Host Present Message over MB 9"
    deviceisup = True
    outluciheader = createlucipacket(9, 2, 0, "")
    datawritten = write_port(outluciheader)
    
def ConfiugurationStatus(data) :
    networkconnectstatus = int(data)
    print "Configuration Status %d " %networkconnectstatus
    
messagebox = {10 : AllowPlayack,
              50 : CurrentSource,
              64 :  volumechange,
              103 : QuerryDDMS,
              105 : DDMSSSID,
              107 : SceneName,
              124 : networkstatus,
              143 : ConfiugurationStatus,
              43690 : UARTReady,               
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
        print "data : %s " % data
        functioncall = messagebox.get(command)
        if command in responsewaitlist :
                position = responsewaitlist.index(command)
                responsewaitlist.remove[position]
                responselist[command]= commandstatus+"#"+data          
        else :
            messageboxthread = Thread(target = functioncall,args=(data,))
            messageboxthread.start()
            messageboxthread.join()
        print "-----------------------------------------------------------------"

def createlucipacket(mid,commandtype,status, data):
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
    currentaudiosource = "0"
    lock = threading.Lock()
    q = Queue.Queue(maxsize =0)
    ipaddress = "0.0.0.0"
    restartcount = 0
    deviceisup = False 
    port = serial.Serial()
    port.baudrate = 57600
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
