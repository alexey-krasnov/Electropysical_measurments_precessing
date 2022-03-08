import os
import glob
import numpy as np
import pandas as pd


def get_user_input() -> tuple:
    """Get the height and diameter of the sample from user in mm, transform them in m (SI).
    Calculate and return surface area and vacuum capacity."""
    while True:
        try:
            H = float(input("Enter the thickness of the sample in mm: ")) / 1000
            D = float(input("Enter the diameter of the sample in mm: ")) / 1000
        except ValueError:
            print("The values should be only digits, e.g. 1.2 and 13.5.")
        else:
            break
    return H, D


def calc_geometrical_params(H, D) -> tuple:
    """"Calculate the surface area S of the sample in m^2 and vacuum capacity C_0"""
    S = (np.pi * D * D) / 4
    C_0 = ((8.854 * (10**-12)) * S) / H
    return S, C_0


def data_reading():
    """Read data from the raw csv files in the current directory. Return DataFrame.
    Please, check the input files, they should be in the form of columns separated with ';'."""
    colnames = ['f', '|Z|', '-φ']  # Assign column names
    df = pd.read_csv(i, names=colnames, sep=";")
    return df


def data_processing(df, H, S, C_0):
    """Processing, calculation of the corresponding electrophysical values. Collecting data in the DataFrame."""
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
    return df


def export_data_excel(df):
    """Create one Excel file and store the electrophysical values at one temperature as the corresponding sheet."""
    df.to_excel(writer, sheet_name=f'{i.replace(".txt", "")}', index=False,
                columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu', 'σspec, Sm/cm', 'logσspec',
                         'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ', 'M\'', 'M\"'])


def export_data_zview(df, dir_name):
    """Make a directory and export data as txt files for Zview processing. The format of txt file is f, Z', -Z". """
    df["-Z\", Om·cm"] = df["Z\", Om·cm"] * (-1)
    df.to_csv(f'{dir_name}/{i}', columns=['f', 'Z\', Om·cm', "-Z\", Om·cm"], sep=' ', index=False, header=None)


def export_data_as_txt(df, dir_name):
    """Make a directory and export data as txt files with the electrophysical values
    for further plotting processing. """
    df.to_csv(f'{dir_name}/{i}', columns=['f', 'Z\', Om·cm', "Z\", Om·cm", 'logf', 'ω', 'Cu', 'φ', 'σu', 'σspec, Sm/cm',
                'logσspec', 'ε\'', 'ε\"', 'β\'', 'β\"', 'tanδ', 'M\'', 'M\"'], sep=';', index=False)

def makedir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print('Warning!!! Files have already been generated')


# Get name of current directory
current_dir = os.path.basename(os.getcwd())
# Check if you have already run the program and got all generated files.
generated_dirs = {'Zview_files': os.path.exists('Zview_files'),
                   'Data_txt': os.path.exists('Data_txt'),
                  }

if all([file==True for file in generated_dirs.values()]) \
        and glob.glob(f'{current_dir}*.xlsx'):
    print("You have already generated necessary files.")
else:
    print("'Warning!!! All existed files will be rewritten now...'")
    for dir, item in generated_dirs.items():
        if item == False:
            makedir(dir)

    height, diameter = get_user_input()
    geometrical_params = calc_geometrical_params(H=height, D=diameter)
    with pd.ExcelWriter(f'{current_dir}_h={height}_d={diameter}.xlsx') as writer:
        for i in sorted(glob.glob('*.txt')):
            current_data_frame = data_reading()
            data_processing(current_data_frame, height, *geometrical_params)
            export_data_excel(current_data_frame)
            export_data_zview(current_data_frame, dir_name='Zview_files')
            export_data_as_txt(current_data_frame, dir_name='Data_txt')
    print("Processing of your absorption data is finished successfully!")
