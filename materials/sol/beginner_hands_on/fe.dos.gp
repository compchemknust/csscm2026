set xlabel 'Energy (eV, file reference)'
set ylabel 'DOS (states/eV/cell)'
plot 'fe.dos.dat' using 1:2 with lines title 'up', '' using 1:3 with lines title 'down'
