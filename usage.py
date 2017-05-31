__author__ = 'alex@zwetsloot.uk'
import wosm

wos = wosm.Telnet_MCU("hermes.al.cx",25)
print("================================")
print("WOSM storm1.cmcb.local v1.6f")
print("Latency: %sus" % wos.getLatency())
print("================================")

print(wos.cmd("HELO mail.al.cx"))
print(wos.cmd("HELO mail.al.cx"))
