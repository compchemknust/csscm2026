# Lab — Scientific plotting with GNUPLOT

Run GNUPLOT from this directory so the `.dat` paths in `plot.gp` resolve.

```bash
gnuplot plot.gp
```

That writes `potential_plot.png` and `potential_plot1.png` here.

| File | Role |
| --- | --- |
| [`plot.gp`](plot.gp) | Script: Berendsen vs Nosé–Hoover potential vs time |
| [`potential.dat`](potential.dat) | Potential vs time |
| [`potential_noose.dat`](potential_noose.dat) | Nosé–Hoover series |
| [`potential_berend_noose.dat`](potential_berend_noose.dat) | Combined Berendsen / Nosé columns |
| [`xy.dat`](xy.dat), [`yz.dat`](yz.dat) | Small 2-column series |
| [`count_script.sh`](count_script.sh) | AWK helper over `potential.dat` |
| [`examples/`](examples/) | Reference PNGs from earlier runs |
