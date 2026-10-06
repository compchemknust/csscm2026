# Quantum ESPRESSO beginner laboratory

Use [the revised teaching slides](../quantum_espresso_beginner_beamer.pdf) with this folder. The slides introduce each concept immediately before students need it. Complete silicon first; aluminum, iron and graphene belong in later sessions.

## Before class: instructor setup

1. Provide a working Quantum ESPRESSO installation with `pw.x`, `bands.x` and `dos.x` on `PATH`. Install it before class rather than making compilation the students' first exercise. Use a macOS/Linux terminal, or a prepared Linux/WSL environment on Windows.
2. Provide Python 3 for the optional repetition helper. Provide gnuplot or a spreadsheet application for plotting. A text editor is sufficient for input editing; the slides explain nano.
3. Give each student a separate copy of this **entire folder**, including `pseudo/`, `lab.py` and all `.in` files. The historical archive does not need to be downloaded.
4. From the copied folder, run `command -v pw.x`, `command -v bands.x`, `command -v dos.x`, and `command -v python3`. Each should print a path. `gnuplot --version` checks the optional plotting tool.
5. Run `python3 lab.py scf` on the classroom machine. Check its output before teaching. On a cluster, adapt commands to the site's scheduler and launcher. The supplied helper launches serial jobs.

On the author's machine, QE is installed at `/Users/awineamos/software/qe-7.6/build-native/bin`. If needed, the instructor can enable it for that terminal with:

```sh
export PATH="/Users/awineamos/software/qe-7.6/build-native/bin:$PATH"
```

This path is specific to that machine. A student's computer needs its own installation path. No student should guess or copy a nonexistent path.

All commands below run **inside this folder**. From the repository root:

```sh
cd teaching/beginner_hands_on
mkdir -p tmp
```

`pseudo_dir='./pseudo'` and `outdir='./tmp'` refer to the terminal working directory. Each student needs write access and sufficient space for saved data. Keep `tmp/` until bands/DOS work finishes. Use separate folders or separate prefixes for concurrent calculations.

## Session 1: one silicon calculation, then an accuracy test

Allow about 90 minutes, adjusting to the classroom machines.

| Time | Student action | Evidence before moving on |
| --- | --- | --- |
| 0–15 min | Locate the folder and check the programs | Paths printed, inputs and UPFs visible |
| 15–30 min | Read the complete Si input with the instructor | Explain task, atom count and file locations |
| 30–45 min | Run `pw.x` and inspect its output | SCF convergence, final energy, `JOB DONE.` |
| 45–60 min | Change one cutoff pair by hand | Two successful outputs with different settings |
| 60–90 min | Run and plot the cutoff series | A table and a justified provisional cutoff |

The first run is deliberately small:

```sh
pw.x -in si.scf.in > si.scf.out 2>&1
grep 'convergence has been achieved' si.scf.out
grep '!' si.scf.out
grep 'JOB DONE' si.scf.out
```

Record the final energy from your own output. A negative energy is normal; its magnitude depends on the atom file and model. It is in Ry **per two-atom cell**. Divide by two for a value per atom. Do not compare absolute energies from different pseudopotentials or compositions as a stability test.

Make one change by hand:

```sh
cp si.scf.in si.24.in
nano si.24.in
```

In the copy, set `prefix='si_24'`, `ecutwfc=24` and `ecutrho=96`. Save, then run and check the output exactly as above with the new filenames. The density cutoff ratio of four is for this norm-conserving Si exercise. It is not a rule for every atom file.

Once students can do this manually, automate the repetition:

```sh
python3 lab.py cutoff
```

This creates seven separately named inputs/outputs and `cutoff.csv`. The final column compares each result with the 48 Ry run, in meV/atom. The teaching target is 1 meV/atom. Extend the series above 48 Ry to confirm the reference is stable. Passing one comparison does not prove convergence for forces, stress or a different material.

## Session 2: sampling, lattice length and bands

| Time | Student action | Evidence before moving on |
| --- | --- | --- |
| 0–25 min | Run `python3 lab.py mesh` | Five successful grid tests and an accuracy decision |
| 25–50 min | Run `python3 lab.py lattice` | Minimum bracketed on both sides |
| 50–75 min | Run the matching Si SCF/bands pair and postprocessor | Saved SCF data and `.gnu` plot data |
| 75–90 min | Plot and explain the results | Axes, units, method and limitations recorded |

The mesh series uses 48/192 Ry and grids 2, 4, 6, 8 and 10 with identical shifts. The lattice series uses 48/192 Ry and an 8 by 8 by 8 shifted grid. These are fixed classroom test settings. If students' accuracy tests require tighter settings, update the helper before the lattice series. Test the cutoff and grid together once more for the final result.

Plot the lattice table. Find the lowest sampled energy, add points around it, and extend the range if the lowest point lies at an endpoint. This is a sampled minimum, not an equation-of-state fit or a precise bulk modulus. Ideal diamond Si can have zero forces at multiple lattice lengths because of symmetry.

