# -*- coding: utf-8 -*-
# AUTHOR: Shreeja Das
# DATE:   20.11.2018
# NAME: pbands_v4.py
# PURPOSE: Plot projected bands 
# USAGE:1. Set the values of  systemname, ele_ip, orb_ip, up_color, down_color in this file
#		2. Run using $python pbands_v4.py
# CHANGE: Added check for spin-polarized for correct legend.
'''
	Program for plotting projected bandstructures of elements and their orbitals 
	into separate figures. The typical usage is:
		FUNCTIONALITY (20.11.2018):
			1. Choose only one atom and one of its orbital out of the structure for which you want the spin-up and spin-down contributions. 
			For e.g. in a system of graphene and h-BN on Ni(111) plane, say we want to find the projection of C-p or C-s or Ni-d or B-px or C-pz or Ni-f0 etc. It will plot one figure for each.
			2. Select any one orbital out of the following:
				s, px, py, pz, p, 
				dxy, dyz, dz2, dxz, dx2, d, 
				f_3, f_2, f_1, f0, f1, f2, f3, f
			3. Specify the colors of spin-up and spin-down for each figure viz. C-s, C-p, B-px etc.
            4. All the above values are stored as lists named ele_ip, orb_ip, up_color and down_color
			5. Pass these as arguments to BSPlotterProjected.get_projected_plots_dots_patom_pmorb function in the modified plotter.py module
				5.1 plotter.py module has been modified to remove subplots and some bugs
			6. Save all the figures as 600 dpi png
	
	
'''

import pymatgen as mg
from pymatgen.io.vasp.outputs import BSVasprun, Vasprun
from pymatgen import Spin
from pymatgen.electronic_structure.plotter import BSPlotter, BSDOSPlotter, DosPlotter, BSPlotterProjected

import matplotlib.pyplot as plt
import time

## Uncomment this section if running in Windows
#run = BSVasprun("C:\\Users\\IIT\\OneDrive\\MihirNiBNGrPaper\\band\\vasprun.xml", parse_projected_eigen=True) 	#BSVasprun object
#bs = run.get_band_structure("C:\\Users\\IIT\\OneDrive\\MihirNiBNGrPaper\\band\\KPOINTS")				#BandStructureSymmLine object

run = BSVasprun("../band/vasprun.xml",parse_projected_eigen=True)   #BSVasprun object
bs=run.get_band_structure("../band/KPOINTS")  #BandStructureSymmLine object
print("********************************************************************")
print("Struture:\n ",bs.structure)
print("********************************************************************")
print("Fermi level= ", bs.efermi)

bsplot = BSPlotterProjected(bs)						#BSPlotterProjected object

print("********************************************************************")
print("Available elements--> ", set(run.atomic_symbols))

## Uncomment for user interactive input
#element_selected=input("Select one element: ")
#orbital_selected=input("Enter orbital --> s, px, py, pz, p, dxy, dyz, dz2, dxz, dx2, d, f_3, f_2, f_1, f0, f1, f2, f3, f\n")

## List of inputs to atom_selected and orbital_selected
systemname="AlBNGr"
ele_ip=['C','C','B','B','N','N','Al','Al','Al']		#can be obtained from set(BSVasprun().atomic_symbols))
orb_ip=['s','p','s','p','s','p','s','p','d']
up_color=  ['#0089FF','#C30AFF','#C2FF0A','#0AFF6A','#17FF0A','#0A84FF','#D800FF','#FF3100','#FFF200']
down_color=['#FFF000','#00D4FF','#FF6D00','#FFD400','#005DFF','#FF0090','#FF4000','#FFBE00','#0028FF']

for j in range(len(ele_ip)):
    element_selected=ele_ip[j]
    orbital_selected=orb_ip[j]
    spin_upcol=up_color[j]
    spin_downcol=down_color[j]

    natoms=run.atomic_symbols.count(element_selected)
    start_time = time.time()
	# Set orbitals
    if orbital_selected =='p':
        orbs=['px','py','pz']
        sum_morbs={element_selected:orbs}
    elif orbital_selected=='d':
        orbs=['dxy','dyz','dz2','dxz','dx2']
        sum_morbs={element_selected:orbs}
    elif orbital_selected=='f':
        orbs=['f_3', 'f_2', 'f_1', 'f0', 'f1', 'f2', 'f3', 'f']
        sum_morbs={element_selected:orbs}
    else:
        orbs=[orbital_selected]
        sum_morbs=None

    # Set dictio 
    if element_selected in str(bs.structure.types_of_specie):
        print("I found your element in the structure!")
        dictio={element_selected:orbs}
    else:
        raise ValueError("%s you entered is not present in the structure" % element_selected)
    print("You have selected: ",dictio)

    # Set dictpa
    sites=[]
    c=0
    for i in range(bs.structure.num_sites):
        if element_selected == str(bs.structure.sites[i].specie):
            sites.append(i+1)
            c=c+1
    dictpa={element_selected:sites}
    print(dictpa)

    # Set sum_atoms
    if c==1:
        sum_atoms=None
    else:
        sum_atoms=dictpa

    print("Plotting for : ",element_selected, orbital_selected, "orbital ",  "at ", natoms, "sites...")


    bsplotpy=bsplot.get_projected_plots_dots_patom_pmorb( dictio, \
														  dictpa, spin_upcol, spin_downcol, \
														  sum_atoms, \
														  sum_morbs, \
														  ylim=(-5, 5), \
														  zero_to_efermi=True)					
														  #matplotlib object
	   

    title="Projected Band Structure of: " + element_selected +" "+ orbital_selected + " orbital."

    ## add some features
    ax = bsplotpy.gca()
    ax.set_title(title, fontsize=20)
    xlim = ax.get_xlim()
    ax.set_xlim(list(xlim))
    ax.hlines(0, xlim[0], xlim[1], linestyles="dashed", color="black")
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    
	#Legend testing
    # plt.plot(range(5),range(5))
    # ax=plt.gca()
    # plt.savefig("test.png", dpi=600)

    ### add legend and save figure as .png
    if bs.is_spin_polarized:
        ax.plot((), (), color=spin_upcol, marker='o',markersize=10, linestyle='none', label="\u2191", alpha=0.6)
        ax.plot((), (), color=spin_downcol, marker='o',markersize=10, linestyle='none', label="\u2193", alpha=0.6)
        ax.legend(fontsize=20, loc="upper left")
    figname=systemname+"_"+element_selected + "-" + orbital_selected+".png"
    bsplotpy.savefig(figname, dpi=600)
    
	
    print("%f seconds" % (time.time() - start_time))
    print("+++++++++++++++++++++DONE: ",figname," :DONE++++++++++++++++++++++++")
    print("********************************************************************\n\n")
    
	
