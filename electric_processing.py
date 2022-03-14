# -*- coding: UTF-8 -*-
"""Process raw data from RLC meter as txt files.
Get final Excel file with electrophysical characteristics,
directory 'Zview_files' with txt files for Zview program,
and directory 'Data_txt' with txt files for plotting or further study"""


import glob
from pathlib import Path
import numpy as np
import pandas as pd


def get_user_input() -> tuple:
    """Get the height and diameter of the sample from user in mm, transform them in m (SI).
    Calculate and return surface area and vacuum capacity."""
    while True:
        try:
            h = float(input("Enter the thickness of the sample in mm: ")) / 1000
            d = float(input("Enter the diameter of the sample in mm: ")) / 1000
        except ValueError:
            print("The values should be only digits, e.g. 1.2 and 13.5.")
        else:
            break
    return h, d


def calc_geometrical_params(h: float, d: float) -> tuple:
    """"Calculate the surface area S of the sample in m^2 and vacuum capacity C_0"""
    s = (np.pi * d ** 2) / 4
    c_0 = ((8.854 * (10**-12)) * s) / h
    return s, c_0


def data_reading():
    """Read data from the raw csv files in the current directory. Return DataFrame.
    Please, check the input files, they should be in the form of columns separated with ';'."""
    colnames = ['f', '|Z|', '-φ']  # Assign column names
    df = pd.read_csv(txt_file, names=colnames, sep=";")
    return df


def data_processing(df, h, s, c_0):
    """Processing, calculation of the corresponding electrophysical values. Collecting data in the DataFrame."""
    phi_radian = (df['-φ'] * np.pi * -1) / 180   # Transform phase angle into radian
    df['Z\''] = df['|Z|'] * np.cos(phi_radian)  # Real part of the impedance modulus|Z|
    df["Z\""] = df['|Z|'] * np.sin(phi_radian)  # Imaginary part of the impedance modulus|Z|
    df['Z\', Om·cm'] = df['|Z|'] * np.cos(phi_radian) * 100 * s / h  # Specific real part of the impedance modulus
    df["Z\", Om·cm"] = df['|Z|'] * np.sin(phi_radian) * 100 * s / h  # Specific imaginary part of the impedance modulus
    df['logf'] = np.log10(df['f'])  # lg of frequency
    df['ω'] = 2 * np.pi * df['f']  # circular frequency
    df['Cu'] = df["Z\""] / (df['ω'] * ((df['Z\''])**2 + (df["Z\""])**2))  # real capacity
    df['φ'] = df['-φ'] * (-1)  # Positive phase angle
    df['σu'] = df['Z\''] / ((df['Z\''])**2 + (df["Z\""])**2)  # Conductivity
    df['σspec, Sm/cm'] = (df['σu'] * h * 0.01) / s  # Specific conductivity in Sm/cm
    df['logσspec'] = np.log10(df['σspec, Sm/cm'])  # lg of specific conductivity
    df['ε\''] = df['Cu'] / c_0  # Real part of the dielectric constant
    df['ε\"'] = df['σu'] / (df['ω'] * c_0)  # Imaginary part of the dielectric constant
    df['β\''] = 1 / df['ε\'']
    df['β\"'] = 1 / df['ε\"']
    df['tanδ'] = df['ε\"'] / df['ε\'']  # Dielectric loss tangent
    df['M\''] = df['ω'] * c_0 * df["Z\""]  # Real part of the electric modulus
    df['M\"'] = df['ω'] * c_0 * df['Z\'']  # Imaginary part of the electric modulus
    return df


def export_data_excel(df):
    """Create one Excel file and store the electrophysical values at one temperature as the corresponding sheet."""
    df.to_excel(writer, sheet_name=f'{txt_file.replace(".txt", "")}', index=False,
                columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu', 'σspec, Sm/cm', 'logσspec',
                         'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ', 'M\'', 'M\"'])


def export_data_zview(df, dir_name):
    """Make a directory and export data as txt files for Zview processing. The format of txt file is f, Z', -Z". """
    df["-Z\", Om·cm"] = df["Z\", Om·cm"] * (-1)
    df.to_csv(f'{dir_name}/{txt_file}', columns=['f', 'Z\', Om·cm', "-Z\", Om·cm"], sep=' ', index=False, header=None)


def export_data_as_txt(df, dir_name):
    """Make a directory and export data as txt files with the electrophysical values
    for further plotting processing. """
    df.to_csv(f'{dir_name}/{txt_file}', columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu',
                                          'σspec, Sm/cm', 'logσspec', 'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ',
                                          'M\'', 'M\"'], sep=';', index=False)


def check_dirs_existence(dict_of_dirs: dict, work_dir: str):
    """Check existence of 'Zview_files' and 'Data_txt' directories.
    Ask user whether program should overwrite files or not"""
    def create_dirs(*args):
        """Create 'Zview_files' and 'Data_txt' directories"""
        for name in args:
            Path(name).mkdir(exist_ok=True)
            print(f'{name} directory has been created')
    if not (all(dict_of_dirs.values()) and glob.glob(f'{work_dir}*.xlsx')):
        return create_dirs(*dict_of_dirs.keys())

    user_asks = input('Do yoy want to overwrite all files? Type Yes/No: ')
    if user_asks in ('Yes', 'yes'):
        print('Warning!!! All existed files will be rewritten now...')
        return create_dirs(*dict_of_dirs.keys())
    return True


if __name__ == "__main__":
    generated_dirs = {'Zview_files': Path('Zview_files').exists(), 'Data_txt': Path('Data_txt').exists()}
    current_dir = Path.cwd().stem
    if check_dirs_existence(generated_dirs, current_dir):
        print("Electric_processing program is stopping...")
    else:
        print('Running...')
        height, diameter = get_user_input()
        geometrical_params = calc_geometrical_params(h=height, d=diameter)
        with pd.ExcelWriter(f'{current_dir}_h={height}_d={diameter}.xlsx') as writer:
            for txt_file in sorted(glob.glob('*.txt')):
                current_data_frame = data_reading()
                data_processing(current_data_frame, height, *geometrical_params)
                export_data_excel(current_data_frame)
                export_data_zview(current_data_frame, dir_name='Zview_files')
                export_data_as_txt(current_data_frame, dir_name='Data_txt')
        print("Processing of your absorption data is finished successfully!")
