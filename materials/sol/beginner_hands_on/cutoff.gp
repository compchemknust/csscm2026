set datafile separator ','
set xlabel 'Wavefunction cutoff (Ry)'
set ylabel 'Difference from reference (meV/atom)'
plot 'cutoff.csv' every ::1 using 1:3 with linespoints notitle
