# 方法选择

[English](../methods.md) | 简体中文

工具箱中的熵估计方法相互关联，但不能彼此替换。选择方法时应依据其数学含义、已发表证据和在目标数据上的表现，而不是选择数值最大的那个方法。

## 方法族概览

| 方法族 | 已注册方法 | 编码内容 | 实际区别 |
|---|---|---|---|
| [排列熵](algorithms/permutation-entropy.md) | MPE, TSMPE | 样本之间的相对次序 | 关注序数模式，而不是绝对幅值。 |
| [斜率熵](algorithms/slope-entropy.md) | MSlopEn, TSMSlopEn | 相邻样本变化的量化类别 | 使用与幅值相关的 `delta` 和 `gamma` 阈值；缩放信号会改变阈值含义。 |
| [散布熵](algorithms/dispersion-entropy.md) | MDE, RCMDE, TSMDE | 映射到 `nc` 个离散类别的幅值 | 适合关注幅值分布模式时作为直接起点。 |
| [模糊散布熵](algorithms/fuzzy-dispersion-entropy.md) | MFuDE, CMFuDE, RCMFuDE, TSMFuDE | 散布模式的模糊隶属度 | 用模糊隶属度代替硬类别边界。 |
| [集成模糊散布熵](algorithms/ensemble-fuzzy-dispersion-entropy.md) | MEFuDE, CMEFuDE, RCMEFuDE, TSMEFuDE | 多种模糊映射的集成 | 组合多个映射；需要特别留意恒定或近似恒定信号。 |

## 多尺度构造

完整定义和公式见[多尺度构造](algorithms/multiscale-constructions.md)。

| 前缀或形式 | 在本工具箱中的含义 | 影响 |
|---|---|---|
| `M` | 标准多尺度构造 | 每个尺度计算一条粗粒化序列。 |
| `CM` | 复合多尺度构造 | 每个尺度计算多个偏移序列，使用更多信息，也需要更多计算。 |
| `RCM` | 精细复合多尺度构造 | 先在概率分布层面合并偏移信息，再计算熵。 |
| `TSM` | 时间移位多尺度构造 | 计算直至 `kmax` 的时间移位子序列，而不是使用普通的 `scale` 接口。 |

## 实用的起始选择

- 需要直接反映幅值模式的多尺度基线时，可从 **MDE** 开始。
- 关注相对次序而非绝对幅值时，可使用 **MPE**。
- 希望表示局部变化的符号和幅度类别时，可使用 **MSlopEn**；阈值应按预处理后信号的单位选择。
- 当研究方法明确要求复合粗粒化时，可考虑 **CM** 或 **RCM** 变体。它们不是标准多尺度方法的数值替代品。
- 当研究目标采用时间移位多尺度构造时，使用 **TSM** 方法。
- 复现或扩展本项目论文中的方法时，使用 **TSMEFuDE**。

这些内容用于帮助导航，并不表示某个方法族普遍更准确。应在与目标任务有代表性的数据上验证选择，并引用[英文参考文献列表](../references.md)中的相关定义。

## 已注册方法及参数

| 方法 | 全称 | 高层接口参数 |
|---|---|---|
| MPE | Multiscale Permutation Entropy | `m`, `tau`, `scale` |
| MSlopEn | Multiscale Slope Entropy | `m`, `delta`, `gamma`, `scale` |
| MDE | Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| MFuDE | Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, 可选 `type_` |
| CMFuDE | Composite Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, 可选 `type_` |
| RCMFuDE | Refined Composite Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale`, 可选 `type_` |
| MEFuDE | Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| CMEFuDE | Composite Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| RCMEFuDE | Refined Composite Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| RCMDE | Refined Composite Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `scale` |
| TSMPE | Time-Shift Multiscale Permutation Entropy | `m`, `tau`, `kmax` |
| TSMSlopEn | Time-Shift Multiscale Slope Entropy | `m`, `delta`, `gamma`, `kmax` |
| TSMDE | Time-Shift Multiscale Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
| TSMFuDE | Time-Shift Multiscale Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
| TSMEFuDE | Time-Shift Multiscale Ensemble Fuzzy Dispersion Entropy | `m`, `nc`, `tau`, `kmax` |
