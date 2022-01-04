from scipy.constants import c, h
from math import log10


# Function to convert from dBm to mW
def dBm2mW(dBm):
    return 10 ** ((dBm) / 10.)


class OSNRCalculator:
    def __init__(self, input_power, unit_attenuation, track_length, amplifiers_count,
                 amplifier_locations: [], amplifier_gains: [], amplifier_noise_factors: [],
                 wavelength=1550, delta_wavelength=0.1):
        self.input_power = input_power
        self.unit_attenuation = unit_attenuation
        self.track_length = track_length
        self.amplifiers_count = amplifiers_count

        self.amplifier_locations = amplifier_locations
        self.amplifier_gains = amplifier_gains
        self.amplifier_noise_factors = amplifier_noise_factors

        self.wavelength = wavelength * 10 ** (-9)  # express in nanometers
        self.delta_wavelength = delta_wavelength * 10 ** (-9)  # express in nanometers

        self.constant = self.calculate_constant()
        self.fiber_sections = self.calculate_fiber_sections()
        self.output_signal_power = self.calculate_output_signal_power()
        self.amplifier_noise_powers = self.calculate_noise_powers()

    def calculate_constant(self):
        freq = c / self.wavelength
        delta_freq = c * self.delta_wavelength / pow(self.wavelength, 2)
        constant = 10 * log10(h * freq * delta_freq) + 30  # express in dBm
        print(f"\n10log10(hfΔf):  {constant.__round__(2)} dBm\n")
        return constant

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
        # num_zeros = 0
        # for j in range(len(self.amplifier_locations)-1):
        #     if j == 0:
        #         if self.amplifier_locations[j] == float(0):
        #             num_zeros += 1
        #     else:
        #         if self.amplifier_locations[j] == self.amplifier_locations[j+1]:
        #             print("\n INKREMENTACJA NUM ZEROS")
        #             num_zeros += 1
        #             pass



        # if self.amplifier_locations[0] == float(0):
        #     iterator = len(self.amplifier_locations) + 1
        #     # print("float == 0")
        # else:
        #     iterator = len(self.amplifier_locations)
        #     # print("cos innego")

        # for i in range(len(self.amplifier_locations) + num_zeros):
        #     if i == 0:
        #         fs.append(self.amplifier_locations[i])
        #
        #     elif i == len(self.amplifier_locations):
        #         fs.append(self.track_length - self.amplifier_locations[i - 1])
        #     else:
        #         fs.append(self.amplifier_locations[i] - self.amplifier_locations[i - 1])

        for i in range(self.amplifiers_count):
            if i == 0:
                if self.amplifier_locations[i] == float(0):
                    fs.append(float(0))
                else:
                    fs.append(self.amplifier_locations[i])
            else:
                fs.append(self.amplifier_locations[i] - self.amplifier_locations[i - 1])
                if i == (len(self.amplifier_locations) - 1) and self.amplifier_locations[i] != self.track_length:

                    fs.append(self.track_length - self.amplifier_locations[i])
                    break

                # if self.amplifier_locations[i] == self.amplifier_locations[i - 1]:
                #     fs.append(float(0))
                # else:
        # print(fs)
        return fs

    def calculate_noise_powers(self):
        pn = []
        for i in range(self.amplifiers_count):
            pni: float = self.amplifier_noise_factors[i] + sum(self.amplifier_gains[i:]) \
                         + self.constant - self.unit_attenuation * (sum(self.fiber_sections[i + 1:]))
            # print(f"Sum amplifier gains {i}: {sum(self.amplifier_gains[i:])}")
            # print(f"Sum fiber sections {i}: {sum(self.fiber_sections[i + 1:])}\n")
            pn.append(pni)
        return pn

    def calculate_osnr(self):
        osnr: float
        # osnr = self.input_power
        output_power_mw = dBm2mW(self.output_signal_power)
        print("Output signal power: ", self.output_signal_power.__round__(2))

        for i in range(len(self.amplifier_noise_powers)):
            print(f"PN{i+1}: {self.amplifier_noise_powers[i].__round__(2)}")

        pn_mw = []
        for i in self.amplifier_noise_powers:
            pni: float = dBm2mW(i)
            pn_mw.append(pni)
        amplifiers_noise_sum_mw = sum(pn_mw)
        osnr = 10 * log10(output_power_mw / amplifiers_noise_sum_mw)
        return osnr
