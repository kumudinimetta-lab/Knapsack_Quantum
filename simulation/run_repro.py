"""Reproduce the revised paper without overwriting historical raw experiments."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true',
                        help='Exact reference, mathematical checks and witness tests only')
    args = parser.parse_args()
    steps = [['revision_adversarial_20261022.py'],
             ['revision_audit_20261022.py', '--part', 'reference'],
             ['revision_audit_20261022.py', '--part', 'recovery']]
    if not args.quick:
        steps += [['revision_audit_20261022.py', '--part', 'oracle'],
                  ['revision_audit_20261022.py', '--part', 'small'],
                  ['revision_coherent_h_20261023.py'],
                  ['revision_spectral_20261022.py'],
                  ['revision_large_coefficients_20261022.py'],
                  ['revision_regression_20261022.py'],
                  ['revision_predicate_20261022.py']]
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
    for step in steps:
        subprocess.run([sys.executable, str(ROOT/'simulation'/step[0]), *step[1:]],
                       cwd=ROOT, env=env, check=True)
    print('Finished. See REPRODUCIBILITY_REVISION.md for scopes and mismatch counts.')


if __name__ == '__main__':
    main()
