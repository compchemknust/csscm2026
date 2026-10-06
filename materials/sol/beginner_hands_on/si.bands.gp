set xlabel 'Path distance (units of 2*pi/A)'
set ylabel 'Energy (eV, file reference)'
set xtics ('L' 0, 'Gamma' 0.8660254, 'X' 1.8660254)
plot 'si.bands.dat.gnu' using 1:2 with lines notitle
