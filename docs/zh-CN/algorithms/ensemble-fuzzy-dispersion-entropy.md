# 集成模糊散布熵

[English](../../algorithms/ensemble-fuzzy-dispersion-entropy.md) | 简体中文

已实现的多尺度方法：**MEFuDE**、**CMEFuDE**、**RCMEFuDE** 和 **TSMEFuDE**。

## 定义

集成模糊散布熵在多种幅值映射下分别计算模糊模式分布，再将它们组合成一个分布。集成的目的是避免结果只依赖一种从幅值到模糊类别的映射。

## 核心步骤

为一条输入序列构造四种映射：

1. **LM**：线性最小值—最大值映射。
2. **NCDF**：正态累积分布函数映射后再进行最小值—最大值映射。
3. **TANSIG**：标准化样本通过双曲正切 sigmoid，再进行最小值—最大值映射。
4. **LOGSIG**：标准化样本通过 logistic sigmoid，再进行最小值—最大值映射。

对每种映射 $q$，计算[模糊散布熵](fuzzy-dispersion-entropy.md)中介绍的模糊散布模式分布 $\mathbf{p}^{(q)}$。逐元素组合四个分布：

$$
\bar{\mathbf{p}}
=
\frac{1}{4}
\sum_{q=1}^{4}\mathbf{p}^{(q)}.
$$

计算

$$
H_{\mathrm{EFuDE}}
=
-\sum_{\pi:\bar p(\pi)>0}
\bar p(\pi)\ln\bar p(\pi).
$$

多尺度变体采用不同构造：

- **MEFuDE**：在每个尺度的一条标准粗粒化序列上计算集成熵。
- **CMEFuDE**：为每个复合偏移计算集成熵，再平均熵值。
- **RCMEFuDE**：先平均各复合偏移的集成模式分布，再计算熵。
- **TSMEFuDE**：为每个时间移位相位计算集成熵，再平均各相位结果。

## 参数含义

- `m`：每个模式中的模糊类别数。
- `nc`：模糊幅值类别数；共有 $n_c^m$ 种可能的类别模式。
- `tau`：模式元素之间的延迟，单位为样本点。
- `scale`：MEFuDE、CMEFuDE 和 RCMEFuDE 的最大尺度。
- `kmax`：TSMEFuDE 的最大时间移位尺度。

sigmoid 映射会使用信号标准差对输入进行标准化，因此恒定或近似恒定序列可能不适合该方法族。提取特征前，应检测并处理无效或恒定通道。

## 结果

MEFuDE、CMEFuDE 和 RCMEFuDE 返回 `scale` 个值；TSMEFuDE 返回 `kmax` 个值。每个元素概括相应多尺度构造下的集成模糊模式分布。

结果使用自然对数，且未按 $\ln(n_c^m)$ 归一化。比较信号时，应保持方法、参数、片段长度和预处理一致。

另见[多尺度构造](multiscale-constructions.md)和[英文参考文献列表](../../references.md)。
