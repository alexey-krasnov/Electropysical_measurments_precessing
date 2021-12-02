import pandas as pd
import glob
from math import pi
import numpy as np
import os


def data_processing():
    """Read data from the raw csv files in the current directory, processing, and writing data in the DataFrame."""
    global df
    colnames = ['f', '|Z|', '-φ']  # Assign column names
    df = pd.read_csv(i, names=colnames, sep=";")
    phi_radian = (df['-φ'] * pi * -1) / 180   # Transform phase angle into radian
    # Calculation of the corresponding electrophysical values.
    df['Z\', Om·cm'] = df['|Z|'] * np.cos(phi_radian) * 100 * s / h
    df["Z\", Om·cm"] = df['|Z|'] * np.sin(phi_radian) * 100 * s / h


def export_data_zview():
    """Make a directory ans export data as txt files for Zview processing. The format of txt file is f, Z', -Z". """
    df["-Z\", Om·cm"] = df["Z\", Om·cm"] * (-1)
    df.to_csv(f'{outdir}/{i}', columns=['f', 'Z\', Om·cm', "-Z\", Om·cm"], sep=' ', index=False, header=None)


def export_data_excel():
    """Create one excel file and store the electrophysical values at one temperature as the corresponding sheet."""
    df.to_excel(writer, sheet_name=f'{i}', index=False)


# Get the thikness and diameter of the sample in mm, transform them in m
h = float(input("Enter the thikness of the sample in mm "))/1000
d = float(input("Enter the diameter of the sample in mm "))/1000
# Calculate the surface area of the sample in m^2
s = (pi * d * d) / 4

# Check if you have already run the program and got the files.
current_dir = os.getcwd()
outdir = 'Zview_files'
try:
    os.mkdir(outdir)
except FileExistsError:
    print("You have already generated necessary files.")
finally:
    with pd.ExcelWriter(f'out.xlsx') as writer:
        for i in glob.glob('*.txt'):
            data_processing()
            export_data_zview()
            export_data_excel()

print("Processing of your absorption data is finished successfully!")
