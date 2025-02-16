# 设置绘图样式
set terminal pngcairo  # 指定输出文件格式为PNG
set output "heatmap.png"  # 指定输出文件名为heatmap.png

set title "Heatmap"
set xlabel "X"
set ylabel "Y"
set xrange [0:454]
set yrange [0:1633280]

# 定义归一化函数
normalize(x) = (x - min) / (max - min)
min = 0
max = 32

# 设置调色板
set palette defined (0 "blue", 1 "green", 2 "yellow", 3 "red")

# 绘制热图
plot "plot_matrix" matrix using 1:2:(normalize($3)) with image