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
FIELD2 = E.firmware



fw_version_Value = sys.argv[1]
firmware_Value = sys.argv[2]

the_doc = ROOT(
            FIELD1(fw_version_Value),
            FIELD2(firmware_Value),
			)
print lxml.etree.tostring(the_doc, xml_declaration=True,encoding='utf-8', pretty_print=True)


