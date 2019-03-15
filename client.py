from __future__ import division
import os,sys
import socket
import time
import signal
from threading import Thread,Lock,Condition
import sys
from struct import *
import glob
dict_intent={}
import pyaudio
import wave
import random
class lucicomm:
        def __init__(self,ip,port,list_message_box,callback):
            self.ip=ip
            self.port=port
            self.thread=0
            self.BUFFER_SIZE=1024
            self.list_message_box=list_message_box
            self.call_back=callback
            self.luci_dict={}
            self.luci_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.luci_sock.settimeout(150)
        def __enter__(self):
            self.thread=1
            try:
                self.luci_sock.bind(('',0))
                self.luci_sock.connect((self.ip,self.port))
                print("Device connected")
                self.sendLUCI_data([],3)
                print("Luci connection Successfull")
                threadoutput=Thread(target=self.Luci_recv)#,args=(self,))
                threadoutput.daemon=True
                threadoutput.start()
                return self
            except:
                self.thread=0
                return 0
            
        def __exit__(self,exc_type,exc_val,exc_tb):
                self.thread=0
                try:
                        
                        time.sleep(1)
                        self.sendLUCI_data([],4)
                        print("Luci connection Disconnected")
                        self.luci_sock.close()
                except:
                        pass
        def sendLUCI_data(self,data,boxid):
                luciarr=bytearray([0,0,2,0,0,0,0,0])
                luciarr[3]=boxid & 0xff
                luciarr[4]=boxid>>8 & 0xff
                datalen=len(data)
                datalenL=datalen & 0xff
                datalenH = datalen>>8 & 0xff
                datalenarr=bytearray([datalenL,datalenH])
                buf=bytearray()
                buf+=luciarr
                buf+=datalenarr
                buf+=bytearray(data)
                packbuf=pack('B'*len(buf),*tuple(buf))
                if(self.luci_sock):
                        self.luci_sock.sendall(packbuf)
                        time.sleep(.1)
        def paser_luci(self,data_list):
                if(len(data_list)<0):
                        return(0,0,[])
                else:
                        boxid=data_list[4]+data_list[3]*256
                        data_length=data_list[9]+data_list[8]*256
                        data=data_list[10:10+data_length]
                        return(boxid,data,data_list[10+data_length:])
        def update_dict(self,luci_dict,boxid,data):
                
                if(boxid not in self.list_message_box):
                    luci_dict[boxid]=data
                else:
                    luci_dict[boxid]="".join(map(lambda x: chr(x),data))
                    if(boxid==self.list_message_box[-1]):
                        self.call_back(luci_dict[boxid])
                    
        def Luci_recv(self):
            data_list=[]
            while(self.thread):
                   time.sleep(.1)
                   recv_data=self.luci_sock.recv(self.BUFFER_SIZE)
                   if len(recv_data):
                           del data_list
                           data_len=len(recv_data)
                           data_list=unpack("%dB"%data_len,recv_data)
                           while(len(data_list)):        
                                boxid,data,data_list=self.paser_luci(data_list)
                                if len(data):
                                   self.update_dict(self.luci_dict,boxid,data)
            self.threadkilled=0
