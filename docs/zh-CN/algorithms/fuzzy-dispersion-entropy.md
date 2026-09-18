# 模糊散布熵

[English](../../algorithms/fuzzy-dispersion-entropy.md) | 简体中文

已实现的多尺度方法：**MFuDE**、**CMFuDE**、**RCMFuDE** 和 **TSMFuDE**。

## 定义

模糊散布熵用相互重叠的隶属函数替代散布熵的硬类别划分。一个样本可以部分属于相邻类别，因此类别边界附近的小幅变化不一定会把一种模式完全切换为另一种模式。

## 核心步骤

通过正态累积分布函数映射每个样本，并将其放到连续类别轴上：

$$
y_i
=
\Phi\!\left(\frac{x_i-\mu}{\sigma}\right),
\qquad
z_i=n_c y_i+\frac{1}{2}.
$$

对于每个类别 $c\in\{1,\ldots,n_c\}$，计算隶属度 $u_c(z_i)\in[0,1]$。中间类别使用三角隶属函数，首尾类别使用梯形边界函数。

对于类别模式

$$
\pi=(c_1,c_2,\ldots,c_m),
$$

从 $i$ 开始的延迟窗口对该模式的隶属度为

$$
U_i(\pi)
=
\prod_{j=0}^{m-1}
u_{c_{j+1}}\!\left(z_{i+j\tau}\right).
$$

完整窗口数为

$$
W=N-(m-1)\tau,
$$

由此估计模糊模式分布：

$$
p(\pi)
=
\frac{1}{W}\sum_{i=1}^{W}U_i(\pi).
$$

最后计算

$$
H_{\mathrm{FuDE}}
=
-\sum_{\pi:p(\pi)>0}p(\pi)\ln p(\pi).
$$

已注册方法按以下方式使用该估计器：

- **MFuDE**：每个尺度使用一条标准粗粒化序列。
- **CMFuDE**：为每个复合偏移计算熵，再平均熵值。
- **RCMFuDE**：先平均各偏移的模糊模式分布，再计算熵。
- **TSMFuDE**：为每个时间移位相位计算熵，再平均各相位结果。

## 参数含义

- `m`：每个模式中的模糊类别数。
- `nc`：模糊幅值类别数；模式空间包含 $n_c^m$ 种模式。
- `tau`：模式元素之间的延迟，单位为样本点。
- `scale`：MFuDE、CMFuDE 和 RCMFuDE 的最大尺度。
- `kmax`：TSMFuDE 的最大时间移位尺度。
- `type_`：部分高层方法保留的熵分支选择参数。默认值 `0` 是已有文档说明并受支持的 Shannon 熵分支。

## 结果

MFuDE、CMFuDE 和 RCMFuDE 返回 `scale` 个值；TSMFuDE 返回 `kmax` 个值。数值越大，表示模糊散布模式的隶属度在模式空间中分布越均匀。

结果使用自然对数，且未除以 $\ln(n_c^m)$。比较信号时应使用相同的参数和多尺度构造。

另见[多尺度构造](multiscale-constructions.md)和[英文参考文献列表](../../references.md)。
