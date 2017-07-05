import OSC
import time
import random

client = OSC.OSCClient()
client.connect(('127.0.0.1', 57120))

firstMessage = OSC.OSCMessage()
firstMessage.setAddress("/event")
firstMessage.append(440)
firstMessage.append(1)
client.send(firstMessage)

time.sleep(2)

secondMessage = OSC.OSCMessage()
secondMessage.setAddress("/event")
secondMessage.append(880)
secondMessage.append(0)
client.send(secondMessage)