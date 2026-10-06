#!/usr/bin/env python3
"""Small, serial QE lab runner. Run from this directory. Python standard library only."""
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(executable, name, scf=False):
    if not shutil.which(executable):
        raise RuntimeError(f'{executable} is not on PATH. Ask the instructor to configure QE.')
    output = ROOT / (name + '.out')
    with output.open('w') as stream:
        result = subprocess.run([executable, '-in', name + '.in'], cwd=ROOT,
                                stdout=stream, stderr=subprocess.STDOUT)
    text = output.read_text(errors='replace')
    if result.returncode or 'JOB DONE.' not in text or (scf and 'convergence has been achieved' not in text):
        raise RuntimeError(f'{name} did not finish successfully. Read {output.name}; no result accepted.')
    print(f'{name}: finished successfully')
    return text

def energy(text):
    matches = re.findall(r'!\s+total energy\s*=\s*([-+0-9.EeDd]+)', text)
    if not matches:
        raise RuntimeError('No final SCF energy found.')
    return float(matches[-1].replace('D', 'E').replace('d', 'e'))

def sweep(kind):
    template = (ROOT / 'si.scf.in').read_text()
    choices = {'cutoff': [12, 16, 20, 24, 32, 40, 48],
               'mesh': [2, 4, 6, 8, 10],
               'lattice': [5.20, 5.25, 5.30, 5.35, 5.40, 5.45, 5.50, 5.55, 5.60]}
    rows = []
    for value in choices[kind]:
        name = f'si_{kind}_{value}'
        text = template.replace("prefix='si'", f"prefix='{name}'")
        cutoff = value if kind == 'cutoff' else 48
        mesh = value if kind == 'mesh' else (4 if kind == 'cutoff' else 8)
        text = text.replace('ecutwfc=20, ecutrho=80', f'ecutwfc={cutoff}, ecutrho={4*cutoff}')
        text = text.replace('4 4 4 1 1 1', f'{mesh} {mesh} {mesh} 1 1 1')
        if kind == 'lattice':
            text = text.replace('A=5.43', f'A={value:.2f}')
        (ROOT / (name + '.in')).write_text(text)
        rows.append([value, energy(run('pw.x', name, scf=True))])
    reference = rows[-1][1]
    headers = [kind, 'energy_Ry_per_cell', 'difference_meV_per_atom_vs_last']
    if kind == 'lattice':
        headers = ['a_angstrom', 'energy_Ry_per_cell', 'relative_meV_per_atom']
        reference = min(row[1] for row in rows)
    with (ROOT / (kind + '.csv')).open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        for value, e in rows:
            writer.writerow([value, f'{e:.10f}', f'{abs(e-reference)*13.605693*1000/2:.6f}'])
    print(f'Wrote {kind}.csv. Inspect the trend; the final settings are not automatically converged.')

def main():
    if Path.cwd().resolve() != ROOT:
        raise RuntimeError('First cd to the directory containing lab.py.')
    (ROOT / 'tmp').mkdir(exist_ok=True)
    if len(sys.argv) != 2:
        raise RuntimeError('Usage: python3 lab.py scf|cutoff|mesh|lattice|bands|al|fe|dos|graphene|graphane')
    task = sys.argv[1]
    if task in ('cutoff', 'mesh', 'lattice'):
        sweep(task)
    elif task == 'bands':
        run('pw.x', 'si.final.scf', True)
        run('pw.x', 'si.bands')
        run('bands.x', 'si.bands.pp')
    elif task == 'dos':
        run('pw.x', 'fe.scf', True)
        run('pw.x', 'fe.nscf')
        run('dos.x', 'fe.dos')
    else:
        cases = {'scf': 'si.scf', 'al': 'al.scf', 'fe': 'fe.scf',
                 'graphene': 'graphene.scf', 'graphane': 'graphane.relax'}
        if task not in cases:
            raise RuntimeError('Unknown exercise: ' + task)
        text = run('pw.x', cases[task], True)
        if task == 'graphane' and 'End of BFGS Geometry Optimization' not in text:
            raise RuntimeError('Electronic steps finished, but geometry optimization did not converge.')
        print(f'Final energy: {energy(text):.8f} Ry per cell')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError) as exc:
        sys.exit(str(exc))
