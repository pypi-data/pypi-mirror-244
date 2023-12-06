# import pathlib

# import waveforms

# def print_tree(path, module):
#     for f in path.iterdir():
#         if f.is_dir():
#             print_tree(f, f'{module}.{f.stem}')
#         elif f.suffix == '.py':
#             if f.stem == '__init__':
#                 print(f'import {module}')
#             else:
#                 print(f'import {module}.{f.stem}')

# print_tree(pathlib.Path(waveforms.__file__).parent, 'waveforms')


def test_import():
    import waveforms.math
    import waveforms.math.bayes
    import waveforms.math.fibheap
    import waveforms.math.fit
    import waveforms.math.fit._fit
    import waveforms.math.fit.delay
    import waveforms.math.fit.geo
    import waveforms.math.fit.peak
    import waveforms.math.fit.qubit_dynamics
    import waveforms.math.fit.readout
    import waveforms.math.fit.resonator
    import waveforms.math.fit.simple
    import waveforms.math.fit.spectrum
    import waveforms.math.fit.symmetry
    import waveforms.math.func
    import waveforms.math.graph
    import waveforms.math.group
    import waveforms.math.group._SU_n_
    import waveforms.math.group.clifford
    import waveforms.math.group.clifford.funtions
    import waveforms.math.group.clifford.group
    import waveforms.math.group.permutation_group
    import waveforms.math.interval
    import waveforms.math.paulis
    import waveforms.math.prime
    import waveforms.math.signal
    import waveforms.math.signal.demodulate
    import waveforms.math.signal.distortion
    import waveforms.math.signal.func
    import waveforms.math.transmon
    import waveforms.math.group.clifford.chp
    import waveforms.math.group.clifford.chp_numpy

    import waveforms.quantum
    import waveforms.quantum.analyze
    import waveforms.quantum.analyze.coupling
    import waveforms.quantum.analyze.decoherence
    import waveforms.quantum.analyze.gate_error
    import waveforms.quantum.clifford
    import waveforms.quantum.clifford.clifford
    import waveforms.quantum.clifford.db
    import waveforms.quantum.clifford.mat
    import waveforms.quantum.clifford.seq2mat
    import waveforms.quantum.fourier_grid
    import waveforms.quantum.math
    import waveforms.quantum.rb
    import waveforms.quantum.tomo
    import waveforms.quantum.transmon
    import waveforms.quantum.xeb
    
    assert True
