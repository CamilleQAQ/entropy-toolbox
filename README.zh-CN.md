# Python 熵工具箱

[English](README.md) | 简体中文

`msentropy` 是一个基于 NumPy 和 SciPy 的一维时间序列熵分析工具箱。
它通过统一的高层接口提供 20 种多尺度方法，同时保留可用于
数值复现和深入研究的底层实现。

## 安装

需要 Python 3.10 或更高版本。在首次发布到 PyPI 之前，请从本地仓库安装：

```bash
git clone https://github.com/CamilleQAQ/entropy-toolbox.git
cd entropy-toolbox
python -m pip install .
```

如果需要开发或运行测试，请使用可编辑安装：

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## 第一次计算

下面的示例会计算尺度 1 到尺度 20 的 MDE，每个尺度返回一个熵值：

```python
import numpy as np
import msentropy

# 实际使用时，将它替换成自己的一维信号。
x = np.random.default_rng(0).standard_normal(2048)

curve = msentropy.compute(
    "MDE",
    x,
    m=3,       # 嵌入维数
    nc=6,      # 离散类别数
    tau=1,     # 延迟，单位为采样点
    scale=20,  # 计算尺度 1、2、...、20
)

print(curve)
print(curve[0])   # 尺度 1
print(curve[-1])  # 尺度 20
```

`m=3`、`nc=6` 和 `tau=1` 是 MDE 示例的实用起点，不是适用于所有
研究的固定参数。参数应根据信号长度、采样过程、所选方法和研究问题决定。

建议先阅读[入门指南](docs/zh-CN/getting-started.md)，再查看
[方法选择](docs/zh-CN/methods.md)、[参数与数据准备](docs/zh-CN/parameters.md)
以及[算法手册](docs/zh-CN/algorithms/index.md)。

可以直接运行 [`examples/quickstart.py`](examples/quickstart.py) 查看基础示例；
[`examples/all_methods.py`](examples/all_methods.py) 会运行全部 20 种方法。

## 接口选择

- `msentropy.compute(...)` 是日常分析使用的高层 API。它会统一向量方向、
  检查常见输入错误，并使用一致的关键字参数。
- `msentropy.core.*` 是底层兼容 API。它直接暴露数值实现，适合研究算法
  细节或复现特定数值行为。

新编写的分析代码建议优先使用 `msentropy.compute`。

方法名不区分大小写。可以在不执行计算的情况下查看全部方法及其签名：

```python
for name in msentropy.list_methods():
    print(msentropy.get_method(name).signature)
```

## 支持的方法

- 排列熵：MPE、TSMPE
- 斜率熵：MSlopEn、TSMSlopEn
- 散布熵：MDE、RCMDE、TSMDE
- 模糊散布熵：MFuDE、CMFuDE、RCMFuDE、TSMFuDE
- 集成模糊散布熵：MEFuDE、CMEFuDE、RCMEFuDE、TSMEFuDE
- 样本熵与模糊熵：MSE、MFE
- 注意力熵：MAttEn
- 其他精细复合方法：RCMPE、RCMSlopEn

这些方法使用普通多尺度、复合多尺度、精细复合多尺度或时间移位多尺度
构造。具体区别见[方法选择](docs/zh-CN/methods.md)和
[算法手册](docs/zh-CN/algorithms/index.md)。

## 安全解释结果

- 比较不同信号时，应保持方法、参数、信号长度和预处理方式一致。
- 最大尺度越大，曲线末端可用的样本越少，不能脱离信号长度单独选择。
- 高层 API 会拒绝包含 `NaN` 或无穷大的信号。缺失值应先按研究目的明确处理。
- 不同算法家族或不同参数设置的熵值不一定处于同一数值尺度，不能只根据
  原始数值大小给方法排序。
- 工具箱不会自动完成滤波、去趋势、重采样或标准化。

这些规则的原因和实际检查方法见
[参数与数据准备](docs/zh-CN/parameters.md)。

## 项目状态

工具箱正在准备第一次公开发布。高层 API、打包配置、自动测试、引用信息、
来源说明和用户文档均已建立，目前尚未发布正式版本标签。

许可证和第三方声明以仓库中的英文原文为准。
