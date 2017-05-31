# andor python module requires:
#   -> cython
#   -> numpy
#   -> C++ build tools http://landinghub.visualstudio.com/visual-cpp-build-tools


__author__ = 'alex@zwetsloot.uk'
import wosm
from ctypes import *
from matplotlib import pyplot as plt
import time
import numpy as np

wos = wosm.Telnet_MCU("192.168.10.134",1023)
print("================================")
print("WOSM storm1.cmcb.local v1.6f")
print("Latency: %sus" % wos.getLatency())
print("================================")

# Example 1: Move between two locations and take images.

# Get the stage size and the the maximum analogue output on that line.
dac_minmax_X = wos.getMinMax("px")
print("Debug: minmax X = " + str(dac_minmax_X))
dac_minmax_Y = wos.getMinMax("py")
print("Debug: minmax Y = " + str(dac_minmax_Y))
units = wos.getUnits("px")
print("Debug: units " + units)
range = (wos.getRange("px"),wos.getRange("py"))
print("Debug: real term range: " + str(range))
scalefactors = (dac_minmax_X[1]/range[0],dac_minmax_Y[1]/range[1])       #  Scale between um and dac values
print("Debug: scalefactors (x,y) " + str(scalefactors))
print("Debug: 10um would be %s dac units" % round(10*scalefactors[0],0))

# Get the xyz dac position so we can return to our location later
start_position = wos.getXYZ()

# Init camera -
dll = windll.LoadLibrary("C:\\Program Files\\Andor Driver Pack 2\\atmcd32d.dll")
print(dll.Initialize(""))
print(dll.SetReadMode(4))
print(dll.SetImage(1,1,1,512,1,512))
print(dll.SetAcquisitionMode(1))
print(dll.SetExposureTime(c_float(0.1)))
print(dll.CoolerON())
print(dll.SetShutter(1,1,0,0))
dll.SetTriggerMode(0)
dll.SetShutter(1, 0, 1000, 1000)
dll.SetExposureTime(c_float(0.1))
imStorage = c_uint16*(512*512)
imStorage = imStorage()
print(dll.StartAcquisition())
dll.WaitForAcquisition()
error = dll.GetAcquiredData16(pointer(imStorage), 512*512)
print(error)
dll.ShutDown()

wos.Disconnect()