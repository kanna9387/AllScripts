import pyping
import os, sys, time

Host_Ip = sys.argv[1]
r = pyping.ping(Host_Ip)

while True:
	if r.ret_code == 0:
		print("Success")
		time.sleep(600)
	else:
		print("Failed with {}".format(r.ret_code))
		break


#print('Timeout 5min is over')
