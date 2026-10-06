"""Rebuild the editable Beamer source, matching teaching PDF, and starter inputs."""
from pathlib import Path
import hashlib
import json
import shutil
from html import escape

ROOT = Path(__file__).resolve().parent
TEACHING = ROOT.parent

def pw(prefix, system, species, positions, mesh, calculation='scf', extra=''):
    return f"""&CONTROL
 calculation='{calculation}', prefix='{prefix}'
 pseudo_dir='./pseudo', outdir='./tmp'
 tprnfor=.true., tstress=.true.
{extra}/
&SYSTEM
 {system}
/
&ELECTRONS
 conv_thr=1.0d-8, mixing_beta=0.4
/
""" + ("&IONS\n ion_dynamics='bfgs'\n/\n" if calculation == 'relax' else '') + f"""ATOMIC_SPECIES
{species}
ATOMIC_POSITIONS {positions}
K_POINTS {mesh}
"""

SI = pw('si', "ibrav=2, A=5.43, nat=2, ntyp=1\n ecutwfc=20, ecutrho=80\n occupations='fixed'",
        'Si 28.085 Si.pz-vbc.UPF', 'alat\nSi 0.00 0.00 0.00\nSi 0.25 0.25 0.25',
        'automatic\n4 4 4 1 1 1')
FINAL = SI.replace('ecutwfc=20, ecutrho=80', 'ecutwfc=48, ecutrho=192').replace('4 4 4 1 1 1', '8 8 8 1 1 1')
BANDS = FINAL.replace("calculation='scf'", "calculation='bands'").replace("occupations='fixed'", "occupations='fixed', nbnd=8")
BANDS = BANDS[:BANDS.index('K_POINTS')] + 'K_POINTS tpiba_b\n3\n0.5 0.5 0.5 20\n0.0 0.0 0.0 20\n0.0 0.0 1.0 1\n'
AL = pw('al', "ibrav=2, A=4.05, nat=1, ntyp=1\n ecutwfc=40, ecutrho=160, nbnd=8\n occupations='smearing', smearing='mv', degauss=0.02",
        'Al 26.9815 Al.pz-vbc.UPF', 'crystal\nAl 0.0 0.0 0.0', 'automatic\n8 8 8 1 1 1')
FE = pw('fe', "ibrav=3, A=2.87, nat=1, ntyp=1\n ecutwfc=40, ecutrho=320, nbnd=16\n nspin=2, starting_magnetization(1)=0.5\n occupations='smearing', smearing='mv', degauss=0.02",
        'Fe 55.845 Fe.pbe-nd-rrkjus.UPF', 'crystal\nFe 0.0 0.0 0.0', 'automatic\n6 6 6 1 1 1')
GRAPHENE = pw('graphene', "ibrav=4, A=2.46, C=20.0, nat=2, ntyp=1\n ecutwfc=40, ecutrho=320, nbnd=8\n occupations='smearing', smearing='mv', degauss=0.005",
              'C 12.011 C.pbe-rrkjus.UPF', 'crystal\nC 0.0 0.0 0.5\nC 0.3333333333 0.6666666667 0.5', 'automatic\n9 9 1 0 0 0')
GRAPHANE = pw('graphane', "ibrav=4, A=2.54, C=20.0, nat=4, ntyp=2\n ecutwfc=40, ecutrho=320, nbnd=8\n occupations='fixed'",
              'C 12.011 C.pbe-rrkjus.UPF\nH 1.008 H.pbe-rrkjus.UPF',
              'angstrom\nC 0.0 0.0000000000 10.20\nC 0.0 1.4664696837 9.80\nH 0.0 0.0000000000 11.30\nH 0.0 1.4664696837 8.70',
              'automatic\n6 6 1 0 0 0', 'relax',
              ' etot_conv_thr=1.0d-5, forc_conv_thr=1.0d-4, nstep=100\n')

