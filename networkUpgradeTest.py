import mechanize
import os
import time
import serial
import sys

def networkFlash(url,FormNo):
    Form=FormNo
    filename = 'lsimage'
    try:
        fp = open(filename,'r')
        fp.close()
    except :
        print "lsimage not found.. \n\n Kindly place lsimage in the script folder and try again!!! \n\n"
        main()
    link = url
    print "Connecting to "+link+" .....\n"
    resultUrl = link
    browser = mechanize.Browser()
    try:
        browser.open(resultUrl)
        print "Webpage opened successfully...\n"
    except:
        print "Couldnot open "+link
        print "\n\nKindly check if system is connected to the same network as of device...\n\nTest Failed!!!\n\n"
        return
    browser.select_form(nr=Form)
    print "Form "+str(Form)+" selected..\n"
    try:
        
        control  = browser.form.find_control("FWMethod")
        for item in control.items:
		#print item.name
                if item.name == "Network":
                        item.selected = True
    
                        print "FWMETHOD selected as Network..\n"
                        try:
                            result = browser.submit()
                        except:
                            print "Could not start flashing with FW_METHOD as NETWORK!!!\nTest Failed!!!\n"
                            return
    except:
        print "This form doesnot contain the FWmethod"
        time.sleep(0.5)
	networkFlash(link,Form+1)
    time.sleep(5)
    browser = mechanize.Browser()
    browser.open(resultUrl)
    print "Webpage opened successfully...\n"
    print "Upload page opened...\n"
 
    browser.select_form(nr=0)
    print "Form selected..\n"
    time.sleep(1)
    
    browser.form.add_file(open(filename,'rb'),'application/file',filename,name='filename')
    print "Uploading lsimage to Network...\n"
    time.sleep(2)
    try:
        result = browser.submit()
    except:
        print "Exception raised"

    br = mechanize.Browser()
    br.open(str(resultUrl)+"/confirm_download.asp")
    print "Confirm page opened...\n"
 
    br.select_form(nr=0)
    print "Form selected..\n"
    time.sleep(1)
    
    try:
        result = br.submit()
    except:
        print "Exception raised"
 
    print "Network flashing has been started successfully...\n\n Kindly donot restart the device!!!\n\n"

    time.sleep(10)
    

if __name__=="__main__":
    try:
	fp =open("ip.txt","r")
	lines_ip = fp.readlines()
	#print lines_ip
	fp.close()
	for each in lines_ip:
	    networkFlash("http://"+str(each).strip().split("\n")[0],3)
    except:
       	networkFlash("http://"+raw_input("Enter the IP Address of the Device: "),0)
    
