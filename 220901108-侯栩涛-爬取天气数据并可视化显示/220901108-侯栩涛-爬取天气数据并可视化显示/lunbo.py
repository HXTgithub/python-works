import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie ,Bar,Timeline,Page

# 读csv的数据
f = pd.read_csv('data.csv', encoding='gb18030')
#print("111")
print(f['日期'])

# 转换日期类型
f['日期'] = f['日期'].apply(lambda x: pd.to_datetime(x))
#print("222")
print(f['日期'])

# 提取日期中的月份数据
f['month'] = f['日期'].dt.month
print(f['month'])
print(f)
# 按照月份进行分组
f_agg = f.groupby(['month','天气']).size().reset_index()
print(f_agg)

# 设置列名
f_agg.columns = ['month','tianqi','count']
print(f_agg)

# 提取1月的数据，并转换为列表形式
print(f_agg[f_agg['month']==1][['tianqi','count']].sort_values(by='count',ascending=False).values.tolist())

timeline = Timeline()
timeline.add_schema(play_interval=1000)    # 单位是:ms(毫秒)

#第一个网页
#遍历月份
for month in f_agg['month'].unique():
    data = (

        f_agg[f_agg['month']==month][['tianqi','count']]
        .sort_values(by='count',ascending=True)
        .values.tolist()
    )
    #画图
    bar = Bar()
    # x
    bar.add_xaxis([x[0] for x in data])
    # y
    bar.add_yaxis('',[x[1] for x in data])

    bar.set_series_opts(label_opts=opts.LabelOpts(position='top'))
    # 图表的名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title='安阳2024年每月天气变化 '))
    # 将表放置到时间轮播图中
    timeline.add(bar, f'{month}月')
# 将第一个表存到weathers1文件
timeline.render('show1.html')

#第二个网页
#按天气统计分组，统计天气的次数
w_counts = f.groupby('天气').size().reset_index(name='count')

#计算
total_count = w_counts['count'].sum()
w_counts['percentage'] = (w_counts['count'] / total_count) * 100

#绘图数据
w_names = w_counts['天气'].tolist()  # 天气类型
percent = w_counts['percentage'].tolist()  # 百分比

#柱状图
bar1 = Bar()
bar1.add_xaxis(w_names)
bar1.add_yaxis("占比（%）", percent)
bar1.set_global_opts(
    title_opts=opts.TitleOpts(title="2024年每种天气占比(%)"),
    yaxis_opts=opts.AxisOpts(name="占比（%）", axislabel_opts=opts.LabelOpts(formatter="{value}%")),
    xaxis_opts=opts.AxisOpts(name="天气类型"),
)

#扇形图
pie = Pie()
pie.add(
    "",
    [list(z) for z in zip(w_names, percent)],
    radius=["25%", "50%"],  # 设置内外半径
)
pie.set_series_opts(
    label_opts=opts.LabelOpts(formatter="{b}: {d}%")  # 显示百分比
)

# 将两个图表放入一个容器
page = Page()
page.add(bar1,pie)

# 渲染为 HTML 文件
page.render("show2.html")

