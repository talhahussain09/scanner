from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

scanner_data = {}

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        scanner_data = {'time':datetime.now(),'AdvData':dev.rawdata,'MacAdd':dev.addr}
        client.publish('raspberry/topic', payload=scanner_data, qos=0, retain=False)
        print(datetime.now().time(), dev.rawData, dev.addr)
        
        scanner.clear()
        scanner.start()
        


scanner = Scanner().withDelegate(ScanDelegate())
scanner.start()

while True:
    scanner.process()
