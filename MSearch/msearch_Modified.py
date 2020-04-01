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
        data, addr = s.recvfrom(6557)
        print (addr, data)
        print ("\n")
        print (addr[0])
        print ("\n")
        print (data)
        print ("\n")
        a = str(addr)
        fo=open('links.txt','a')
        fo.write(a + '\n')
        fo.close()
        
except socket.timeout:
    s.close();
    pass