For bands, the matching SCF/bands inputs both initially use `A=5.43`, 48/192 Ry and the same model. To use the lattice length found above, change `A` in **both** inputs and rerun SCF first. The grid in the SCF file and the path in the bands file intentionally differ.

```sh
pw.x -in si.final.scf.in > si.final.scf.out 2>&1
pw.x -in si.bands.in > si.bands.out 2>&1
bands.x -in si.bands.pp.in > si.bands.pp.out 2>&1
```

Check SCF convergence and `JOB DONE.` before advancing. Check normal termination in each following output. Alternatively, `python3 lab.py bands` runs this sequence and stops on failure. It **reruns SCF** so the saved potential matches the supplied bands input.

The short path is L–Gamma–X. In `tpiba_b` coordinates these are `(0.5,0.5,0.5)`, `(0,0,0)` and `(0,0,1)`, in Cartesian units of `2*pi/A`. The x coordinate in the `.gnu` file is path distance. Vertices are at approximately 0, 0.866025 and 1.866025. The initial plot uses the file's energy zero. For a semiconductor comparison, shift by the valence-band maximum from your calculation. Do not claim a full band gap from this short path alone; it may miss extrema, and semilocal DFT has model limitations.

## Plotting without an additional Python dependency

Open `cutoff.csv`, `mesh.csv` and `lattice.csv` in a spreadsheet application. Choose an **XY scatter** plot with a numerical x axis. Use column 1 for x. For convergence, use column 3 for y; for the lattice minimum, use column 2 or the relative energy in column 3. Label units.

For gnuplot, start `gnuplot` in this folder, then type:

```gnuplot
set datafile separator ','
set xlabel 'Wavefunction cutoff (Ry)'
set ylabel 'Difference from reference (meV/atom)'
plot 'cutoff.csv' every ::1 using 1:3 with linespoints
```

For the band file, restore whitespace parsing and add vertex labels:

```gnuplot
set datafile separator whitespace
set xlabel 'Path distance (units of 2*pi/A)'
set ylabel 'Energy (eV, file reference)'
set xtics ('L' 0, 'Gamma' 0.8660254, 'X' 1.8660254)
plot 'si.bands.dat.gnu' using 1:2 with lines notitle
```

If using a spreadsheet for bands, preserve blank lines as branch boundaries. Plot each branch as a separate series to avoid artificial lines joining separate bands.

## Later lessons

Each example below is a **complete independent input**, not a fragment to splice into the silicon file.

| Lesson | Command | What students inspect | What still needs testing |
| --- | --- | --- | --- |
| Aluminum | `python3 lab.py al` | Fermi energy and partial occupations | Cutoffs, mesh, smearing and empty bands |
| Iron | `python3 lab.py fe` | Total and absolute magnetization | Both cutoffs, mesh, smearing, initial magnetic guesses |
| Iron DOS | `python3 lab.py dos` | Header and two spin channels | Dense NSCF mesh and postprocessing broadening |
| Graphene | `python3 lab.py graphene` | Two atoms centred in vacuum | Cutoffs, in-plane mesh, smearing and vacuum height |
| Graphane | `python3 lab.py graphane` | Final coordinates, buckling and forces | Force accuracy and in-plane lattice length |

Al uses the old supplied LDA norm-conserving file. Fe uses the supplied PBE ultrasoft file. C and H use supplied PBE ultrasoft files. Different lessons use different models; do not combine their energies. `pseudo/manifest.json` records source filenames and SHA-256 checksums. The files are preserved historical teaching resources, not a claim of modern dataset validation or a source of recommended research cutoffs.

For an Al test, copy `al.scf.in` into distinct cases. Change only the grid at fixed smearing first, then change the smearing width at a sufficiently dense grid. Use a new prefix for each case. With `smearing='mv'`, `degauss` is a numerical width in Ry, not a temperature. Inspect the highest band occupations and increase `nbnd` if needed.

For Fe DOS, the helper reruns Fe SCF, then NSCF on a 12 by 12 by 12 mesh, then `dos.x`. It therefore replaces saved Fe data deliberately. `fe.dos.dat` has energy in eV, up/down DOS in states/eV/cell, and integrated DOS. Plot spin-up and spin-down against energy minus the Fermi energy reported by the NSCF result. The postprocessor uses Gaussian broadening, `degauss=0.01` Ry; `DeltaE=0.05` is in eV. Finer `DeltaE` alone adds no electronic states.

For graphane, `relax` moves atoms with the cell fixed. Success requires completed electronic steps **and** an optimization convergence message, acceptable final forces, and energy change. Copy the final positions with their exact unit label into a fresh verification input. It does not optimize the in-plane lattice constant. The vacuum dimension must remain fixed in any later in-plane cell optimization.

Leave AFM comparisons, PDOS, hcp iron, supercells and epoxide defects for an advanced workshop. They require additional choices about magnetic branches, projections, cell constraints and reference energies that distract from the first executable workflow.

## Corrections and clarifications to the supplied reference

These findings distinguish statements in the old teaching resources from the instructions of this lab.

