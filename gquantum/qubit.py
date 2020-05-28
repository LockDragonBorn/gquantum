import numpy as np
from gquantum.backend import _apply_gate, _collapse, _measure
from collections import Counter

class Qubit:
    single_qubit_gates = {
        # Pauli-X / Not Gate
        'X': np.matrix([
            [0, 1],
            [1, 0]
        ]),
        # Pauli-Y Gate
        'Y': np.matrix([
            [0, -1j],
            [1j, 0]
        ]),
        # Pauli-Z Gate
        'Z': np.matrix([
            [1, 0],
            [0, -1]
        ]),
        # Hadamard Gate
        'H': np.multiply(1. / np.sqrt(2), np.matrix([
            [1, 1],
            [1, -1]
        ])),
        # Identity Gate
        'Id': np.eye(2),
        # S & S Dagger Gate
        'S': np.matrix([
            [1, 0],
            [0, 1j]
        ]),
        'SDagger': np.matrix([
            [1, 0],
            [0, 1j]
        ]).conjugate().transpose(),
        # T & T Dagger / Pi over 8 Gate
        'T': np.matrix([
            [1, 0],
            [0, np.e ** (1j * np.pi / 4.)]
        ]),
        'TDagger': np.matrix([
            [1, 0],
            [0, np.e ** (1j * np.pi / 4.)]
        ]).conjugate().transpose()
    }

    def __init__(self, num_qubits):
        assert num_qubits < 32, 'This lib support at most 31 qubits.'
        self.num_qubits = num_qubits
        self.amplitudes = np.zeros((np.ones(num_qubits) * 2).astype(int).tolist()).astype(np.complex64)
        self.amplitudes[tuple(np.zeros(num_qubits).astype(int)[:, np.newaxis].tolist())] = 1

    def h(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["H"], qubit_index)

    def x(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], qubit_index)

    def y(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["Y"], qubit_index)

    def z(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["Z"], qubit_index)

    def s(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["S"], qubit_index)

    def t(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["T"], qubit_index)

    def id(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["Id"], qubit_index)

    def s_dagger(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["SDagger"], qubit_index)

    def t_dagger(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["TDagger"], qubit_index)

    def rx(self, theta, qubit_index):
        a = np.cos(theta / 2)
        b = -1j * np.sin(theta / 2)
        c = -1j * np.sin(theta / 2)
        d = np.cos(theta / 2)
        gate_matrix = np.array([
            [a, b],
            [c, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index)

    def ry(self, theta, qubit_index):
        a = np.cos(theta / 2)
        b = -np.sin(theta / 2)
        c = np.sin(theta / 2)
        d = np.cos(theta / 2)
        gate_matrix = np.array([
            [a, b],
            [c, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index)

    def rz(self, theta, qubit_index):
        a = np.exp(-1j * theta / 2)
        d = np.exp(1j * theta / 2)
        gate_matrix = np.array([
            [a, 0],
            [0, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index)

    def cx(self, control_index, target_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index])

    def cnot(self, control_index, target_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index])

    def toffoli(self, control_index_1, control_index_2, target_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index_1, control_index_2])

    def ccnot(self, control_index_1, control_index_2, target_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index_1, control_index_2])

    def swap(self, control_index, target_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index])
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], control_index, [target_index])
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], target_index, [control_index])

    def multi_controlled_gate(self, gate, qubit_index, control_index_list):
        assert gate in Qubit.single_qubit_gates.keys(), \
            'Gate should be one from "X, Y, Z, H, S, T, Id, SDagger, TDagger"'
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates[gate], qubit_index, control_index_list)

    def multi_controlled_rx(self, theta, qubit_index, control_index_list):
        a = np.cos(theta / 2)
        b = -1j * np.sin(theta / 2)
        c = -1j * np.sin(theta / 2)
        d = np.cos(theta / 2)
        gate_matrix = np.array([
            [a, b],
            [c, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index, control_index_list)

    def multi_controlled_ry(self, theta, qubit_index, control_index_list):
        a = np.cos(theta / 2)
        b = -np.sin(theta / 2)
        c = np.sin(theta / 2)
        d = np.cos(theta / 2)
        gate_matrix = np.array([
            [a, b],
            [c, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index, control_index_list)

    def multi_controlled_rz(self, theta, qubit_index, control_index_list):
        a = np.exp(-1j * theta / 2)
        d = np.exp(1j * theta / 2)
        gate_matrix = np.array([
            [a, 0],
            [0, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index, control_index_list)

    def reset(self, qubit_index):
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        if measure_result[0] == "1":
            _apply_gate(self.amplitudes, Qubit.single_qubit_gates["X"], qubit_index)

    def reset_all(self):
        self.amplitudes = np.zeros((np.ones(self.num_qubits) * 2).astype(int).tolist()).astype(np.complex64)
        self.amplitudes[tuple(np.zeros(self.num_qubits).astype(int)[:, np.newaxis].tolist())] = 1

    def measure(self, qubit_index):
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        return measure_result[0]

    def measure_x(self, qubit_index):
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["H"], qubit_index)
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        _apply_gate(self.amplitudes, Qubit.single_qubit_gates["H"], qubit_index)
        return measure_result[0]

    def measure_y(self, qubit_index):
        _apply_gate(self.amplitudes, np.matmul(Qubit.single_qubit_gates["H"], Qubit.single_qubit_gates["SDagger"]),
                    qubit_index)
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        _apply_gate(self.amplitudes, np.matmul(Qubit.single_qubit_gates["S"], Qubit.single_qubit_gates["H"]),
                    qubit_index)
        return measure_result[0]

    def measure_z(self, qubit_index):
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        return measure_result[0]

    def multi_qubit_measure(self, qubit_index_list):
        measure_result = _measure(self.amplitudes, qubit_index_list)
        _collapse(self.amplitudes, qubit_index_list, measure_result)
        return measure_result

    def simulator_func_multi_measure_without_collapse(self, qubit_index_list, measure_times):
        measure_result_list = []
        for i in range(measure_times):
            measure_result = _measure(self.amplitudes, qubit_index_list)
            measure_result_list.append("".join(measure_result))
        count_result = Counter(measure_result_list)
        return count_result

    def simulator_func_get_amplitudes(self):
        return self.amplitudes

    def simulator_func_save_amplitudes(self, file="amplitudes.npy"):
        np.save(file, self.amplitudes)

    def simulator_func_load_amplitudes(self, file="amplitudes.npy"):
        self.amplitudes = np.load(file)
        self.num_qubits = len(self.amplitudes.shape)
