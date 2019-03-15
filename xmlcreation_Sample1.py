# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#
#This script is used to create the fwdownload.xml file for LS9/LS9AD/GVA OTA upgrade testing	#
#               Created by Kannan.P																#
# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#	# 	#	#	#	#

#!/usr/bin/python
import sys
import lxml.etree
import lxml.builder    

E = lxml.builder.ElementMaker()
ROOT = E.content
FIELD1 = E.fw_version
FIELD2 = E.mcu_version
FIELD3 = E.firmware
FIELD4 = E.otapackage
FIELD5 = E.ForceUpgrade
FIELD6 = E.crc32check
FIELD7 = E.otacrc
FIELD8 = E.MAC

"""
fw_version_Value = '100'
mcu_version_Value = '100'
firmware_Value = "http://106.51.231.213/download/Customer/GVA/SoundCrush/Polaroid-SC950/NewTest/83_IMAGE_network_SC950"
otapackage_Value = "http://106.51.231.213/download/Customer/Libre_Demo/OTA/GVA/internal_1.36a_assistantdefault-user_146299_cast_receiver_signed.zip"
crc32check_Value = "sadsasdas"
ForceUpgrade_Value = 'yes'
macaddress ='D8:f7:10:c4:e1:20'
"""

fw_version_Value = sys.argv[1]
mcu_version_Value = sys.argv[2]
firmware_Value = sys.argv[3]
otapackage_Value = sys.argv[4]
ForceUpgrade_Value = sys.argv[5]
crc32check_Value = sys.argv[6]
otacrc_Value = sys.argv[7]
macaddress = sys.argv[8]
macempty = ""

if macaddress == "":
    the_doc = ROOT(
            FIELD1('p',fw_version_Value),
            FIELD2(mcu_version_Value),
            FIELD3(firmware_Value),
            FIELD4(otapackage_Value),
            FIELD5(ForceUpgrade_Value),
            FIELD6(crc32check_Value),
            FIELD7(otacrc_Value),
			)    
elif macaddress == 'empty' :
	the_doc = ROOT(
            FIELD1('p',fw_version_Value),
            FIELD2(mcu_version_Value),
            FIELD3(firmware_Value),
            FIELD4(otapackage_Value),
            FIELD5(ForceUpgrade_Value),
            FIELD6(crc32check_Value),
            FIELD7(otacrc_Value),
            FIELD8(macempty),
			)
else:
	the_doc = ROOT(
            FIELD1('p',fw_version_Value),
            FIELD2(mcu_version_Value),
            FIELD3(firmware_Value),
            FIELD4(otapackage_Value),
            FIELD5(ForceUpgrade_Value),
            FIELD6(crc32check_Value),
            FIELD7(otacrc_Value),
            FIELD8(macaddress),
			)
print lxml.etree.tostring(the_doc, xml_declaration=True,encoding='utf-8', pretty_print=True)


