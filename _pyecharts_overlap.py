from pyecharts import Line, Bar, Overlap
'''
    多个x y轴示例
'''
 
 
attr = ["{}月".format(i) for i in range(1, 13)]
v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
v3 = [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
 
bar = Bar()
bar.add("蒸发量", attr, v1)
bar.add("降水量", attr, v2, yaxis_formatter=" ml",
        yaxis_interval=50, yaxis_max=250)
 
line = Line()
line.add("平均温度", attr, v3, yaxis_formatter=" °C", yaxis_interval=5)
 
overlap = Overlap(width=1200, height=600) # 实例化
# 默认不新增 x y 轴，并且 x y 轴的索引都为 0
overlap.add(bar)
# 新增一个 y 轴，此时 y 轴的数量为 2，第二个 y 轴的索引为 1（索引从 0 开始），所以设置 yaxis_index = 1
# 由于使用的是同一个 x 轴，所以 x 轴部分不用做出改变
overlap.add(line, yaxis_index=1, is_add_yaxis=True)
 
overlap.render("./Overlap_图表混合.html")
