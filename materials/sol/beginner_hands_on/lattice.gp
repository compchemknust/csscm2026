set datafile separator ','
set xlabel 'Lattice length (angstrom)'
set ylabel 'Energy relative to sampled minimum (meV/atom)'
plot 'lattice.csv' every ::1 using 1:3 with linespoints notitle
