"""This module contains internal operations on amplitudes of qubits."""

import numpy as np


def _apply_gate(amplitudes, gate, target, control_list=[]):
    assert not target in control_list, 'Target qubit should not in control qubits list!'
    qubit_num = len(amplitudes.shape)
    amplitudes_0 = "]"
    amplitudes_1 = "]"
    for i in range(qubit_num):
        if i == (target):
            amplitudes_0 = "0," + amplitudes_0
            amplitudes_1 = "1," + amplitudes_1
        elif (i) in control_list:
            amplitudes_0 = "1," + amplitudes_0
            amplitudes_1 = "1," + amplitudes_1
        else:
            amplitudes_0 = ":," + amplitudes_0
            amplitudes_1 = ":," + amplitudes_1
    amplitudes_0 = "amplitudes[" + amplitudes_0
    amplitudes_1 = "amplitudes[" + amplitudes_1
    temp_amp_1 = eval(amplitudes_1 + "*" + str(gate[1, 0]))
    temp_amp_2 = eval(amplitudes_0 + "*" + str(gate[0, 1]))
    exec(amplitudes_0 + " = " + amplitudes_0 + "*" + str(gate[0, 0]) + " + temp_amp_1")
    exec(amplitudes_1 + " = " + amplitudes_1 + "*" + str(gate[1, 1]) + " + temp_amp_2")


def _measure(amplitudes, measure_list = [0]):
    qubit_num = len(amplitudes.shape)
    measure_list = qubit_num - np.array(measure_list) - 1
    probablity_array = np.square(abs(amplitudes))
    #to prevent measure list from too long
    if len(measure_list)<21:
        irrelevant_axes = np.array(list(set(range(qubit_num)) - set(measure_list)))
        #to prevent irrelevant axes from too long
        if(len(irrelevant_axes)>12):
            probablity_array = probablity_array.sum(axis = tuple(irrelevant_axes[:12]))
            target_probablity_array = probablity_array.sum(axis = tuple(irrelevant_axes[12:]-12))
        else:
            target_probablity_array = probablity_array.sum(axis = tuple(irrelevant_axes))
        target_probablity_array = target_probablity_array.reshape(-1)
        output_integer = np.random.choice(range(target_probablity_array.shape[0]), p = target_probablity_array.ravel())
        output_binary = list(np.binary_repr(output_integer, width = len(measure_list)))
    else:
        irrelevant_axes1 = np.array(list(set(range(qubit_num)) - set(measure_list[:14])))
        irrelevant_axes2 = np.array(list(set(range(qubit_num)) - set(measure_list[14:])))
        target_probablity_array1 = probablity_array.sum(axis = tuple(irrelevant_axes1))
        target_probablity_array2 = probablity_array.sum(axis = tuple(irrelevant_axes2))
        target_probablity_array1 = target_probablity_array1.reshape(-1)
        target_probablity_array2 = target_probablity_array2.reshape(-1)
        output_integer1 = np.random.choice(range(target_probablity_array1.shape[0]), p = target_probablity_array1.ravel())
        output_integer2 = np.random.choice(range(target_probablity_array2.shape[0]), p = target_probablity_array2.ravel())
        output_binary1 = list(np.binary_repr(output_integer1, width = 14))
        output_binary2 = list(np.binary_repr(output_integer2, width = len(measure_list)-14))
        output_binary = output_binary2 + output_binary1
    return output_binary


def _collapse(amplitudes, measure_list, measure_result_list):
    measure_list.sort()
    measure_list.reverse()
    qubit_num = len(amplitudes.shape)
    new_amplitudes = np.zeros_like(amplitudes)
    amplitudes_parameter = "]"
    for i in range(qubit_num):
        if i in measure_list:
            if measure_result_list[measure_list.index(i)] == "0":
                amplitudes_parameter = "0," + amplitudes_parameter
            else:
                amplitudes_parameter = "1," + amplitudes_parameter
        else:
            amplitudes_parameter = ":," + amplitudes_parameter
    amplitudes_parameter = "[" + amplitudes_parameter
    exec("new_amplitudes"+amplitudes_parameter+" = "+ "amplitudes" + amplitudes_parameter)
    amplitudes[...] = new_amplitudes/np.linalg.norm(new_amplitudes)
