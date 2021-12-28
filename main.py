# from tkinter import *
#
# root = Tk()
# root.title('[SIS] Program obliczający OSNR na wyjściu toru optycznego')
# root.geometry("600x400")
#
# e = Entry(root, width=50)
# e.pack()
# e.insert(0, "Moc wejściowa")
#
# e1 = Entry(root, width=50)
# e1.pack()
# e1.insert(0, "Wzmocnienie")
#
#
# def my_click():
#     g = int(e.get()) + int(e1.get())
#     my_label = Label(root, text=f"📃 Paper LOOOOK {g}")
#     my_label.pack()
#
#
# my_button = Button(root, text="Enter your name", command=my_click)
# my_button.pack()
#
# root.mainloop()

# -moc sygnału na wejściu światłowodu,
# -tłumienność jednostkowa światłowodu (w dB/km),
# -całkowita długość toru (w km),
# -położenie wzmacniaczy optycznych (ich odległość od początku światłowodu wyrażona w kilometrach),
# -wartości wzmocnienia i współczynnika szumów dla poszczególnych wzmacniaczy optycznych
# (mogą być różne dla różnych wzmacniaczy

import tkinter as tk

amplifier_locations = []
amplifier_gains = []
amplifier_noise_factors = []


def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e_input_power.get(), e_unit_attenuation.get()))


# global next_counter
ctr = 1


def input_amplifiers_data():
    amplifiers_count = int(e_amplifiers_count.get())

    tk.Label(root, text=f"Położenie wzmacniacza {1} [km]: ", pady=10, width=40).grid(row=10)
    tk.Label(root, text=f"Wzmocnienie wzmacniacza {1} [dB]: ", pady=10, width=40).grid(row=11)
    tk.Label(root, text=f"Współczynnik szumów wzmacniacza {1}: ", pady=10, width=40).grid(row=12)

    e_amplifier_location = tk.Entry(root, width=50)
    e_amplifier_gain = tk.Entry(root, width=50)
    e_amplifier_noise_factor = tk.Entry(root, width=50)

    e_amplifier_location.grid(row=10, column=1)
    e_amplifier_gain.grid(row=11, column=1)
    e_amplifier_noise_factor.grid(row=12, column=1)

    def append_data():
        amplifier_locations.append(float(e_amplifier_location.get()))
        amplifier_gains.append(float(e_amplifier_gain.get()))
        amplifier_noise_factors.append(float(e_amplifier_noise_factor.get()))

    def erase():
        e_amplifier_location.delete(0, 'end')
        e_amplifier_gain.delete(0, 'end')
        e_amplifier_noise_factor.delete(0, 'end')


    def next_amplifier():
        global ctr
        # erase()
        append_data()
        if ctr != 1:
            erase()
        ctr += 1


        tk.Label(root, text=f"Położenie wzmacniacza {ctr} [km]: ", pady=10, width=40).grid(row=10)
        tk.Label(root, text=f"Wzmocnienie wzmacniacza {ctr} [dB]: ", pady=10, width=40).grid(row=11)
        tk.Label(root, text=f"Współczynnik szumów wzmacniacza {ctr}: ", pady=10, width=40).grid(row=12)

        print(ctr, amplifiers_count)
        if ctr == amplifiers_count:
            amplifier_locations.append(float(e_amplifier_location.get()))
            amplifier_gains.append(float(e_amplifier_gain.get()))
            amplifier_noise_factors.append(float(e_amplifier_noise_factor.get()))

            b1.grid_forget()
            tk.Button(root, command=calculate_osnr, text="Oblicz OSNR").grid(row=13, column=1)



    b1 = tk.Button(root, command=next_amplifier, text="Następny wzmacniacz")
    b1.grid(row=13, column=1)


def calculate_osnr():
    print(amplifier_locations)
    print(amplifier_gains)
    print(amplifier_noise_factors)
    OSNR = 123
    tk.Label(root, text=f"OSNR: ", pady=30, width=40).grid(row=14, column=0)
    tk.Label(root, text=f"{OSNR}", pady=30, width=40).grid(row=14, column=1)
    pass


def restart():
    root.destroy()
    root.__init__()


root = tk.Tk()
root.title('[SIS] Program obliczający OSNR na wyjściu toru optycznego')
root.geometry("800x600")

tk.Label(root, text="Moc sygnału na wejściu światłowodu [dBm]: ", pady=10, width=40).grid(row=0)
tk.Label(root, text="Tłumienność jednostkowa światłowodu [dB/km]: ", pady=10, width=40).grid(row=1)
tk.Label(root, text="Całkowita długość toru [km]: ", pady=10, width=40).grid(row=2)
tk.Label(root, text="Liczba wzmacniaczy optycznych: ", pady=10, width=40).grid(row=3)

e_input_power = tk.Entry(root, width=50)
e_unit_attenuation = tk.Entry(root, width=50)
e_track_length = tk.Entry(root, width=50)
e_amplifiers_count = tk.Entry(root, width=50)

e_input_power.grid(row=0, column=1)
e_unit_attenuation.grid(row=1, column=1)
e_track_length.grid(row=2, column=1)
e_amplifiers_count.grid(row=3, column=1)

tk.Button(root,
          text='Zamknij program!',
          command=root.quit).grid(row=0,
                                  column=5,
                                  sticky=tk.W,
                                  padx=80)
# tk.Button(root,
#           text='Od początku!',
#           command=restart).grid(row=1,
#                                 column=5,
#                                 sticky=tk.W,
#                                 padx=80)
tk.Button(root,
          text='Rozpocznij wprowadzanie danych wzmacniaczy', command=input_amplifiers_data).grid(row=4,
                                                                                                 column=1,
                                                                                                 sticky=tk.W,
                                                                                                 pady=20)

tk.mainloop()
