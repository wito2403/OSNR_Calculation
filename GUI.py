import tkinter as tk
from OSNR_calculator import OSNRCalculator


class GUI:
    def __init__(self):
        self.ctr = 1

        def input_amplifiers_data():
            amplifier_locations = []
            amplifier_gains = []
            amplifier_noise_factors = []

            wavelength = float(e_wavelength.get())
            wavelength_delta = float(e_wavelength_delta.get())
            input_power = float(e_input_power.get())
            unit_attenuation = float(e_unit_attenuation.get())
            track_length = float(e_track_length.get())
            amplifiers_count = int(e_amplifiers_count.get())

            tk.Label(root, text=f"Położenie wzmacniacza {1} [km]: ", pady=10, width=40).grid(row=12)
            tk.Label(root, text=f"Wzmocnienie wzmacniacza G{1} [dB]: ", pady=10, width=40).grid(row=13)
            tk.Label(root, text=f"Współczynnik szumów wzmacniacza N{1} [dB]: ", pady=10, width=40).grid(row=14)

            e_amplifier_location = tk.Entry(root, width=50)
            e_amplifier_gain = tk.Entry(root, width=50)
            e_amplifier_noise_factor = tk.Entry(root, width=50)

            e_amplifier_location.grid(row=12, column=1)
            e_amplifier_gain.grid(row=13, column=1)
            e_amplifier_noise_factor.grid(row=14, column=1)

            def append_data():
                amplifier_locations.append(float(e_amplifier_location.get()))
                amplifier_gains.append(float(e_amplifier_gain.get()))
                amplifier_noise_factors.append(float(e_amplifier_noise_factor.get()))

                e_amplifier_location.delete(0, 'end')
                e_amplifier_gain.delete(0, 'end')
                e_amplifier_noise_factor.delete(0, 'end')

            def next_amplifier():
                append_data()
                self.ctr += 1

                tk.Label(root, text=f"Położenie wzmacniacza {self.ctr} [km]: ", pady=10, width=40).grid(row=12)
                tk.Label(root, text=f"Wzmocnienie wzmacniacza G{self.ctr} [dB]: ", pady=10, width=40).grid(row=13)
                tk.Label(root, text=f"Współczynnik szumów wzmacniacza N{self.ctr} [dB]: ", pady=10, width=40).grid(
                    row=14)

                if self.ctr == amplifiers_count:
                    b1.grid_forget()
                    tk.Button(root, command=calculate_osnr, text="Oblicz OSNR").grid(row=15, column=1)

            def calculate_osnr():
                append_data()
                print(f"\n================== NOWA KALKULACJA ==================\n")
                print(f"Moc wejściowa [dBm]: {input_power}")
                print(f"Tłumienność jednotkowa [dB/km]: {unit_attenuation}")
                print(f"Długość toru [km]: {track_length}")
                print(f"Liczba wzmacniaczy: {amplifiers_count}")
                print(f"Położenia wzmacniaczy [km]: {amplifier_locations}")
                print(f"Wzmocnienia [dB]: {amplifier_gains}")
                print(f"Współczynniki szumów [dB]: {amplifier_noise_factors}")

                calculator = OSNRCalculator(input_power, unit_attenuation, track_length, amplifiers_count,
                                            amplifier_locations, amplifier_gains, amplifier_noise_factors,
                                            wavelength, wavelength_delta)

                print(f"Odcinki światłowodu między wzmacniaczami [km]:  {calculator.fiber_sections}")

                OSNR = calculator.calculate_osnr()
                tk.Label(root, text=f"OSNR: ", width=40).grid(row=16, column=0)
                tk.Label(root, text=f"{OSNR.__round__(2)} [dB]", pady=30, width=40).grid(row=16, column=1)
                pass

            # show relevant button
            if amplifiers_count == 1:
                tk.Button(root, command=calculate_osnr, text="Oblicz OSNR").grid(row=15, column=1)
                pass
            else:
                b1 = tk.Button(root, command=next_amplifier, text="Następny wzmacniacz")
                b1.grid(row=15, column=1)

        def restart():
            root.destroy()
            self.__init__()

        root = tk.Tk()
        root.title('[SIS] Program obliczający OSNR na wyjściu toru optycznego')
        root.geometry('800x550+550+50')

        tk.Label(root, text="Długość fali λ [nm]: ", pady=10, width=40).grid(row=0)
        tk.Label(root, text="Szerokość pasma filtru Δλ [nm]: ", pady=10, width=40).grid(row=1)
        pe = u'P\u2099'  # low index n
        tk.Label(root, text=f"Moc nadajnika {str(pe)} [dBm]: ", pady=10, width=40).grid(row=2)
        tk.Label(root, text="Tłumienność jednostkowa α [dB/km]: ", pady=10, width=40).grid(row=3)
        tk.Label(root, text="Całkowita długość toru [km]: ", pady=10, width=40).grid(row=4)
        tk.Label(root, text="Liczba wzmacniaczy optycznych: ", pady=10, width=40).grid(row=5)

        e_wavelength = tk.Entry(root, width=50)
        e_wavelength_delta = tk.Entry(root, width=50)
        e_input_power = tk.Entry(root, width=50)
        e_unit_attenuation = tk.Entry(root, width=50)
        e_track_length = tk.Entry(root, width=50)
        e_amplifiers_count = tk.Entry(root, width=50)

        e_wavelength.grid(row=0, column=1)
        e_wavelength_delta.grid(row=1, column=1)
        e_input_power.grid(row=2, column=1)
        e_unit_attenuation.grid(row=3, column=1)
        e_track_length.grid(row=4, column=1)
        e_amplifiers_count.grid(row=5, column=1)

        tk.Button(root,
                  text='Zamknij program',
                  command=root.quit).grid(row=0,
                                          column=5,
                                          sticky=tk.W,
                                          padx=80)
        tk.Button(root,
                  text='Nowa kalkulacja',
                  command=restart).grid(row=1,
                                        column=5,
                                        sticky=tk.W,
                                        padx=80)

        tk.Button(root,
                  text='Rozpocznij wprowadzanie danych wzmacniaczy', command=input_amplifiers_data).grid(row=6,
                                                                                                         column=1,
                                                                                                         sticky=tk.W,
                                                                                                         pady=20)

        tk.mainloop()
