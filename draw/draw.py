import numpy as np
import matplotlib.pyplot as plt

# 设置Matplotlib为非交互模式
plt.ioff()

# 从文件中读取数据
data = np.loadtxt('plot_matrix')

# 获取数据的行数和列数
rows, cols = data.shape

# 绘制热图，设置extent参数
plt.imshow(data, cmap='hot', interpolation='nearest', extent=[0, cols, 0, rows])

plt.colorbar()  # 添加颜色条
plt.title('Heatmap')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("heatmap.png")
