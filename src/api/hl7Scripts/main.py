#hl7_messageSender.Hl7Message.send("167.81.222.175",1235,"MSH")
#obj = hl7_portScanner.Scan()
#obj.start("167.81.222.175",1235,"",2)

#obj = networkAnalyzer.analyze()

#obj.hl7Traffic("C:\\Users\\310283356\\Documents\\Research\\capt4.pcapng")

#obj = hl7_Server.server2x()
#obj.startServer(10023,"A"*500)


from hl7_maliciousServer import startServer

startServer(8888,"Server test",1)

