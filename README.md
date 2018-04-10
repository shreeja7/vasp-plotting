# vasp-plotting
Some codes to convert VASP output files into easily readable data files for plotting. 

1. readeigenSingleFileOP.py: 
Usage - python readeigenSingleFileOP.py
This script reads the band energy and k-points from EIGENVAL file, then subtracts the energies from the fermi energy 
(obtained from OUTCAR) and stores them all in a single text file called eigenBands.dat in the following format:
Kpoints	EnergyForBand1	EnergyForBand2	...	EnergyForbandn

You can now read this file to plot band diagrams using codes of your choice.

2. bandDiagramGnuplot.p
Usage - gnuplot -e "nb=8" -persist "bandDiagramGnuplot.p"
Small gnuplot code to quickly plot and save band diagrams. Reads the eigenBands.dat file from <1>
To convert the eps output into 300 dpi jpg: 
convert -density 300 band_diagram.eps -flatten band_diagram.jpg
