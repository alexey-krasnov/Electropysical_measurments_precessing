<h1 align="center">Welcome to Impedance_data_processing 👋</h1>
<p>
  <a href="https://twitter.com/AlekseiKrasnov4" target="_blank">
    <img alt="Twitter: AlekseiKrasnov4" src="https://img.shields.io/twitter/follow/AlekseiKrasnov4.svg?style=social" />
  </a>
</p>

# electric_processing
> Python script that automatically processes csv (.txt) files recorded by RLC impedance meter.

##  Prerequisites

This package requires:

- [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)
- [NumPy](https://docs.scipy.org/doc/numpy/index.html)

## Usage
`electric_processing` should be used within a directory containing your raw csv (.txt) files. These files should have the following format:
```python
X1;Y1;Z1 
X2;Y2;Z2
 .;.;.
 .;.;.
 .;.;.
```
where Xi is the recorded linear frequency, Yi - the impedance modulus, Zi - phase angle. Note that headers are absent.
Within the directory containing csv (.txt) files files, run:
```sh
electric_processing.py
```
it ask you to input the height and diameter of the cylindrical sample in mm.
Then program will read and process data from the csv files. After calculation programm creates one Excel file and store the electrophysical values at each temperature as the corresponding sheet. It also makes directories 'Zview_files' with .txt files for Zview program, and 'Data_txt' with txt files for plotting or further study. Please check the Example catalogue for sample input txt files and examples of the output files. 

## Questions, bug reports, feature requests

Please use the Github [issue tracker](https://github.com/alexey-krasnov/Impedance_data_processing/issues/) for any questions, feature requests or bug reports.

## Author

👤 **Aleksei Krasnov**

* Website: https://www.researchgate.net/profile/Aleksei-Krasnov
* Twitter: [@AlekseiKrasnov4](https://twitter.com/AlekseiKrasnov4)
* Github: [@alexey-krasnov](https://github.com/alexey-krasnov)
* LinkedIn: [@aleksei-krasnov-b53b2ab6](https://linkedin.com/in/aleksei-krasnov-b53b2ab6)
