# gquantum

[![PyPi
Version](https://img.shields.io/pypi/v/gquantum.svg?style=for-the-badge)](https://pypi.python.org/pypi/gquantum)
[![License](https://img.shields.io/pypi/l/gquantum.svg?style=for-the-badge)](https://pypi.python.org/pypi/gquantum/)
[![GitHub
stars](https://img.shields.io/github/stars/yangzheliu/gquantum.svg?style=for-the-badge&label=Stars)](https://github.com/YangzheLiu/gquantum)

GQuantum(Grace Quantum Computer Simulator) is an open-source quantum computer simulator with least dependent APIs. It simulates arbitrary quantum circuits with at most 31 qubits. (本项目所有说明包含中文版 ，请往下翻。)

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



# 中文说明

GQuantum(Grace Quantum Computer Simulator)是轻量级开源量子计算机模拟器。它能模拟最多31个量子位的所有量子线路。

## 安装

GQuantum的安装基于
[PyPI](https://pypi.python.org/pypi/gquantum) 请运行pip命令:

```bash
$ pip install gquantum
```

## 入门教程

量子计算的最基本元素是**量子位**。你可以使用GQuantum中的``Qubit()``类初始化多个量子位:

```python
import gquantum as gq

qu = gq.Qubit(2)
```
    
同传统计算机中逻辑门作用于比特类似，**量子门**用来操纵量子位:

```python
qu.h(0)
qu.cnot(0, 1)
```
**H** 门将第一个量子位从 |0> 状态变换到 |0> 与 |1> 之间的叠加态。 **CNOT** 建立了第一个量子位与第二个量子位的量子纠缠。


``measure()`` 函数用于测量单个量子位的观测值:

```python
print(qu.measure(0))
print(qu.measure(1))
```

由于这两个量子位处于纠缠状态，当测量第一个量子位时第二个量子位跟着坍缩。所以两个量子位测量结果将同时是 |0> 或者 |1>.

## 性能测试

我们在 Intel(R) Xeon(R) Gold 5118 CPU 跑了50组随机量门。然后取平均得到单个量子门的运行时间:
| 量子位个数   | 单个量子门运行时间(s) | 最低需占用内存(GB) |
| ---             | ---    | --- |
| 31             | 35.3 | 40.9 |
| 30             | 16.2 | 20.2 |
| 29             | 8.7 | 10.2 |

注意在真实的量子计算机中，连续作用量子门的个数一般不会超过量子位的一百倍。否则产生的物理干扰将严重影响系统。所以在真正的31位量子计算程序中，量子门一般少于3100个。GQuantum将在30小时内运行完所有的量子门，所以GQuantum能在可接受的范围内模拟几乎所有31位量子计算程序。

