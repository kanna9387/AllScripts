from playsound import playsound
import os
import sys

argumentList = sys.argv 
print argumentList 

file = sys.argv[1]

print file

# initialize play

playsound(file)
