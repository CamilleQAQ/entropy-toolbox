# 斜率熵

[English](../../algorithms/slope-entropy.md) | 简体中文

已实现的多尺度方法：**MSlopEn** 和 **TSMSlopEn**。

## 定义

斜率熵使用五种符号表示局部变化。符号记录相邻差分是较小、中等幅度的正负变化，还是较强的正负变化，再根据这些符号组成的序列计算熵。

## 核心步骤

对相邻差分

```math
d_i=x_{i+1}-x_i,
```

按下式分配符号：

```math
s_i=
\begin{cases}
0, & -\delta\le d_i\le\delta,\\
1, & \delta<d_i\le\gamma,\\
2, & d_i>\gamma,\\
-1, & -\gamma\le d_i<-\delta,\\
-2, & d_i<-\gamma.
\end{cases}
```

建立由 $m-1$ 个连续符号组成的重叠模式。若 $p(\mathbf{s})$ 是符号模式的相对频率，则计算

```math
H_{\mathrm{SlopEn}}
=
-\sum_{\mathbf{s}:p(\mathbf{s})>0}
p(\mathbf{s})\ln p(\mathbf{s}).
```

MSlopEn 将该估计器应用于标准粗粒化信号。TSMSlopEn 对每个时间移位相位计算该估计器，并平均各相位结果。

## 参数含义

- `m`：原始样本窗口维数；每个斜率模式包含 $m-1$ 个差分。当前实现支持 $2\le m\le5$。
- `delta`：较低的幅度阈值。位于 $[-\delta,\delta]$ 内的差分分配为符号 0。
- `gamma`：较高的幅度阈值，要求 $\gamma\ge\delta$。
- `scale`：MSlopEn 的最大标准多尺度尺度。
- `kmax`：TSMSlopEn 的最大时间移位尺度。

`delta` 和 `gamma` 的单位与预处理后信号的差分相同。如果缩放信号而不同时调整这两个阈值，符号序列会发生变化。

高层接口使用拼写 `gamma`；为兼容旧用法，仍接受 `gama`。

## 结果

MSlopEn 返回 `scale` 个值，TSMSlopEn 返回 `kmax` 个值。数值越大，表示在所选阈值和维数下斜率符号模式分布越均匀。使用不同阈值得到的结果不应视为处于同一测量尺度。

另见[多尺度构造](multiscale-constructions.md)和[英文参考文献列表](../../references.md)。
