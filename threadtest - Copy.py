from multiprocessing import Process, Queue
import time
import serial
from serial import SerialException
from threading import Thread
import struct


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
    print "Hello"
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

if __name__ == "__main__" :
    main()