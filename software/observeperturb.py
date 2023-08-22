
from MPPTController import MPPTController
import time

def clamp(vRef):
    '''clamp vRef voltage'''
    if vRef <= 0:
        vRef = 0
    elif vRef >= 70:
        vRef = 70
    return vRef

device = MPPTController()
device.shutdown(True)
time.sleep_ms(1000)
device.shutdown(False)

power = 0.
voltage_delta = 0.
power_delta = 0.
voltage_pre = 0.
power_pre = 0.
device.setDutyCycle(0)
time.sleep(1)

while(True):
    device.getfilteredADC()
    device.calcADCData()
    power_delta = device.power[0] - power_pre
    voltage_delta = device.voltage[0] - voltage_pre
    power_pre = device.power[0]
    voltage_pre = device.voltage[0]

    if power_delta >= 0:
        if voltage_delta > 0:
            device.vRef -= 1
        else:
            device.vRef += 1
    elif power_delta < 0:
        if voltage_delta > 0:
            device.vRef += 1
        else:
            device.vRef -= 1
            
    device.vRef = clamp(device.vRef)
    device.setDutyCycle(device.vRef)
    device.printOut()
    time.sleep_ms(100)