def write_inputs():
    files = {'si.scf.in': SI, 'si.final.scf.in': FINAL, 'si.bands.in': BANDS,
             'si.bands.pp.in': "&BANDS\n prefix='si', outdir='./tmp', filband='si.bands.dat'\n lsym=.true.\n/\n",
             'al.scf.in': AL, 'fe.scf.in': FE,
             'fe.nscf.in': FE.replace("calculation='scf'", "calculation='nscf'").replace('6 6 6 1 1 1', '12 12 12 1 1 1'),
             'fe.dos.in': "&DOS\n prefix='fe', outdir='./tmp', fildos='fe.dos.dat'\n Emin=-20, Emax=30, DeltaE=0.05\n ngauss=0, degauss=0.01\n/\n",
             'graphene.scf.in': GRAPHENE, 'graphane.relax.in': GRAPHANE}
    for name, text in files.items():
        (ROOT / name).write_text(text)
    plots = {
        'cutoff.gp': "set datafile separator ','\nset xlabel 'Wavefunction cutoff (Ry)'\nset ylabel 'Difference from reference (meV/atom)'\nplot 'cutoff.csv' every ::1 using 1:3 with linespoints notitle\n",
        'mesh.gp': "set datafile separator ','\nset xlabel 'Grid divisions in each direction'\nset ylabel 'Difference from reference (meV/atom)'\nplot 'mesh.csv' every ::1 using 1:3 with linespoints notitle\n",
        'lattice.gp': "set datafile separator ','\nset xlabel 'Lattice length (angstrom)'\nset ylabel 'Energy relative to sampled minimum (meV/atom)'\nplot 'lattice.csv' every ::1 using 1:3 with linespoints notitle\n",
        'si.bands.gp': "set xlabel 'Path distance (units of 2*pi/A)'\nset ylabel 'Energy (eV, file reference)'\nset xtics ('L' 0, 'Gamma' 0.8660254, 'X' 1.8660254)\nplot 'si.bands.dat.gnu' using 1:2 with lines notitle\n",
        'fe.dos.gp': "set xlabel 'Energy (eV, file reference)'\nset ylabel 'DOS (states/eV/cell)'\nplot 'fe.dos.dat' using 1:2 with lines title 'up', '' using 1:3 with lines title 'down'\n"}
    for name, text in plots.items():
        (ROOT / name).write_text(text)
    (ROOT / 'pseudo').mkdir(exist_ok=True)
    names = ['Si.pz-vbc.UPF', 'Al.pz-vbc.UPF', 'Fe.pbe-nd-rrkjus.UPF', 'C.pbe-rrkjus.UPF', 'H.pbe-rrkjus.UPF']
    manifest = []
    for name in names:
        source = TEACHING / 'handson_pwscf' / 'pseudo' / name
        target = ROOT / 'pseudo' / name
        shutil.copy2(source, target)
        manifest.append({'filename': name, 'source': '../handson_pwscf/pseudo/' + name,
                         'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    (ROOT / 'pseudo' / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

# Each slide contains one student action followed by an observable checkpoint.
# Theory appears immediately before the action that needs it.
slides = []
def slide(part, title, text, code='', check='', question=''):
    slides.append(dict(part=part, title=title, text=text, code=code, check=check, question=question))

slide('Welcome', 'Quantum ESPRESSO: your first materials calculation',
      'A guided laboratory with silicon\nThen separate lessons on metals, magnetism and atomic relaxation.',
      check='You will leave with inputs, outputs, an energy table and a band plot.')
slide('Welcome', 'The lesson schedule',
      'Session 1, about 90 minutes: terminal basics, silicon input, first energy, cutoff tests.\nSession 2, about 90 minutes: k-point tests, lattice scan, silicon bands.\nLater sessions: aluminum, iron and graphene. Run times depend on the computer.',
      check='Pause at each checkpoint. Complete silicon before moving to a new material.')
slide('Welcome', 'What the calculation answers',
      'We give QE a repeating crystal and a recipe for its electrons.\nQE finds an electron distribution and reports the energy of that cell.\nEnergy differences help us compare structures using the same physical model.',
      question='Our first question: can we calculate and identify the energy of a two-atom silicon cell?')
slide('Setup', 'Step 1: the working folder',
      'Open a terminal at the qe-tools repository root. Type the commands below.\nEach line is a command. Do not type a leading dollar sign.',
      'cd teaching/beginner_hands_on\npwd\nls\nmkdir -p tmp',
      'You see si.scf.in, lab.py and the pseudo folder. Keep this terminal in this folder.')
slide('Setup', 'Step 2: the programs',
      'The instructor should install QE before class. The exercises use a macOS or Linux shell.\nWindows students can use the instructor-provided Linux/WSL environment.',
      'command -v pw.x\ncommand -v bands.x\ncommand -v dos.x\ncommand -v python3',
      'Each command prints a path. An empty result means the instructor must configure PATH.')
slide('Setup', 'Step 3: the supplied atom files',
      'A pseudopotential describes the core of an atom so QE can compute its valence electrons.\nThis kit copies the actual files supplied with handson_pwscf. No download or renaming is needed.',
      'ls pseudo\nhead -n 12 pseudo/Si.pz-vbc.UPF',
      'Silicon uses an old LDA, norm-conserving file. It is a classroom example; test datasets before research use.')
slide('Setup', 'Terminal commands you will use',
      'ls lists files. pwd shows your folder. cp makes a copy.\nnano opens a plain-text editor. In nano: Ctrl+O, Enter saves; Ctrl+X exits.\ngrep searches text. tail shows the end of a file.',
      'cp si.scf.in si.practice.in\nnano si.practice.in\ntail -n 10 si.practice.in',
      'The original si.scf.in stays available if your practice copy has a mistake.')
slide('Silicon', 'Step 4: the whole silicon input',
      'Open si.scf.in. It is a complete file, with no missing lines to invent.\nThe first three blocks set the task, crystal and electronic accuracy.\nThe final lists name the atoms, positions and sampling grid.',
      'cat si.scf.in',
      'Find &CONTROL, &SYSTEM, &ELECTRONS, ATOMIC_SPECIES, ATOMIC_POSITIONS and K_POINTS.')
slide('Silicon', 'The task and file locations',
      'scf means self-consistent field: QE repeats electronic steps until the density settles.\nprefix names the saved calculation. Paths are relative to the terminal working folder.',
      "&CONTROL\n calculation='scf', prefix='si'\n pseudo_dir='./pseudo', outdir='./tmp'\n tprnfor=.true., tstress=.true.\n/",
      'Every settings block ends with /. The atom files are in pseudo; saved results go in tmp.')
slide('Silicon', 'The crystal and accuracy settings',
      'ibrav=2 selects an fcc lattice. A is the cubic lattice length in angstroms.\nnat counts atoms in the simulated cell. ntyp counts species labels.\necutwfc sets the wavefunction detail. ecutrho sets density detail. Both are in Ry.',
      "&SYSTEM\n ibrav=2, A=5.43, nat=2, ntyp=1\n ecutwfc=20, ecutrho=80\n occupations='fixed'\n/",
      'This cell has two Si atoms. The cutoffs are starting settings to test, not certified accuracy.')
slide('Silicon', 'Electronic stopping accuracy',
      'QE updates the electron density repeatedly while the atoms stay fixed.\nconv_thr controls its estimated electronic energy error in Ry.\nmixing_beta controls how strongly each update changes the density.',
      '&ELECTRONS\n conv_thr=1.0d-8, mixing_beta=0.4\n/',
      'Keep this block unchanged in your first tests. 1.0d-8 means 0.00000001.')
slide('Silicon', 'The two silicon atoms',
      'The filename must exactly match a file in pseudo.\nalat uses Cartesian positions divided by A. It differs from crystal coordinates, which use lattice-vector fractions.',
      'ATOMIC_SPECIES\nSi 28.085 Si.pz-vbc.UPF\nATOMIC_POSITIONS alat\nSi 0.00 0.00 0.00\nSi 0.25 0.25 0.25',
      'The second atom is at (1.3575, 1.3575, 1.3575) angstrom. Keep the alat label.')
slide('Silicon', 'The sampling grid',
      'k-points sample how electrons behave throughout a periodic crystal.\nMore sampling usually costs more time. We will test how much is enough.',
      'K_POINTS automatic\n4 4 4 1 1 1',
      'The first three numbers give a 4 by 4 by 4 grid. The final 1s shift the grid by half a step.')
slide('Silicon', 'Step 5: your first calculation',
      'Run this from the working folder. Wait until the terminal prompt returns.\n-in chooses the input. > writes output to a file. 2>&1 also captures error messages.',
      'pw.x -in si.scf.in > si.scf.out 2>&1\ntail -n 20 si.scf.out',
      'Look for JOB DONE. If it is missing, read the error before continuing.')
slide('Silicon', 'Step 6: the result and success checks',
      'Check electronic convergence as well as normal program termination.\nThe line beginning with ! gives the final energy in Ry per simulated cell.\nCopy your own number into your calculation log.',
      "grep 'convergence has been achieved' si.scf.out\ngrep '!' si.scf.out\ngrep 'JOB DONE' si.scf.out",
      'You find all three. This is one energy for two Si atoms, not an energy per atom.')
slide('Silicon', 'A short calculation log',
      'Write one row per run: filename, lattice length, cutoffs, full grid and final energy.\nAlso record success or failure, QE version and pseudopotential filename.\nThe supplied Si file has four valence electrons per atom, so expect eight electrons in this cell.',
      "grep -E 'Program PWSCF|number of electrons|Exchange-correlation' si.scf.out",
      'You can explain which settings produced each energy. Preserve si.scf.in and si.scf.out.')
slide('Accuracy', 'Step 7: one cutoff change by hand',
      'Make a copy. In the copy, change prefix to si_24 and the cutoffs to 24 and 96.\nKeep the crystal, grid and electronic threshold unchanged.',
      "cp si.scf.in si.24.in\nnano si.24.in\npw.x -in si.24.in > si.24.out 2>&1\ngrep '!' si.24.out",
      'Check convergence and JOB DONE again. Compare the new energy with the first result.')
slide('Accuracy', 'Two kinds of convergence',
      'Electronic convergence: did the density settle within this calculation?\nNumerical convergence: does the result stay nearly the same when we improve cutoffs or sampling?\nA successful run still needs numerical accuracy tests.',
      question='Does JOB DONE tell you that a 4 by 4 by 4 grid is accurate enough? Explain why.')
slide('Accuracy', 'Step 8: the cutoff series',
      'After the hand-edited test, use this helper to repeat it at 12, 16, 20, 24, 32, 40 and 48 Ry.\nIt keeps the 4 by 4 by 4 grid and sets ecutrho to four times ecutwfc for this Si file.',
      'python3 lab.py cutoff\ncat cutoff.csv',
      'Seven rows appear. The helper rejects failed SCF runs and saves each input and output.')
slide('Accuracy', 'An accuracy decision',
      'For this exercise, use a target of 1 meV per atom. Compare with the highest tested cutoff.\nFor two atoms: difference = |E - Eref| x 13.605693 x 1000 / 2.\nFor example, 0.0001 Ry per cell is about 0.6803 meV per atom.',
      check='Identify the lowest cutoff within the target. Add a higher test to confirm the reference is stable.',
      question='This tolerance concerns energy. Would you reuse it automatically for a force or stress calculation?')
slide('Accuracy', 'Step 9: the sampling series',
      'The helper tests grids 2, 4, 6, 8 and 10 at a fixed 48/192 Ry cutoff pair.\nIt keeps the grid shifts unchanged. Energies need not approach the answer monotonically.',
      'python3 lab.py mesh\ncat mesh.csv',
      'Apply the same energy tolerance. If 10 is not a stable reference, extend the series in lab.py.')
slide('Accuracy', 'Your first convergence plot',
      'Open the CSV in a spreadsheet and make an XY scatter plot.\nUse cutoff or grid size for x, and difference in meV per atom for y.\nIf gnuplot is installed, this command makes a quick interactive plot.',
      'gnuplot -persist cutoff.gp\ngnuplot -persist mesh.gp',
      'Label both axes and their units. A smooth-looking plot alone does not establish accuracy.')
slide('Structure', 'Step 10: the preferred lattice length',
      'Now ask a materials question: which lattice length gives the lowest energy?\nThe helper tests A from 5.20 to 5.60 angstrom at fixed 48/192 Ry and an 8 by 8 by 8 grid.\nVerify these settings against your convergence tests before accepting the result.',
      'python3 lab.py lattice\ncat lattice.csv',
      'Plot lattice length against energy. The lowest point should have tested points on both sides.')
slide('Structure', 'A minimum and its limits',
      'The lowest sampled point estimates the preferred lattice length.\nAdd more lengths close to that point to refine it. If the minimum is at an endpoint, extend the range.\nSymmetry can give zero atomic forces in ideal silicon at many lattice lengths.',
      check='Report the sampled minimum and spacing. A later equation-of-state fit can refine it.',
      question='Why can zero atomic forces alone fail to identify the best silicon lattice length?')
slide('Bands', 'Step 11: the saved silicon calculation',
      'Bands use the potential saved by an SCF run. Keep the same crystal, atom file, prefix and outdir.\nsi.final.scf.in and si.bands.in are a matching pair at A=5.43.\nTo use your preferred A or accuracy settings, edit both files identically first.',
      'pw.x -in si.final.scf.in > si.final.scf.out 2>&1',
      'Check SCF success. tmp/si.save exists. Do not run unrelated jobs with the same prefix and outdir.')
slide('Bands', 'A short path through the crystal',
      'si.bands.in changes the task to bands and adds nbnd=8 to include empty states.\nIts short L, Gamma, X path is enough for a first band plot.\ntpiba_b uses Cartesian coordinates in units of 2*pi/A.',
      'K_POINTS tpiba_b\n3\n0.5 0.5 0.5 20\n0.0 0.0 0.0 20\n0.0 0.0 1.0 1',
      'The final integers set interpolation toward the next point. Keep this path separate from a DOS grid.')
slide('Bands', 'Step 12: band energies and plot data',
      'Run the band calculation, then the postprocessor. Check JOB DONE in both outputs.\nThe supplied si.bands.pp.in uses prefix si and outdir ./tmp.',
      'pw.x -in si.bands.in > si.bands.out 2>&1\nbands.x -in si.bands.pp.in > si.bands.pp.out 2>&1\nls si.bands.dat*',
      'si.bands.dat.gnu contains plot data in eV. With lsym=.true., symmetry data use the .rap suffix.')
slide('Bands', 'Step 13: the first band plot',
      'With gnuplot installed, type this command. For this path, Gamma is at x about 0.8660 and X at about 1.8660.\nThe first plot uses the file energy zero. Shift by the valence-band maximum before comparing gaps.',
      'gnuplot -persist si.bands.gp',
      'You see eight branches. This short path may miss an extremum and does not establish the full band gap.')
slide('Silicon review', 'The silicon student hand-in',
      'Submit the original input and output with the final energy identified.\nInclude cutoff and sampling tables, their plots and your accuracy decision.\nInclude the lattice scan and the first band plot with units and labels.',
      check='Explain one difference between a calculation finishing and a result being accurate enough.')
slide('Later lesson: aluminum', 'Step 14: a metal',
      'Aluminum has partially occupied electronic states. Smearing makes the occupancy change smoother.\nOpen the complete al.scf.in. Find occupations, smearing, degauss and nbnd.',
      "python3 lab.py al\ngrep 'Fermi energy' al.scf.out",
      'You find a Fermi energy. The kit uses the supplied LDA Al file and a one-atom fcc cell.')
slide('Later lesson: aluminum', 'A small metal accuracy exercise',
      'Copy al.scf.in. First test grids 8, 12 and 16 at degauss=0.02.\nAt a sufficiently dense grid, test degauss=0.02, 0.01 and 0.005 Ry.\nUse a new prefix for each independent test and record energy per atom.',
      check='Compare mesh and smearing together. mv is numerical cold smearing; its width is not a temperature.',
      question='Do the highest bands have negligible occupations? Increase nbnd and check if needed.')
slide('Later lesson: iron', 'Step 15: a magnetic metal',
      'Iron can have different spin-up and spin-down populations.\nIn fe.scf.in, nspin=2 enables this treatment. starting_magnetization supplies an initial guess.\nThis lesson uses the supplied PBE ultrasoft Fe file, with separate density-cutoff tests needed.',
      "python3 lab.py fe\ngrep 'magnetization' fe.scf.out",
      'Record the final total magnetization in Bohr magnetons per cell. The starting value does not fix it.')
slide('Later lesson: iron', 'Step 16: density of states',
      'DOS counts available electronic states near each energy.\nThe helper performs Fe SCF, a denser uniform-grid NSCF run, then dos.x.\nThe complete inputs share prefix fe and outdir ./tmp.',
      'python3 lab.py dos\nhead -n 5 fe.dos.dat',
      'Read the header: energy, spin-up DOS, spin-down DOS and integrated DOS. The energy column is in eV.')
slide('Later lesson: iron', 'A first DOS plot',
      'Plot columns 2 and 3 against column 1. Both spin channels have positive DOS.\nFor a Fermi-centred plot, subtract the Fermi energy from each x value.\nTest a denser NSCF grid and smaller broadening before interpreting fine features.',
      'gnuplot -persist fe.dos.gp',
      'The postprocessor uses Gaussian degauss=0.01 Ry. Its plotted energy spacing is 0.05 eV.')
slide('Later lesson: graphene', 'Step 17: a sheet with vacuum',
      'The simulation repeats in all directions. Empty space separates the repeated graphene sheets.\nOpen graphene.scf.in: A=2.46 sets in-plane size, C=20 sets cell height in angstrom.\nThe 9 by 9 by 1 grid samples the plane.',
      'python3 lab.py graphene',
      'The two carbon atoms have fractional z=0.5, at the middle of the cell. Test larger vacuum and denser grids.')
slide('Later lesson: relaxation', 'Step 18: atoms that move',
      'Graphane adds hydrogen above and below the carbon sheet.\nOpen graphane.relax.in: nat=4, ntyp=2, calculation=relax and an &IONS block.\nQE repeatedly solves the electrons, calculates forces and moves atoms at fixed cell size.',
      'python3 lab.py graphane\ntail -n 60 graphane.relax.out',
      'Find End of BFGS Geometry Optimization and final positions. Hitting nstep=100 does not prove success.')
slide('Later lesson: relaxation', 'The relaxation result',
      'Record final C-H distances, carbon buckling and residual forces.\nCopy final coordinates with their printed unit label into a fresh input for a verification SCF run.\nrelax holds A and C fixed. It does not optimize the in-plane lattice length.',
      check='The force threshold is 0.0001 Ry/bohr, about 0.00257 eV/angstrom. Test accuracy for forces too.')
slide('Troubleshooting', 'A failed calculation',
      'Atom file missing: check pwd, pseudo_dir and exact UPF filename.\nInput read error: check plain quotes, commas, slash endings and atom counts.\nSCF fails: check geometry and occupations before changing numerical settings.',
      'tail -n 40 si.scf.out\nls pseudo',
      'Keep the input and full error output. Ask for help with these files, not only the last screenshot.')
slide('Troubleshooting', 'Missing saved data or unfinished geometry',
      'Bands/DOS cannot read data: confirm successful SCF, matching prefix/outdir and unchanged model.\nRelaxation stops: check its optimization message and final forces, as well as each electronic step.\nA finished program can still have failed to reach the requested geometry accuracy.',
      check='Keep tmp until dependent work finishes. Use a new prefix for an unrelated experiment.')
slide('Instructor reference', 'Resources and further lessons',
      'Primary classroom reference: supplied handson_pwscf.pdf and its actual input/UPF files.\nUse the README for lesson timing, resource setup, plotting and corrections.\nOfficial manuals: quantum-espresso.org/Doc/INPUT_PW.html, INPUT_BANDS.html and INPUT_DOS.html.\nLater topics: AFM cells, projected DOS, hcp optimization, graphene supercells and oxygen defects.',
      check='This kit was prepared against the local QE 7.6 manuals. Old sample outputs are not new benchmarks.')

def tex_escape(s):
    chars = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(chars.get(c, c) for c in s)

def write_tex():
    tex = [r'\documentclass[aspectratio=169,11pt]{beamer}', r'\usepackage[T1]{fontenc}',
           r'\usepackage{listings}', r'\definecolor{navy}{RGB}{23,48,73}',
           r'\setbeamercolor{frametitle}{fg=navy}', r'\setbeamercolor{structure}{fg=navy}',
           r'\setbeamertemplate{navigation symbols}{}',
           r'\setbeamertemplate{footline}{\hspace{1em}Quantum ESPRESSO hands-on\hfill\insertframenumber/\inserttotalframenumber\hspace{1em}\vspace{1em}}',
           r'\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,columns=fullflexible,keepspaces=true}',
           r'\begin{document}']
    for s in slides:
        tex += [r'\begin{frame}[fragile]{' + tex_escape(s['title']) + '}',
                r'{\small\textbf{' + tex_escape(s['part']) + r'}}\par\medskip']
        for line in s['text'].splitlines():
            tex.append(tex_escape(line) + r'\par\smallskip')
        if s['code']:
            tex += [r'\begin{lstlisting}', s['code'], r'\end{lstlisting}']
        if s['check']:
            tex.append(r'\smallskip\textbf{Checkpoint:} ' + tex_escape(s['check']) + r'\par')
        if s['question']:
            tex.append(r'\smallskip\textbf{Discuss:} ' + tex_escape(s['question']) + r'\par')
        tex.append(r'\end{frame}')
    tex.append(r'\end{document}')
    (TEACHING / 'quantum_espresso_beginner_beamer.tex').write_text('\n'.join(tex) + '\n')

def write_pdf():
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.colors import HexColor
    pdf = TEACHING / 'quantum_espresso_beginner_beamer.pdf'
    backup = ROOT / 'reference' / 'quantum_espresso_beginner_beamer.original.pdf'
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        shutil.copy2(pdf, backup)
    c = canvas.Canvas(str(pdf), pagesize=(960, 540))
    c.setTitle('Quantum ESPRESSO: beginner hands-on tutorial')
    c.setAuthor('QE teaching materials')
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=20, leading=27, textColor=HexColor('#213c50'))
    checkpoint = ParagraphStyle('check', parent=body, fontSize=17, leading=23)
    code_style = ParagraphStyle('code', fontName='Courier', fontSize=17, leading=21, textColor=HexColor('#193549'))
    for i, s in enumerate(slides, 1):
        c.setFillColor(HexColor('#168a82')); c.setFont('Helvetica-Bold', 13)
        c.drawString(42, 507, s['part'].upper())
        title = Paragraph(escape(s['title']), ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=29, leading=34, textColor=HexColor('#173049')))
        _, ht = title.wrap(876, 100)
        title.drawOn(c, 42, 482-ht)
        y = 468-ht
        for line in s['text'].splitlines():
            p = Paragraph(escape(line), body); _, h = p.wrap(876, 400)
            p.drawOn(c, 42, y-h); y -= h+9
        if s['code']:
            y -= 6
            for line in s['code'].splitlines():
                p = Paragraph(escape(line).replace(' ', '&#160;'), code_style)
                _, h = p.wrap(860, 400); p.drawOn(c, 50, y-h); y -= h
            y -= 13
        for label, text in [('Checkpoint', s['check']), ('Discuss', s['question'])]:
            if text:
                p = Paragraph('<b>'+label+':</b> '+escape(text), checkpoint)
                _, h = p.wrap(876, 400); p.drawOn(c, 42, y-h); y -= h+8
        if y < 48:
            raise RuntimeError(f'Slide {i} overflows: {s["title"]}, y={y}')
        c.setFillColor(HexColor('#627987')); c.setFont('Helvetica', 11)
        c.drawString(42, 24, 'Quantum ESPRESSO hands-on')
        c.drawRightString(918, 24, f'{i} / {len(slides)}')
        c.showPage()
    c.save()

if __name__ == '__main__':
    write_inputs()
    write_tex()
    write_pdf()
    print(f'Built {len(slides)} slides, Beamer source and complete input files.')
