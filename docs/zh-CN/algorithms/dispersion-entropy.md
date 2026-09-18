# 散布熵

[English](../../algorithms/dispersion-entropy.md) | 简体中文

已实现的多尺度方法：**MDE**、**RCMDE** 和 **TSMDE**。

## 定义

散布熵将幅值映射为 `nc` 个离散类别，构造带延迟的类别模式，并衡量这些模式分布的均匀程度。与排列熵不同，幅值所在位置会影响被分配的模式。

## 核心步骤

估计信号均值 $\mu$ 和样本标准差 $\sigma$，使用正态累积分布函数映射每个样本：

```math
y_i
=
\Phi\!\left(\frac{x_i-\mu}{\sigma}\right),
\qquad 0\le y_i\le1.
```

将映射值转换为类别：

```math
z_i
=
\operatorname{round}\!\left(n_c y_i+\frac{1}{2}\right),
\qquad
z_i\in\{1,\ldots,n_c\}.
```

构造延迟散布模式：

```math
\mathbf{z}_i^{(m,\tau)}
=
(z_i,z_{i+\tau},\ldots,z_{i+(m-1)\tau}).
```

最多有 $n_c^m$ 种可能模式。根据观测到的相对频率 $p(\pi)$，计算

```math
H_{\mathrm{DE}}
=
-\sum_{\pi:p(\pi)>0}p(\pi)\ln p(\pi).
```

多尺度变体将该估计器与不同构造组合：

- **MDE** 在每个尺度使用一条标准粗粒化序列，并在不同尺度保持原始信号的映射统计量。
- **RCMDE** 先平均所有复合偏移的模式分布，再计算熵。
- **TSMDE** 分别计算每个时间移位相位的散布熵，再平均各相位结果。

## 参数含义

- `m`：每个延迟模式中的类别数；模式空间按 $n_c^m$ 增长。
- `nc`：幅值类别数。
- `tau`：模式元素之间的延迟，单位为样本点。
- `scale`：MDE 或 RCMDE 的最大尺度。
- `kmax`：TSMDE 的最大时间移位尺度。

增大 `m`、`nc` 或 `tau` 通常需要更长的信号，才能可靠估计模式分布。

## 结果

MDE 和 RCMDE 返回 `scale` 个值；TSMDE 返回 `kmax` 个值。数值越大，表示在该方法和参数设置下观测到的散布模式分布越均匀。

结果未除以 $\ln(n_c^m)$。因此，改变 `m` 或 `nc` 会同时改变模式空间和可能的数值范围。

另见[多尺度构造](multiscale-constructions.md)和[英文参考文献列表](../../references.md)。
