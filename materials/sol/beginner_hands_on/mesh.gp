set datafile separator ','
set xlabel 'Grid divisions in each direction'
set ylabel 'Difference from reference (meV/atom)'
plot 'mesh.csv' every ::1 using 1:3 with linespoints notitle
