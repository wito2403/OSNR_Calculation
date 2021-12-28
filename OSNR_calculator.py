from scipy.constants import h
from math import log10


# Function to convert from dBm to mW
def dBm2mW(dBm):
    return 10 ** ((dBm) / 10.)


class OSNRCalculator:
    def __init__(self, input_power, unit_attenuation, track_length, amplifiers_count,
                 amplifier_locations: [], amplifier_gains: [], amplifier_noise_factors: []):
        self.input_power = input_power
        self.unit_attenuation = unit_attenuation
        self.track_length = track_length
        self.amplifiers_count = amplifiers_count

        self.amplifier_locations = amplifier_locations
        self.amplifier_gains = amplifier_gains
        self.amplifier_noise_factors = amplifier_noise_factors

        self.constant = -58
        self.fiber_sections = self.calculate_fiber_sections()
        self.output_signal_power = self.calculate_output_signal_power()
        self.amplifier_noise_powers = self.calculate_noise_powers()

    def calculate_output_signal_power(self):
        g = 0
        for gi in self.amplifier_gains:
            g += gi

        l = 0
        for li in self.fiber_sections:
            a = li * self.unit_attenuation
            l += a

        osp = self.input_power + g - l

        return osp

    def calculate_fiber_sections(self):
        fs = []

        for i in range(len(self.amplifier_locations)):
            if i == 0:
                fs.append(self.amplifier_locations[i])

            else:
                fs.append(self.amplifier_locations[i] - self.amplifier_locations[i - 1])
        return fs

    def calculate_noise_powers(self):
        pn = []
        for i in range(self.amplifiers_count):
            pni: float = self.amplifier_noise_factors[i] + sum(self.amplifier_gains[i:]) \
                         + self.constant - self.unit_attenuation * (sum(self.fiber_sections[i + 1:]))
            print(f"Sum amplifier gains {i}: {sum(self.amplifier_gains[i:])}")
            print(f"Sum fiber sections {i}: {sum(self.fiber_sections[i + 1:])}\n")
            pn.append(pni)
        return pn

    def calculate_osnr(self):
        osnr: float
        # osnr = self.input_power
        output_power_mw = dBm2mW(self.output_signal_power)
        print("Output signal power: ", self.output_signal_power)
        print("PN1: ", self.amplifier_noise_powers[0])
        print("PN2: ", self.amplifier_noise_powers[1])

        pn_mw = []
        for i in self.amplifier_noise_powers:
            pni: float = dBm2mW(i)
            pn_mw.append(pni)
        amplifiers_noise_sum_mw = sum(pn_mw)
        osnr = 10 * log10(output_power_mw / amplifiers_noise_sum_mw)
        return osnr
