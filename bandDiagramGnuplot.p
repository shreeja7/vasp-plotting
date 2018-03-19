#!/usr/bin/gnuplot
#
# AUTHOR: Shreeja Das
# DATE:   08-12-2015
# gnuplot
# Inputs required: filename, nbands, Efermi
# Example: gnuplot -e "nb=8" -e "Ef=-8.7" -persist "bandDiagramGnuplot.p"
# Version 0.1: Removed need to subtract Ef
# 	Usage: gnuplot -e "nb=8" -persist "bandDiagramGnuplot.p"

reset
set xlabel 'k-point'
set ylabel 'E-Ef (eV)'
set title "Graphene(1x1) E vs. k Band Diagram"
set xzeroaxis
set grid x2tics
set x2tics 1000 format "" scale 0
#plot for [col=2:nb+1] "eigenBands.dat" u 1:(column(col)-Ef) notitle w l lw 3
plot for [col=2:nb+1] "eigenBands.dat" u 1:(column(col)) notitle w l lw 3
set terminal postscript eps enhanced color solid font 'Helvetica,20'
set out "band_diagram.eps"
#set terminal jpeg enhanced font helvetica 20
#set out "band_diagram.jpeg"
replot
