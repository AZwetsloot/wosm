import sys, time
from telnetlib import Telnet
__author__ = 'alex'

class Telnet_MCU():

    is_connected = False
    units = "dac"               # "dac" or "real".
    all_lines = dict(dict())    # All the necessary info about all lines

    def __init__(self, host, port, mytimeout = 5, units = "real"):
        # Initiate the question
        self.wos = Telnet()
        try:
            self.wos.open(host,port,timeout=mytimeout)
            self.wos.read_until("password:".encode())
            self.wos.write("wosm\r\n".encode())
            clearBuffer = self.wos.read_until("W>".encode())
            self.is_connected = True
        except:
            print("Connection error:", sys.exc_info()[0])
        return

    def cmd(self,cmd):
        # Send a command to WOSM
        if self.is_connected:
            cmd+="\r\n"
            self.wos.write(cmd.encode())
            reply = self.wos.read_until("W>".encode()).decode().replace("W>","").splitlines()[0]
        else:
            reply = "Not connected."
        return reply

    def getLatency(self):
        # Return the connection latency (There and back)
        # in µs.
        start = time.perf_counter()
        for i in range(0,10):
            result = self.cmd("delta")
        end = time.perf_counter()
        return round(((end-start)/10)*1e6,2)

    def MoveAndAwait(self,point,time_millisecs):
        x,y = point
        continue_waiting = True
        # Move to x, y, z point.
        self.cmd("dac_dest px %s" % x)
        self.cmd("dac_dest py %s" % y)
        while continue_waiting:
            last_movement = self.cmd("dac_last")
            if int(last_movement) > time_millisecs*1000:
                continue_waiting = False
            elif "connected" in last_movement:
                print("Error: Not connected in MoveAndAwait...")
                continue_waiting = False
        # Return control to caller.
        return

    def getXYZ(self):
        x = self.cmd("dac_val px")
        y = self.cmd("dac_val py")
        z = self.cmd("dac_val pz")
        return (x,y,z)

    def getUnits(self, line):
        units = self.cmd("dac_unit %s" % line)
        return units

    def getRange(self, line):
        range = float(self.cmd("dac_range %s" % line))
        return range

    def getMinMax(self, line):
        dac_min = int(self.cmd("dac_min %s" % line))
        dac_max = int(self.cmd("dac_max %s" % line))
        return (dac_min, dac_max)

    def getLineVal(self, line):
        line_val = int(self.cmd("dac_val %s" % line))
        return line_val

    def getRef(self, line):
        line_ref = self.cmd("dac_ref %s" % line)
        return line_ref

    def getMacroList(self):
        # Get a list of macros
        macroList = list()
        i = 0
        wml_cat = self.cmd("wml_file_cat %s" % i)
        while wml_cat is not "" and "Not connected" not in wml_cat:
            i+=1
            macroList.append(wml_cat)
            wml_cat = self.cmd("wml_file_cat %s" % i)
        return macroList

    def Disconnect(self):
        # Graceful exit.
        self.cmd("exit")
        self.wos.close()
        return


class USB_MCU():

    def __init__(self):
        return

