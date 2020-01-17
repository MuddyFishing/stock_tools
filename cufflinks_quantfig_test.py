import pandas as pd
import plotly as py
import cufflinks as cf
import tushare as ts
from copy import deepcopy
cf.set_config_file(offline=True,world_readable=False)

stock = { 'name': '中国平安', 'code': '601318' }
df = ts.get_hist_data(stock['code']).iloc[::-1]
print(df)

qf=cf.QuantFig(df,title=stock['name'],legend='top',name=stock['name'], up_color='red', down_color='green')

boll = deepcopy(qf)
boll.add_bollinger_bands(name="Boll通道")
boll.iplot()

# fig = df.iplot(kind='bar', barmode='stack', asFigure=True)
# py.offline.plot(fig)

# rsi = deepcopy(qf)
# rsi.add_sma()
# rsi.add_macd()
# rsi.add_volume()
# rsi.iplot()

cf.datagen.lines(1,500).ta_plot(study='sma',period=[13,21,55])
