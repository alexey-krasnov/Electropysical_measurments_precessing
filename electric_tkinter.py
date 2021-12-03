import pandas as pd
import glob
from math import pi
import numpy as np
import os
from tkinter import *

def get_user_input():
    global h, d, s, c_0
    """Get the thickness and diameter of the sample from user. Calculate surface area and vacuum capacity"""
    # Get the thickness and diameter of the sample in mm, transform them in m
    while True:
        try:
            h = float(input("Enter the thickness of the sample in mm: ")) / 1000
            d = float(input("Enter the diameter of the sample in mm: ")) / 1000
        except ValueError:
            print("The values should be only digits, e.g. 1.2 and 13.5.")
        else:
            # Calculate the surface area of the sample in m^2
            s = (pi * d * d) / 4
            # Calculate vacuum capacity
            c_0 = ((8.854 * (10 ** -12)) * s) / h
            break


def data_processing():
    """Read data from the raw csv files in the current directory, processing, and writing data in the DataFrame."""
    global df
    colnames = ['f', '|Z|', '-φ']  # Assign column names
    df = pd.read_csv(i, names=colnames, sep=";")
    phi_radian = (df['-φ'] * pi * -1) / 180   # Transform phase angle into radian
    # Calculation of the corresponding electrophysical values.
    df['Z\''] = df['|Z|'] * np.cos(phi_radian)  # Real part of impedance Z
    df["Z\""] = df['|Z|'] * np.sin(phi_radian)  # Imaginary part of impedance
    df['Z\', Om·cm'] = df['|Z|'] * np.cos(phi_radian) * 100 * s / h  # Specific real part of impedance Z
    df["Z\", Om·cm"] = df['|Z|'] * np.sin(phi_radian) * 100 * s / h  # Specific imaginary part of impedance Z
    df['logf'] = np.log10(df['f'])  # lg of frequency
    df['ω'] = 2 * pi * df['f']  # circular frequency
    df['Cu'] = df["Z\""] / (df['ω'] * ((df['Z\''])**2 + (df["Z\""])**2))  # real capacity
    df['φ'] = df['-φ'] * (-1)  # Positive phase angle
    df['σu'] = df['Z\''] / ((df['Z\''])**2 + (df["Z\""])**2)  # Conductivity
    df['σspec, Sm/cm'] = (df['σu'] * h * 0.01) / s  # Specific conductivity in Sm/cm
    df['ε\''] = df['Cu'] / c_0  # real part of dielectric constant
    df['ε\"'] = df['σu'] / (df['ω'] * c_0)  # imaginary part od dielectric constant
    df['β\''] = 1 / df['ε\'']
    df['β\"'] = 1 / df['ε\"']
    df['tanδ'] = df['ε\"'] / df['ε\'']  # dielectric loss tangent
    df['M\''] = df['ω'] * c_0 * df["Z\""]  # real part of electric modulus
    df['M\"'] = df['ω'] * c_0 * df['Z\'']  # imaginary part of electric modulus


def export_data_excel():
    """Create one excel file and store the electrophysical values at one temperature as the corresponding sheet."""
    df.to_excel(writer, sheet_name=f'{i.replace(".txt", "")}', index=False,
                columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu', 'σspec, Sm/cm',
                         'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ', 'M\'', 'M\"'])


def export_data_zview():
    """Make a directory ans export data as txt files for Zview processing. The format of txt file is f, Z', -Z". """
    df["-Z\", Om·cm"] = df["Z\", Om·cm"] * (-1)
    df.to_csv(f'{outdir}/{i}', columns=['f', 'Z\', Om·cm', "-Z\", Om·cm"], sep=' ', index=False, header=None)


current_dir = os.path.basename(os.getcwd())  # Get name of current directory
outdir = 'Zview_files'  # Directory for Zview out files
# Check if you have already run the program and got the files.
if f'{current_dir}.xlsx' and outdir in glob.glob('*'):
    print("You have already generated necessary files.")
else:
    get_user_input()
    os.mkdir(outdir)
    with pd.ExcelWriter(f'{current_dir}_h={h}_d={d}.xlsx') as writer:
        for i in sorted(glob.glob('*.txt')):
            data_processing()
            export_data_excel()
            export_data_zview()
    print("Processing of your absorption data is finished successfully!")

# GUI interface
root = Tk()
# Set geometry
root.geometry('800x400')
# Add Labels, Button and Frames
Label(root, text='Electric processing', font="Helvetica 20 bold", fg="Green").pack(pady=10)

# Frame 1
frame1 = Frame(root)
Label(frame1, text='Type Word', font="Helvetica 15 bold").pack(side=LEFT)
word = Entry(frame1, font='Helvetica 15 bold')
word.pack()
frame1.pack(pady=10)

# Frame 2
frame2 = Frame(root)
Label(frame2, text='Meaning', font="Helvetica 10 bold").pack(side=LEFT)
meaning = Label(frame2, text='', font='Helvetica 10')
meaning.pack()
frame2.pack(pady=10)

# Frame 3
frame3 = Frame(root)
Label(frame3, text='Synonym', font="Helvetica 10 bold").pack(side=LEFT)
synonym = Label(frame3, text='', font='Helvetica 10')
synonym.pack()
frame3.pack(pady=10)

# Frame 4
frame4 = Frame(root)
Label(frame4, text='Antonym', font="Helvetica 10 bold").pack(side=LEFT)
antonym = Label(frame4, text='', font='Helvetica 10')
antonym.pack()
frame4.pack(pady=10)

#  Make Button key
Button(root, text="Submit", font="Helvetica 15 bold", command=dict).pack()
root.mainloop()