class Commclass(lucicomm):
        def __init__(self,ip,port,call_back,set_mbox=311,recv_mbox=310,intent_mbox=312):
                lucicomm.__init__(self,ip,port,[recv_mbox,intent_mbox],call_back)
                self.set_mbox=set_mbox
                self.recv_mbox=recv_mbox
                self.intent_mbox=intent_mbox
                self._ip="127.0.0.1"
                

        def __enter__(self):
                lucicomm.__enter__(self)
                return self
        def __exit__(self,exc_type,exc_val,exc_tb):
                lucicomm.__exit__(self,exc_type,exc_val,exc_tb)
        def get_luci_data(self,env_name):
            data=[ord(i) for i in env_name]
            self.sendLUCI_data(data,self.recv_mbox)
            try:
                return self.luci_dict[self.recv_mbox]
            except KeyError:
                return None
        def set_luci_data(self,env_name,data):
            send_data=[ord(i) for i in "".join([env_name,":",data])]
            self.sendLUCI_data(send_data,self.set_mbox)

        
        @property
        def TargetIP(self):
            return self.get_luci_data("TargetIP")

        @TargetIP.setter
        def TargetIP(self,data):
            print("in setter")

            self.set_luci_data("TargetIP",data)

        @property
        def TargetPort(self):
            i=self.get_luci_data("TargetPort")
            if(i != None):
                return int(i)
            else:
                return -1
        @TargetPort.setter
        def TargetPort(self,data):
            self.set_luci_data("TargetPort",str(data))


        @property
        def LogPath(self):
            return self.get_luci_data("LogPath")
        @LogPath.setter
        def LogPath(self,data):
            self.set_luci_data("LogPath",data)

        @property
        def SystemID(self):
            return self.get_luci_data("SystemID")
        @SystemID.setter
        def SystemID(self,data):
            self.set_luci_data("SystemID",data)

        @property
        def SequenceLearning(self):
            return self.get_luci_data("SequenceLearning")
        @SequenceLearning.setter
        def SequenceLearning(self,data):
            self.set_luci_data("SequenceLearning",",".join(data))

        @property
        def DisplayWords(self):
            return self.get_luci_data("DisplayWords").split(',')
        @DisplayWords.setter
        def DisplayWords(self,data):
            print("in setter")
            self.set_luci_data("DisplayWords",",".join(data))

        @property
        def Sensitivity(self):
            return self.get_luci_data("Sensitivity").split(',')
        @Sensitivity.setter
        def Sensitivity(self,data):
            self.set_luci_data("Sensitivity",",".join(data))

        @property
        def Intents(self):
            return self.get_luci_data("Intents").split(',')
        @Intents.setter
        def Intents(self,data):
            self.set_luci_data("Intents",",".join(data))
        
        @property
        def PredictedSequence(self):
            return self.get_luci_data("PredictedSequence").split(',')
        @PredictedSequence.setter
        def PredictedSequence(self,data):
            self.set_luci_data("Intents",",".join(data))

        @property
        def NumberOfWords(self):
            i=int(self.get_luci_data("NumberOfWords"))
            if(i!=None):
                return int(i)
            else:
                return -1
        @NumberOfWords.setter
        def NumberOfWords(self,data):
            self.set_luci_data("NumberOfWords",int(data))

        
def function_callback(data):
    print("in call back function:{0} intent recived".format(data))
    if(data in dict_intent):
       dict_intent[data]+=1
    else:
       dict_intent[data]=1


dira="rotate_left"
data_dir=os.listdir(os.path.join(dira))
list_files=[]
for dirs in data_dir:
    for files in glob.iglob(os.path.join(dira,dirs,"*.wav")):
	list_files.append(files) 

	
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE=48000


def play_audio(file_name):
	f = wave.open(file_name,'rb')
	Rate=f.getframerate()
	p1= pyaudio.PyAudio()
	print(f.getsampwidth(), f.getnchannels(), f.getframerate())
	stream = p1.open(format=FORMAT,channels=f.getnchannels(),rate=Rate,output=True,frames_per_buffer=CHUNK)
	data = f.readframes(CHUNK)
	while data !=""  :
		stream.write(data)
		data = f.readframes(CHUNK)
	#Stop data flow		
	stream.stop_stream()
	stream.close()
	#Close PyAudio
	p1.terminate()

times={}
def update_dict(file_path):
	global times
	name,ext=os.path.splitext(file_path)
	folder_name=name.split('/')[-2]
	if folder_name in times:
		times[folder_name]+=1
	else:
		times[folder_name]=1
with Commclass("172.16.1.118",7777,call_back=function_callback) as luci:
    #print(luci.DisplayWords)
    #luci.Sensitivity=["0.7" for _ in range(9)]
    #luci.Sensitivity="0.6,0.6,0.6,0.6,0.9,0.4,0.5,0.95,0.95"
    #print(luci.Sensitivity)
    
    while True:
        try:
           #time.sleep(10)
		for i in range(100):
		   print(list_files)
		   random.shuffle(list_files)
		   for i in list_files:
			update_dict(i)
		   	play_audio(i)
		   	time.sleep(random.randint(2,7))
	
          	else:
			break
		
	   
        except KeyboardInterrupt:
            break
    print("\n\n\n\n number of times files played {0} and total intents recived {1} \n\n\n\n".format(times,dict_intent))
    
    
