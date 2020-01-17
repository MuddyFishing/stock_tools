
from pyecharts import Bar, Line, Timeline, Overlap
from random import randint
 
attr = ["{}月".format(i) for i in range(1, 7)]
bar = Bar("1 月份数据", "数据纯属虚构")
bar.add("bar", attr, [randint(10, 50) for _ in range(6)])
line = Line()
line.add("line", attr, [randint(50, 80) for _ in range(6)])
overlap = Overlap()
overlap.add(bar)
overlap.add(line)
 
bar_1 = Bar("2 月份数据", "数据纯属虚构")
bar_1.add("bar", attr, [randint(10, 50) for _ in range(6)])
line_1 = Line()
line_1.add("line", attr, [randint(50, 80) for _ in range(6)])
overlap_1 = Overlap()
overlap_1.add(bar_1)
overlap_1.add(line_1)
 
bar_2 = Bar("3 月份数据", "数据纯属虚构")
bar_2.add("bar", attr, [randint(10, 50) for _ in range(6)])
line_2 = Line()
line_2.add("line", attr, [randint(50, 80) for _ in range(6)])
overlap_2 = Overlap()
overlap_2.add(bar_2)
overlap_2.add(line_2)
 
bar_3 = Bar("4 月份数据", "数据纯属虚构")
bar_3.add("bar", attr, [randint(10, 50) for _ in range(6)])
line_3 = Line()
line_3.add("line", attr, [randint(50, 80) for _ in range(6)])
overlap_3 = Overlap()
overlap_3.add(bar_3)
overlap_3.add(line_3)
 
bar_4 = Bar("5 月份数据", "数据纯属虚构")
bar_4.add("bar", attr, [randint(10, 50) for _ in range(6)])
line_4 = Line()
line_4.add("line", attr, [randint(50, 80) for _ in range(6)])
overlap_4 = Overlap()
overlap_4.add(bar_4)
overlap_4.add(line_4)
 
timeline = Timeline(
                    page_title = "页标签名",
                    width=600,
                    height=600,
                    is_auto_play= True, # 是否自动播放，默认=False
                    is_loop_play= True, # 是否循环播放
                    is_rewind_play=False, # 反向播放
                    is_timeline_show=True, # 是否显示时间线，默认=true
                    timeline_play_interval=1000, # 播放间隔，ms
                    timeline_symbol= "arrow", # 时间点标记图形， 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
                    timeline_symbol_size= [15,8], # 图形大小，可以是数字和列表，列表表示宽高
                    timeline_left= "1% ", # 距离左边距离 , timeline_right
                    timeline_bottom=0, # timeline_top
            )
timeline.add(overlap, '1 月')
timeline.add(overlap_1, '2 月')
timeline.add(overlap_2, '3 月')
timeline.add(overlap_3, '4 月')
timeline.add(overlap_4, '5 月')
timeline.render("./Timeline_时间线轮播多张图表.html")