| Source | Problem | Resolution in this kit |
| --- | --- | --- |
| Reference p. 2 | Missing archive URL, inconsistent `Day1`/folder naming | Distribute this self-contained folder |
| Supplied Si/Al/Fe inputs and scripts | Placeholder pseudopotential and scratch paths | Actual copied files, `./pseudo`, `./tmp`, defined working directory |
| Reference pp. 8–11 | Old example cutoffs can look universal; k-test resets cutoff to 12 Ry | Explicit dataset and separate fixed-high-cutoff grid tests |
| Reference p. 13 | 5.47 angstrom and 10.26 bohr are inconsistent | Use explicit `A` in angstrom; 10.26 bohr is about 5.43 angstrom |
| Supplied `si.scf.in` / `si.bands.in` | `celldm(1)=10.2` versus `10.7`, plus different cutoffs | Matching SCF/bands geometry and cutoffs; fresh SCF before bands |
| Reference p. 14 | Global path continuity presented as mandatory | Short connected path for beginners; disconnected segments can be plotted separately |
| Reference p. 15 | Both symmetry statements say `lsym=.true.`; `.rep` suffix | `.true.` enables analysis, `.false.` disables it; filename is `.rap` |
| Reference p. 20 | Fe described as requiring USPP; `nspin=2` equated to LSDA despite PBE | USPP is a dataset choice; spin polarization and XC are separate settings |
| Reference p. 21 | AFM coordinate typo `(1/2,1,2,1/2)` | Correct second cubic-cell site is `(1/2,1/2,1/2)`; defer AFM lesson |
| Reference p. 24 | Tetrahedron PDOS said to be unimplemented | Current local QE 7.6 PROJWFC documentation supports it; defer PDOS |
| Reference pp. 27–31 | Small vacuum can seem sufficient; relaxation criteria implicit | Start at C=20 angstrom and test it; explicit force/energy thresholds |
| Existing beginner PDF p. 4 | Says input archive and UPFs were unavailable | The repository now contains them; this kit uses the actual resources |

The original 61-slide PDF is preserved in `reference/quantum_espresso_beginner_beamer.original.pdf`. The original `handson_pwscf/` files remain unchanged.

## Instructor discussion answers

- `JOB DONE.` confirms normal termination, not converged sampling or a finished geometry optimization.
- Electronic SCF convergence and numerical basis/sampling convergence answer different questions.
- The Si energy is per two-atom cell. A 0.0001 Ry cell difference is about 0.6803 meV/atom.
- Zero forces in symmetry-constrained diamond silicon do not establish equilibrium lattice length; examine energy versus lattice length or stress.
- The first band plot contains occupied and empty states. A path is unsuitable for a DOS integration grid.
- The final Fe moment depends on the converged state, not only its initial guess. Different initial guesses can converge to different branches.
- Graphane `relax` optimizes atom positions at a chosen cell size, not the lattice length.

## Documentation and rebuilding

### Local execution check

All supplied calculation workflows were executed successfully with the installed QE 7.6 on 6 October 2026: first Si SCF, all cutoff/grid/lattice cases, matching Si SCF and bands plus `bands.x`, Al SCF, Fe SCF/NSCF/DOS, graphene SCF and graphane relaxation. The graphane output included `End of BFGS Geometry Optimization`. These checks establish that the exercises run with this installation and the supplied UPFs; they do not establish research accuracy for the later materials.

`sample_results/` contains newly calculated example tables, clearly separate from students' own results. Additional Si tests at 64, 80 and 96 Ry confirm the cutoff reference: 48 Ry differs from 96 Ry by about 0.6863 meV/atom on the fixed 4 by 4 by 4 grid. The 80-to-96 Ry difference is about 0.0020 meV/atom. This supports 48 Ry for the stated **energy** teaching target with this specific dataset. The sampled lattice minimum is 5.40 angstrom at 0.05 angstrom spacing; this is not a fitted equilibrium value.

The gnuplot executable was unavailable on the authoring machine, so the plotting scripts were supplied but not executed locally. Students can use the spreadsheet route instead. The 40-page distribution PDF was rendered and visually checked.

The local QE 7.6 `PW/Doc/INPUT_PW.def`, `PP/Doc/INPUT_BANDS.def`, `PP/Doc/INPUT_DOS.def` and `PP/Doc/INPUT_PROJWFC.def` were checked. Online documentation may report a different version; use manuals matching the installed executable.

- [Official PW input reference](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
- [Official bands input reference](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html)
- [Official DOS input reference](https://www.quantum-espresso.org/Doc/INPUT_DOS.html)
- [Official projected DOS input reference](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html)

The editable slide source is `../quantum_espresso_beginner_beamer.tex`, which opens in Codex's LaTeX editor and compiled successfully there. `build_tutorial.py` keeps the same lesson content in both an editable Beamer source and the distribution PDF. Its PDF renderer uses ReportLab; this is not an exported copy of the editor preview. Rebuilding also resets starter inputs to their original classroom settings, so keep any student edits elsewhere first. Rebuild using Python with ReportLab installed.
