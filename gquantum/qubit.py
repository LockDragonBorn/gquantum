"""This module contains initialization and operation on qubits.

This module contains all main quantum gates and measurements on quantum
computation. Initializes the class Qubit with the number of required qubits,
and then uses the quantum gates and measurements as functions inside the
class.
"""

import numpy as np
from gquantum.backend import _apply_gate, _collapse, _measure
from collections import Counter

class Qubit:
    """Creates qubits register.

    Attributes:
        num_qubits: The number of qubits in register.
        amplitudes: The amplitudes of qubits in register.
    """

    def __init__(self, num_qubits):
        """Initializes Qubit with the number of qubits."""
        assert num_qubits < 32, 'This lib support at most 31 qubits.'
        self.num_qubits = num_qubits
        self.amplitudes = np.zeros((np.ones(num_qubits) * 2).astype(int).tolist()).astype(np.complex64)
        self.amplitudes[tuple(np.zeros(num_qubits).astype(int)[:, np.newaxis].tolist())] = 1
        self._single_qubit_gates = {
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

    def h(self, qubit_index):
        """Applies the Hadamard transformation to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["H"], qubit_index)

    def x(self, qubit_index):
        """Applies the Pauli X gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], qubit_index)

    def y(self, qubit_index):
        """Applies the Pauli Y gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["Y"], qubit_index)

    def z(self, qubit_index):
        """Applies the Pauli Z gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["Z"], qubit_index)

    def s(self, qubit_index):
        """Applies the π/4 phase gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["S"], qubit_index)

    def t(self, qubit_index):
        """Applies the π/8 phase gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["T"], qubit_index)

    def id(self, qubit_index):
        """Applies the Identity gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["Id"], qubit_index)

    def s_dagger(self, qubit_index):
        """Applies the adjoint of S gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["SDagger"], qubit_index)

    def t_dagger(self, qubit_index):
        """Applies the adjoint of T gate to a qubit.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["TDagger"], qubit_index)

    def rx(self, theta, qubit_index):
        """Applies the RX gate to a qubit.

        The RX gate manipulates a qubit as a rotation with an angle theta
        about X-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
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
        """Applies the RY gate to a qubit.

        The RY gate manipulates a qubit as a rotation with an angle theta
        about Y-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
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
        """Applies the RZ gate to a qubit.

        The RZ gate manipulates a qubit as a rotation with an angle theta
        about Z-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        a = np.exp(-1j * theta / 2)
        d = np.exp(1j * theta / 2)
        gate_matrix = np.array([
            [a, 0],
            [0, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index)

    def cx(self, control_index, target_index):
        """Applies the controlled-NOT(CX) gate to a pair of qubits.

        Args:
            control_index: Index of the control qubit, starts from 0.
            target_index: Index of the target qubit, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], target_index, [control_index])

    def cnot(self, control_index, target_index):
        """Applies the controlled-NOT(CNOT) gate to a pair of qubits.

        Args:
            control_index: Index of the control qubit, starts from 0.
            target_index: Index of the target qubit, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], target_index, [control_index])

    def toffoli(self, control_index_1, control_index_2, target_index):
        """Applies the toffoli(CCNOT) gate to three qubits.

        Args:
            control_index_1: Index of the first control qubit, starts from 0.
            control_index_2: Index of the second control qubit, starts from 0.
            target_index: Index of the target qubit, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], target_index, [control_index_1, control_index_2])

    def ccnot(self, control_index_1, control_index_2, target_index):
        """Applies the CCNOT(toffoli) gate to three qubits.

        Args:
            control_index_1: Index of the first control qubit, starts from 0.
            control_index_2: Index of the second control qubit, starts from 0.
            target_index: Index of the target qubit, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], target_index, [control_index_1, control_index_2])

    def swap(self, qubit_1_index, qubit_2_index):
        """Applies the SWAP gate to a pair of qubits.

        Args:
            qubit_1_index: Index of the first qubit to be swapped, starts from 0.
            qubit_2_index: Index of the first qubit to be swapped, starts from 0.
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], qubit_2_index, [qubit_1_index])
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], qubit_1_index, [qubit_2_index])
        _apply_gate(self.amplitudes, self._single_qubit_gates["X"], qubit_2_index, [qubit_1_index])

    def multi_controlled_gate(self, gate, qubit_index, control_index_list):
        """Applies a specific gate to a qubit with controls of other qubits.

        Args:
            gate: Specific gate to be executed. comes from
                "X, Y, Z, H, S, T, Id, SDagger, TDagger".
            qubit_index: Index of the target qubit, starts from 0.
            control_index_list: List of indices of the control qubits,
                the index in this list should starts from 0.
        """
        assert gate in self._single_qubit_gates.keys(), \
            'Gate should be one from "X, Y, Z, H, S, T, Id, SDagger, TDagger"'
        _apply_gate(self.amplitudes, self._single_qubit_gates[gate], qubit_index, control_index_list)

    def multi_controlled_rx(self, theta, qubit_index, control_index_list):
        """Applies the RX gate to a qubit with controls of other qubits.

        The RX gate manipulates a qubit as a rotation with an angle theta
        about X-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of the target qubit, starts from 0.
            control_index_list: List of indices of the control qubits,
                the index in this list should starts from 0.
        """
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
        """Applies the RY gate to a qubit with controls of other qubits.

        The RY gate manipulates a qubit as a rotation with an angle theta
        about Y-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of the target qubit, starts from 0.
            control_index_list: List of indices of the control qubits,
                the index in this list should starts from 0.
        """
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
        """Applies the RZ gate to a qubit with controls of other qubits.

        The RZ gate manipulates a qubit as a rotation with an angle theta
        about Z-axis.

        Args:
            theta: Angle about which the qubit is to be rotated.
            qubit_index: Index of the target qubit, starts from 0.
            control_index_list: List of indices of the control qubits,
                the index in this list should starts from 0.
        """
        a = np.exp(-1j * theta / 2)
        d = np.exp(1j * theta / 2)
        gate_matrix = np.array([
            [a, 0],
            [0, d]
        ])
        _apply_gate(self.amplitudes, gate_matrix, qubit_index, control_index_list)

    def reset(self, qubit_index):
        """Reset a qubit to |0>.

        When the qubit is entangled with other qubits, those qubits would also
        collapse with the role of quantum measurement.

        Args:
            qubit_index: Index of qubit to which the gate should be applied, starts from 0.
        """
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        if measure_result[0] == "1":
            _apply_gate(self.amplitudes, self._single_qubit_gates["X"], qubit_index)

    def reset_all(self):
        """Reset all qubits to |0>."""
        self.amplitudes = np.zeros((np.ones(self.num_qubits) * 2).astype(int).tolist()).astype(np.complex64)
        self.amplitudes[tuple(np.zeros(self.num_qubits).astype(int)[:, np.newaxis].tolist())] = 1

    def measure(self, qubit_index):
        """Performs a measurement of a single qubit in computational(Pauli Z) basis.

        Args:
            qubit_index: Index of qubit to be measured, starts from 0.

        Returns:
            "0" or "1" as type string. Represent the state |0> and |1> .
        """
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        return measure_result[0]

    def measure_x(self, qubit_index):
        """Performs a measurement of a single qubit in Pauli X basis.

        Args:
            qubit_index: Index of qubit to be measured, starts from 0.

        Returns:
            "0" or "1" as type string. Represent the state |0> and |1> .
        """
        _apply_gate(self.amplitudes, self._single_qubit_gates["H"], qubit_index)
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        _apply_gate(self.amplitudes, self._single_qubit_gates["H"], qubit_index)
        return measure_result[0]

    def measure_y(self, qubit_index):
        """Performs a measurement of a single qubit in Pauli Y basis.

        Args:
            qubit_index: Index of qubit to be measured, starts from 0.

        Returns:
            "0" or "1" as type string. Represent the state |0> and |1> .
        """
        _apply_gate(self.amplitudes, np.matmul(self._single_qubit_gates["H"], self._single_qubit_gates["SDagger"]),
                    qubit_index)
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        _apply_gate(self.amplitudes, np.matmul(self._single_qubit_gates["S"], self._single_qubit_gates["H"]),
                    qubit_index)
        return measure_result[0]

    def measure_z(self, qubit_index):
        """Performs a measurement of a single qubit in Pauli Z(computational) basis.

        Args:
            qubit_index: Index of qubit to be measured, starts from 0.

        Returns:
            "0" or "1" as type string. Represent the state |0> and |1> .
        """
        measure_result = _measure(self.amplitudes, [qubit_index])
        _collapse(self.amplitudes, [qubit_index], measure_result)
        return measure_result[0]

    def multi_qubit_measure(self, qubit_index_list):
        """Performs measurements of qubits in computational(Pauli Z) basis.

        Args:
            qubit_index_list: List of indices of qubits to be measured,
                the index in this list should starts from 0.

        Returns:
            A list with elements "0" or "1" as type string, which represent the
            state |0> and |1> for qubits with the descending order.

            example:

            ['1', '0', '0']

            The '1' represents the state |1> for the qubit with the biggest index.
        """
        measure_result = _measure(self.amplitudes, qubit_index_list)
        _collapse(self.amplitudes, qubit_index_list, measure_result)
        return measure_result

    def simulator_func_multi_measure_without_collapse(self, qubit_index_list, measure_times):
        """Performs measurements several times without collapse.

        This function is not directly performable on a real quantum computer.

        Args:
            qubit_index_list: List of indices of qubits to be measured,
                the index in this list should starts from 0.
            measure_times: Number of times to perform measurements.

        Returns:
            A dict with keys as measured states and values as numbers of
            times measured in that states. The qubits represented are
            in descending order.

            example:

            {'00': 490, '11': 510}
        """
        measure_result_list = []
        for i in range(measure_times):
            measure_result = _measure(self.amplitudes, qubit_index_list)
            measure_result_list.append("".join(measure_result))
        count_result = Counter(measure_result_list)
        return dict(count_result)

    def simulator_func_get_amplitudes(self):
        """Returns the amplitudes of this quantum register.

        This function is not directly performable on a real quantum computer.
        """
        return self.amplitudes

    def simulator_func_save_amplitudes(self, file="amplitudes.npy"):
        """Save the amplitudes of this quantum register to a file.

        This function is not directly performable on a real quantum computer.

        Args:
            file: Path to the file to save amplitudes.
        """
        np.save(file, self.amplitudes)

    def simulator_func_load_amplitudes(self, file="amplitudes.npy"):
        """Load the amplitudes of this quantum register to a file.

        This function is not directly performable on a real quantum computer.

        Args:
            file: Path to the file to load amplitudes.
        """
        self.amplitudes = np.load(file)
        self.num_qubits = len(self.amplitudes.shape)
