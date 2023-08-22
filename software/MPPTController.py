from machine import Pin, PWM, ADC, Timer
from singleton import singleton
from FilterAvg import FilterAvg
from PID import PID

rounded = 3
adcScaleFac = 3.2 / 2**16  		    # 3.3V / 2^16 (bit)
voltDiv = 36 / 2.2		            # voltage divider input stage 36k / 4.7k
currentSensivity = 0.2		    	# TMCS1108A3U 200mV/A
zeroCurrentHall = 3.2 * 0.1     	# datasheet suppy voltage * 0.1
corr = (1.117,                      # correction factor for all ADCs
        1.026,                        # voltage in, current in, voltage out, current out
        1.117,
        1.015)

@singleton
class MPPTController():
    ''' Hardware abtraction layer for MPPTController'''
    def __init__(self):
        self.pwm = PWM(Pin(6, Pin.OUT))
        self.pwm.freq(50000) 
        self.sd = Pin(7, Pin.OUT)
        self.adc1 = ADC(Pin(26, Pin.IN))
        self.adc2 = ADC(Pin(27, Pin.IN))
        self.adc3 = ADC(Pin(28, Pin.IN))
        self.adc4 = ADC(Pin(29, Pin.IN))
        self.filter1 = FilterAvg(adc=self.adc1, samples=50)
        self.filter2 = FilterAvg(adc=self.adc2, samples=50)
        self.filter3 = FilterAvg(adc=self.adc3, samples=50)
        self.filter4 = FilterAvg(adc=self.adc4, samples=50)
        self.filtered = [0.,0.,0.,0.]
        self.voltage = [0.,0.]
        self.current = [0.,0.]
        self.power = [0.,0.]
        self.efficiency = 0.
        self.duty = 0
        self.vRef = 0
        self.pid = PID(scale='ms')

    def shutdown(self, s: bool):
        '''Shutdown the mosfet driver'''
        if s is True:
            self.sd.off()
        else:
            self.sd.on()

    def setpidTuning(self,kp, ki, kd):
        '''Set pid tunings for output controller'''
        self.pid.tunings = (kp, ki, kd)

    def printOut(self):
        '''Print all voltages, currents and power to console'''
        print("duty:{} IN:{}V/{}A {}W OUT:{}V/{}A vRef:{} eff:{}".format(self.duty,
                                                    self.voltage[0],
                                                    self.current[0], 
                                                    self.power[0], 
                                                    self.voltage[1], 
                                                    self.current[1],
                                                    self.vRef,
                                                    self.efficiency))
        
    def setDutyCycle(self, duty):
        '''Set mosfet dutycycle for boost converter'''
        self.duty = int(((100 - duty) / 100) * 65536)
        self.pwm.duty_u16(self.duty)

    def getfilteredADC(self):
        '''Sample and filter adc data'''
        self.filtered[0] = self.filter1.calc()
        self.filtered[1] = self.filter2.calc()
        self.filtered[2] = self.filter3.calc()
        self.filtered[3] = self.filter4.calc()

        return(self.filtered)

    def calcADCData(self):
        '''Calcuate raw adc data to voltages and currents'''
        self.voltage[0] = round(corr[0]*self.filtered[0]*adcScaleFac*voltDiv, rounded)
        self.voltage[1] = round(corr[2]*self.filtered[2]*adcScaleFac*voltDiv, rounded)
        self.current[0] = round(corr[1]*(((self.filtered[1] *
                                                adcScaleFac) - zeroCurrentHall) / 
                                                currentSensivity), rounded)
        self.current[1] = round(corr[3]*(((self.filtered[3] *
                                                adcScaleFac) - zeroCurrentHall) /
                                                currentSensivity), rounded)
        self.power[0] = round(self.voltage[0] * self.current[0], rounded)
        self.power[1] = round(self.voltage[1] * self.current[1], rounded)
        self.efficiency = round(self.power[1] / self.power[0], rounded)
