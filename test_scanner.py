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
        print("data type of adtype is", type(adtype), "and its value is", adtype)
        print("data type of desc is", type(desc), "and its value is", desc)
        print("data type of value is", type(value), "and its value is", value)
        a = [desc,value]
        client.publish('raspberry/topic', payload=adtype, qos=0, retain=False)
        