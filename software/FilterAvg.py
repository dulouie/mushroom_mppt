class FilterAvg():
    def __init__(self, adc: ADC, samples: int):
        self.buf = 0.
        self.samples = samples
        self.adc = adc

    def calc(self):
        for sample in range(self.samples):
            self.buf += self.adc.read_u16()
        filtered = self.buf/self.samples
        self.buf = 0.
        return(filtered)