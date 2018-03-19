# This program reads EIGENVAL from VASP output and generates eigenval.dat file
# which stores the energy eigen values in
# the format ---
# Kpoints	EnergyForBand1	EnergyForBand2	...	EnergyForbandn
# Author: Shreeja Das
# Date:   08-12-2015
# Version 0.1: Dt. 26-08-2017
#	Output file contains energy data after subtracting fermi energy from it. E-Ef
#	Change log: Inserted code for fetching fermi energy from OUTCAR and subtracted #		    it from energy values

import numpy
from numpy import *
import re
infile = open('EIGENVAL','r')
#outfile = open('eigenval.dat','w')
for i in range(5):             #Skip read the first few lines of EIGENVAL
 infile.readline()
line = infile.readline()
nelectrons     = int(line.split()[0])  # no. of electrons per unit cell
nkpts          = int(line.split()[1])  # no. of k points taken
nbands         = int(line.split()[2])  # no. of bands i.e. no. of eigenvalues per k-point
print nelectrons, ' electrons'
print nkpts, ' kpoints'
print nbands, ' bands = eigenvalues per k-point'

outcar=open('OUTCAR','r')		# Inserted on 26-08-2017, SD
for line in outcar:
 if re.search('E-fermi',line):
  print line
  efermi=float(line.split()[2])
outcar.close()

eigenval_array = numpy.zeros((nkpts,nbands+1))  # initialise an array to store the eigenvalues
loop =0
while loop < nkpts:
 print loop
 line = infile.readline()
 #print [ord(c) for c in line]
 line = infile.readline()
 #print line
 if [ord(c) for c in line] != [32,10]:  # check for blank space
  if (line.split()[2] is not None) :    # check if its the k points line
   eigenval_array[loop,0] = loop+1	# kpoint number
   '''for k in range(nbands):
    eigenval_array[(k)*nkpts+loop,1] = float(line.split()[0])  #kx
    eigenval_array[(k)*nkpts+loop,2] = float(line.split()[1])  #ky
    eigenval_array[(k)*nkpts+loop,3] = float(line.split()[2])  #kz'''
   for j in range(nbands):
    line = infile.readline()
    # print line
    #eigenval_array[loop,j+1] = float(line.split()[1])  # Energy of band j; Commented on 26-08-2017, SD
    eigenval_array[loop,j+1] = float(line.split()[1])-efermi  # Energy of band j
   loop = loop+1
print eigenval_array
# Write values to outfile
commentstr = ''
for h in range(nbands):
 commentstr= str(commentstr)+'Band'+str(h+1)+'\t'
savetxt('eigenBands.dat', eigenval_array, header='kpoint'+'\t'+commentstr)
infile.close()
