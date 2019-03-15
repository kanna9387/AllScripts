import binascii
bytesize = 0
with open("Mavid.bin",'r+b') as binfile :
    with open("Mavid_new.bin","wb") as newfile :
        while bytesize < int("0x170000",16):
            #byte_read = binfile.read(1)
            newfile.write(binfile.read(1))
            bytesize+=1
        with open ("Sample.txt","rb") as samplefile :    
            while True :
                lines = samplefile.readline()
                if lines :
                    if "0x" not in lines and "-1" not in lines :
                        #print lines + "msdbvfkjd"
                        pass
                    else :
                        remove1 = lines.replace('{',"")
                        remove2 = remove1.replace('}',"")
                        writelist = remove2.split(',')
                        #print writelist
                        for value in writelist :
                        	#value = writelist[i]
                            if "0x" in value :
                            	value = value.strip()
                                newfile.write(binascii.unhexlify(''.join(format(value[2:],'>04s'))))
                            elif "1" in value and int(value) == 1:
                            	value = value.strip()
                            	#print value,len(value),type(value)
                                newfile.write(binascii.unhexlify(''.join(format(value,'<02s'))))
                            elif "-1" in value and int(value) == -1:
                            	#value = value.strip()
                            	newfile.write(binascii.unhexlify(''.join(format("FFFF",'>02s'))))
                            else :
                            	pass
                        

                else :
                    break

        binfile.seek(int("0x170000",16))
        while True :
            readbyte = binfile.read(1)
            if readbyte :
                newfile.write(readbyte)
            else :
                break
