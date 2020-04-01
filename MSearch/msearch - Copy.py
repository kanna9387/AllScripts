import socket

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'MX: 10\r\n' \
    'ST: urn:schemas-upnp-org:device:DDMSServer:1\r\n' \
    'HOST: 239.255.255.250:1800\r\n' \
    'MAN: \"ssdp:discover\"\r\n'

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(5)
s.sendto(bytes(msg.encode()),('239.255.255.250',1800))
a=None;
fo=open('links.txt','w')
fo.close()
try:
    while True:
        data, addr = s.recvfrom(65507)
        print (addr, data)
        a = str(data)
        fo=open('links.txt','a')
        fo.write(a + '\n')
        fo.close()
        
except socket.timeout:
    s.close();
    pass
