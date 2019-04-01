#hl7_messageSender.Hl7Message.send("167.81.222.175",1235,"MSH")
#obj = hl7_portScanner.Scan()
#obj.start("167.81.222.175",1235,"",2)

#obj = networkAnalyzer.analyze()

#obj.hl7Traffic("C:\\Users\\310283356\\Documents\\Research\\capt4.pcapng")

#obj = hl7_Server.server2x()
#obj.startServer(10023,"A"*500)


#from hl7_exhaust import *

#for i in range(1, 999999):
#    obj = exhaust()
#    obj.port("167.81.222.175",1234)

#import hl7_fuzzer as fe
#message = "MSH | ^ ~\ & | MegaReg | <%FUZZ%> | SuperOE | <%FUZZ%> | 20060529090131 - 0500 | | ADT ^ A01 ^ ADT_A01 | 01052 901 | P | 2.5 EVN | | 200605290901 | | | | 200605290900"

#message,host,port,mode
#fe.start_fuzzing(message, "167.81.222.175", 1235, 3)