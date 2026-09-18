# 算法手册

[English](../../algorithms/index.md) | 简体中文

本手册介绍 `msentropy.compute` 提供的 15 种方法。每个页面采用相同结构：定义、核心步骤、参数含义和结果。

## 建议阅读顺序

1. [多尺度构造](multiscale-constructions.md)介绍标准、复合、精细复合和时间移位构造。
2. 选择单尺度熵方法族：
   - [排列熵](permutation-entropy.md)
   - [斜率熵](slope-entropy.md)
   - [散布熵](dispersion-entropy.md)
   - [模糊散布熵](fuzzy-dispersion-entropy.md)
   - [集成模糊散布熵](ensemble-fuzzy-dispersion-entropy.md)

## 方法对应关系

| 高层方法 | 熵方法族 | 多尺度构造 |
|---|---|---|
| MPE | 排列熵 | 标准 |
| MSlopEn | 斜率熵 | 标准 |
| MDE | 散布熵 | 标准 |
| MFuDE | 模糊散布熵 | 标准 |
| CMFuDE | 模糊散布熵 | 复合 |
| RCMFuDE | 模糊散布熵 | 精细复合 |
| MEFuDE | 集成模糊散布熵 | 标准 |
| CMEFuDE | 集成模糊散布熵 | 复合 |
| RCMEFuDE | 集成模糊散布熵 | 精细复合 |
| RCMDE | 散布熵 | 精细复合 |
| TSMPE | 排列熵 | 时间移位 |
| TSMSlopEn | 斜率熵 | 时间移位 |
| TSMDE | 散布熵 | 时间移位 |
| TSMFuDE | 模糊散布熵 | 时间移位 |
| TSMEFuDE | 集成模糊散布熵 | 时间移位 |

所有已注册方法都使用自然对数，并且不会除以理论最大值。因此，不能默认不同方法族或不同参数设置下的原始结果处于同一数值尺度。

各方法对应的论文见[英文参考文献列表](../../references.md)。
