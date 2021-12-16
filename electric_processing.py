import os
import glob
import numpy as np
import pandas as pd


def get_user_input():
    global H, D, S, C_0
    """Get the thickness and diameter of the sample from user in mm, transform them in m (SI). 
    Calculate surface area and vacuum capacity"""
    while True:
        try:
            H = float(input("Enter the thickness of the sample in mm: ")) / 1000
            D = float(input("Enter the diameter of the sample in mm: ")) / 1000
        except ValueError:
            print("The values should be only digits, e.g. 1.2 and 13.5.")
        else:
            # Calculate the surface area of the sample in m^2
            S = (np.pi * D * D) / 4
            # Calculate vacuum capacity
            C_0 = ((8.854 * (10 ** -12)) * S) / H
            break


def data_reading():
    """Read data from the raw csv files in the current directory.
    Please, check the input files, they should be in form of columns separated with ';'."""
    global df
    colnames = ['f', '|Z|', '-φ']  # Assign column names
    df = pd.read_csv(i, names=colnames, sep=";")


def data_processing():
    """Processing, calculation of the corresponding electrophysical values. Writing data in the DataFrame."""
    phi_radian = (df['-φ'] * np.pi * -1) / 180   # Transform phase angle into radian
    df['Z\''] = df['|Z|'] * np.cos(phi_radian)  # Real part of the impedance modulus|Z|
    df["Z\""] = df['|Z|'] * np.sin(phi_radian)  # Imaginary part of the impedance modulus|Z|
    df['Z\', Om·cm'] = df['|Z|'] * np.cos(phi_radian) * 100 * S / H  # Specific real part of the impedance modulus
    df["Z\", Om·cm"] = df['|Z|'] * np.sin(phi_radian) * 100 * S / H  # Specific imaginary part of the impedance modulus
    df['logf'] = np.log10(df['f'])  # lg of frequency
    df['ω'] = 2 * np.pi * df['f']  # circular frequency
    df['Cu'] = df["Z\""] / (df['ω'] * ((df['Z\''])**2 + (df["Z\""])**2))  # real capacity
    df['φ'] = df['-φ'] * (-1)  # Positive phase angle
    df['σu'] = df['Z\''] / ((df['Z\''])**2 + (df["Z\""])**2)  # Conductivity
    df['σspec, Sm/cm'] = (df['σu'] * H * 0.01) / S  # Specific conductivity in Sm/cm
    df['logσspec'] = np.log10(df['σspec, Sm/cm'])  # lg of specific conductivity
    df['ε\''] = df['Cu'] / C_0  # Real part of the dielectric constant
    df['ε\"'] = df['σu'] / (df['ω'] * C_0)  # Imaginary part of the dielectric constant
    df['β\''] = 1 / df['ε\'']
    df['β\"'] = 1 / df['ε\"']
    df['tanδ'] = df['ε\"'] / df['ε\'']  # Dielectric loss tangent
    df['M\''] = df['ω'] * C_0 * df["Z\""]  # Real part of the electric modulus
    df['M\"'] = df['ω'] * C_0 * df['Z\'']  # Imaginary part of the electric modulus


def export_data_excel():
    """Create one Excel file and store the electrophysical values at one temperature as the corresponding sheet."""
    df.to_excel(writer, sheet_name=f'{i.replace(".txt", "")}', index=False,
                columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu', 'σspec, Sm/cm', 'logσspec',
                         'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ', 'M\'', 'M\"'])


def export_data_zview():
    """Make a directory and export data as txt files for Zview processing. The format of txt file is f, Z', -Z". """
    df["-Z\", Om·cm"] = df["Z\", Om·cm"] * (-1)
    df.to_csv(f'{out_dir}/{i}', columns=['f', 'Z\', Om·cm', "-Z\", Om·cm"], sep=' ', index=False, header=None)


current_dir = os.path.basename(os.getcwd())  # Get name of current directory
out_dir = 'Zview_files'  # Directory for Zview out files
# Check if you have already run the program and got the files.
if os.path.exists(out_dir) and glob.glob('*.xlsx'):
    print("You have already generated necessary files.")
else:
    get_user_input()
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        print('Zview files will be rewritten...')
    finally:
        # Generate or rewrite all files in any cases
        with pd.ExcelWriter(f'{current_dir}_h={H}_d={D}.xlsx') as writer:
            for i in sorted(glob.glob('*.txt')):
                data_reading()
                data_processing()
                export_data_excel()
                export_data_zview()
        print("Processing of your absorption data is finished successfully!")
