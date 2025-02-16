import numpy as np

import matplotlib.pyplot as plt

def cal_heat(history:int)->int:
    heat=0
    for i in range(0,12):
        heat<<=1
        if history&1:
            heat|=1
        history>>=1
    return heat
raw_history_input=[]
with open("400.perlbench.history","r") as f:
    raw_history_input=f.readlines()
plot_data=[]
i=0
while i < len(raw_history_input):
    if "round=" in raw_history_input[i]:
        i=i+1
        index=raw_history_input[i].find("=")
        record_amount=int(raw_history_input[i][index+1:])
        i=i+1

        heat_array=[0 for j in range(0,4096)]
        for j in range(record_amount):
            line=raw_history_input[i+j]
            index=line.find("-")
            left_pfn=int(line[:index])
            line=line[index+1:]
            index=line.find(":")
            right_pfn=int(line[:index])
            history=int(line[index+1:])
            heat=cal_heat(history)
            heat_array[heat]+=right_pfn-left_pfn
        i+=record_amount
        print(heat_array)
        plot_data.append(heat_array)

data_array = np.array(plot_data)
data_array=data_array.transpose()
# 获取数据的形状（列数和行数）
num_cols = len(plot_data)
num_rows = len(plot_data[0])
print(num_cols)
print(num_rows)
# 绘制热图
plt.figure(figsize=(10, 8))
plt.imshow(data_array, cmap='hot', interpolation='nearest')

# 设置热图的标签
plt.xlabel('X 轴')
plt.ylabel('Y 轴')

# 设置X轴刻度
plt.xticks(np.arange(num_cols), np.arange(num_cols))

# 设置Y轴刻度
plt.yticks(np.arange(num_rows), np.arange(num_rows))

# 添加颜色条
plt.colorbar()

# 显示图形
plt.savefig("heat.png")