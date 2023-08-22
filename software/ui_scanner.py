from MPPTController import MPPTController
import time

power_curve =[]

while(True):
    for duty in range(70):
        device.setDutyCycle(duty)
        time.sleep_ms(50)
        device.getfilteredADC()
        device.calcADCData()
        time.sleep_ms(50)
        power_curve.append(device.power[0])
        device.printOut()
        if device.voltage[0] < 12:
            print('Abbruch ', device.voltage[0])
            break
    power_max = max(power_curve)
    duty_max = power_curve.index(power_max)
    device.setDutyCycle(duty_max)
    device.getfilteredADC()
    device.calcADCData()
    print('finished')
    print('power_max:{}W duty_max:{}'.format(power_max, duty_max))
    time.sleep(10)

