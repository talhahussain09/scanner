from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0,passive=True)

for dev in devices:
    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))
        a = [adtype,desc,value]
        client.publish('raspberry/topic', payload=a, qos=0, retain=False)