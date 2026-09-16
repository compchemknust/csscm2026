set terminal png size 800,600
set output "potential_plot.png"

set xlabel "Time(ps)" 
set ylabel "Potential (kJ/mol) "
set title "Energy Minimization "
set key right


#set style fill solid 1.0 border -1
#plot 'potential.dat' using  1:2 ls 1 t "Berendsen" 
#plot "potential.dat" t "Potential energy vrs time" lt 7 lc 0 w lines
#plot "potential.dat" title "Berendsen vrs time" lt 7 lc 0 lw 4 w lp,\
     "potential_noose.dat" title "Noose-H Pot" lt 8 lc 12 lw 2 w lines

plot "potential_berend_noose.dat" using 1:2 title "Berendsen vrs time" lt 7 lc 0 w lines,\
                                ''  using 1:3 title "Noose" lt 8 lc 12 w lp


set terminal png size 800,600
set output "potential_plot1.png"

set xlabel "Time(ps)" 
set ylabel "Potential (kJ/mol) "
set title "Energy Minimization "
set key right


#set style fill solid 1.0 border -1
#plot 'potential.dat' using  1:2 ls 1 t "Berendsen" 
#plot "potential.dat" t "Potential energy vrs time" lt 7 lc 0 w lines
#plot "potential.dat" title "Berendsen vrs time" lt 7 lc 0 lw 4 w lp,\
     "potential_noose.dat" title "Noose-H Pot" lt 8 lc 12 lw 2 w lines

plot "potential_berend_noose.dat" using 1:2 title "Berendsen vrs time" lt 7 lc 0 w lines,\
                                ''  using 1:3 title "Noose" lt 8 lc 12 w lp