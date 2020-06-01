# gquantum

[![PyPi
Version](https://img.shields.io/pypi/v/gquantum.svg?style=for-the-badge)](https://pypi.python.org/pypi/gquantum)
[![License](https://img.shields.io/pypi/l/gquantum.svg?style=for-the-badge)](https://pypi.python.org/pypi/gquantum/)
[![GitHub
stars](https://img.shields.io/github/stars/yangzheliu/gquantum.svg?style=for-the-badge&label=Stars)](https://github.com/YangzheLiu/gquantum)

GQuantum(Grace Quantum Computer Simulator) is an open-source quantum computer simulator with least dependent APIs. It simulates arbitrary quantum circuits with at most 31 qubits.

## Installing

This library is distributed on
[PyPI](https://pypi.python.org/pypi/gquantum) and can be installed using
pip:

```bash
$ pip install gquantum
```

## Getting Started

The basic element in quantum computing is **qubit**. You can initialize several qubits with the class ``Qubit()`` in GQuantum:

```python
import gquantum as gq

qu = gq.Qubit(2)
```
    
Similar to logic gates in traditional computer, **quantum gates** are used to manipulate the state of qubit:

```python
qu.h(0)
qu.cnot(0, 1)
```
The **H** gate changed the first qubit from state |0> to superposition between |0> and |1>. The **CNOT** gate entangled the first qubit with the second qubit.


The function ``measure()`` is used to observe the state of qubit:

```python
print(qu.measure(0))
print(qu.measure(1))
```

Because these two qubits above are entangled, the outputs of measurements should be both |0> or |1>.

## Runtime Analysis

We ran 50 random quantum gates with Intel(R) Xeon(R) Gold 5118 CPU. And we got average time per gate:
| Qubits Number   | Average Time(s) | RAM Required(GB) |
| ---             | ---    | --- |
| 31             | 35.3 | 40.9 |
| 30             | 16.2 | 20.2 |
| 29             | 8.7 | 10.2 |

Notice that the number of quantum gates executed in a practical quantum computer typically does not surpass 100 times the number of qubits in the sysytem. Otherwise the noise gonna ruin the system. Thus to practically simulate a 31 qubits quantum system, less than 3100 quantum gates should be executed. These quantum gates will spend less than 30 hours, which is acceptable by most research situation.

