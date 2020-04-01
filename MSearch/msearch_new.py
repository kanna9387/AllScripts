import socket

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST: 239.255.255.250:1800\r\n' \
	'ST:upnp:rootdevice\r\n' \
    'MX: 10\r\n' \
    'MAN: \"ssdp:discover\"\r\n'

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(10)
s.sendto(bytes(msg.encode()),('239.255.255.250',1800))
print ("Sending M-Search packets")
a=None;
fo=open('links.txt','w')
fo.close()
try:
    while True:
        data, addr = s.recvfrom(65507)
        print (addr, data)
        print ("\n")
        print (addr[0])
        print ("\n")
        #print (type(data))
        #print ("\n")
        a = str(addr)
        a2 = str(addr[0])
        print (a2)
        a1 = str(addr[0])
        b = str(data)
        fo=open('links.txt','a')
        #fo.write(a1 + '\n')
        #fo.write(a + '\n')
        #fo.write(b + '\n')
        fo.close()
        
except socket.timeout:
    s.close();
    pass
