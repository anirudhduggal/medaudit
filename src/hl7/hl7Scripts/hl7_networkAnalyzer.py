import networkx as nx
from scapy.all import *
from scapy.utils import PcapWriter
from medaudit.settings import BASE_DIR
from urllib.parse import unquote

class hl7Traffic:

    def analyze(self,pcapFilename):
        hl7Output =BASE_DIR+"/hl7/networkFiles/hl7PacketDump.pcap"
        hl7Dump = PcapWriter((hl7Output),append=True,sync=True)

        G = nx.DiGraph(directed=True)

        print(unquote(pcapFilename))
        pcapFilename = unquote(pcapFilename)

        packets = rdpcap(pcapFilename)
        networkSession = packets.sessions()

        for session in networkSession:
            for packet in networkSession[session]:
                try:
                    if (str(packet[TCP].payload).startswith("b\'")) and str(packet[TCP].payload).endswith("r\'"):
                        hl7Dump.write(packet)
                        G.add_edge( (str(packet[IP].dst)+":"+str(packet[IP].dport)),(str(packet[IP].src)+":"+str(packet[TCP].sport)))
                except:
                    continue

        nx.draw(G, with_labels=True)
        plt.show()
        hl7Dump.close()

        return hl7Output