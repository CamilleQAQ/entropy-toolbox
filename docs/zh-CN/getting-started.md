# 入门指南

[English](../getting-started.md) | 简体中文

本指南使用高层接口 `msentropy.compute`。对于日常分析，建议从这里开始：它接收一维信号，会检查常见输入错误，并始终返回一维 NumPy 数组。

## 1. 安装软件包

在仓库的本地副本中运行：

```bash
python -m pip install .
```

如果要开发工具箱或运行测试，请改用 `python -m pip install -e ".[dev]"`。

## 2. 准备一段信号

```python
import numpy as np

x = np.random.default_rng(0).standard_normal(2048)
```

`x` 可以是 Python 序列或 NumPy 数组。程序接受一维数组、单行数组和单列数组，但不接受包含多个通道的矩阵；多通道数据应先明确选择通道，或逐通道循环计算。

计算熵之前，需要自行确定如何处理缺失样本、去趋势、滤波、重采样和归一化。工具箱不会自动替你做这些实验选择。

## 3. 计算熵曲线

MDE 是一个简洁的入门示例：

```python
import msentropy

curve = msentropy.compute(
    "MDE",
    x,
    m=3,
    nc=6,
    tau=1,
    scale=20,
)
```

`curve` 包含 20 个元素。`curve[0]` 对应尺度 1，`curve[1]` 对应尺度 2，`curve[-1]` 对应尺度 20。科学表述中的尺度从 1 开始，而 Python 数组下标从 0 开始。

这些数值只是起始示例，并非自动得到的最佳参数。为实验选择设置前，请先阅读[参数与数据准备](parameters.md)。

## 4. 绘制结果

```python
import matplotlib.pyplot as plt

scales = np.arange(1, curve.size + 1)
plt.plot(scales, curve, marker="o")
plt.xlabel("Scale")
plt.ylabel("MDE")
plt.show()
```

Matplotlib 不是工具箱的运行时依赖；需要绘图时请单独安装。

## 5. 选择其他方法

工具箱注册了 20 种多尺度方法：

```python
print(msentropy.list_methods())
```

查看某个方法接受的参数：

```python
print(msentropy.get_method("TSMEFuDE").signature)
```

更换方法前，建议先通过[方法选择表](methods.md)了解各方法族。如果实验需要比较多种方法，应保持信号片段和预处理一致，并报告每种方法的全部参数。

数学定义和计算步骤见[算法手册](algorithms/index.md)。

## 高层接口与兼容接口

日常分析使用 `msentropy.compute(...)`。它提供一致的关键字参数、输入归一化和易读的校验错误。

只有在需要直接访问实现或复现特定边界行为时，才使用 `msentropy.core.*`。兼容函数可能接受高层接口会拒绝的退化输入。

## 后续示例

- [`examples/quickstart.py`](../../examples/quickstart.py) 是上述 MDE 案例的可运行版本。
- [`examples/all_methods.py`](../../examples/all_methods.py) 使用同一段可复现信号演示全部 20 种方法。
- [参数与数据准备](parameters.md)说明信号长度、预处理、非有限值和有效比较方式。
