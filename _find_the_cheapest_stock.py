# -*- coding: utf-8 -*-
# author: 微信号 pp_LoveSmile
# author: 公众号 摸鱼大佬
__author__ = 'Roy T.Burns'

import pymongo
from PIL import Image
import json
import tushare as ts
import time, datetime
import random
import requests
import pandas as pd
import numpy as np

import tushare as ts
# ts.set_token('your token here')
pro = ts.pro_api()

from pyecharts import Line, Bar, Pie, configure, Overlap
configure(output_image=True)

save_path = 'D:\\tools\\'


# stock index amount
def moneyflow_a_stock_all(date_start, date_end, save_path_moneyflow_ggt=''):
    # '000001.SH', '上证指数'
    # '399001.SZ', '深证成指'
    # '399006.SZ', '创业板指'
    # '399005.SZ', '中小板指'
    df1 = pro.index_daily(ts_code='000001.SH', start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    df2 = pro.index_daily(ts_code='399001.SZ', start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    # df3 = pro.index_daily(ts_code='399006.SZ', start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    # df4 = pro.index_daily(ts_code='399005.SZ', start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    # df5 = pro.index_daily(ts_code='399300.SZ', start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)

    df0 = pd.DataFrame()
    df0['amount'] = df1['amount'] + df2['amount']
    df0['trade_date'] = df1['trade_date']

    df0 = df0.assign(amount=df0.amount.apply(lambda x:round(x/100000, 0)))
    df1 = df1.assign(amount=df1.amount.apply(lambda x:round(x/100000, 0)))
    df2 = df2.assign(amount=df2.amount.apply(lambda x:round(x/100000, 0)))

    title = ' 盘面资金 - A股(亿元)'
    subtitle = '    GZH: 摸鱼大佬'
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("macarons")
    bar.add("上证", df1['trade_date'], df1['amount'], bar_category_gap='40%')
    bar.add("深证", df2['trade_date'], df2['amount'], bar_category_gap='40%')
    line = Line()
    line.add("全市场", df0['trade_date'], df0['amount'], mark_line=['average'], mark_point=['min', 'max'])
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line, is_add_xaxis=False)  #是否新增一个 x 坐标轴，默认为 False
    render_path = save_path + 'moneyflow_a_stock_all_' + date_end + '.png'
    # bar.render(path=render_path)
    overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_ggt done: ' + render_path)
    return render_path


# moneyflow_hsgt
def moneyflow_lgt(date_start, date_end, df, save_path_moneyflow_lgt):

    df = df.assign(hgt=df.hgt.apply(lambda x:round(x/100, 2)))
    df = df.assign(sgt=df.sgt.apply(lambda x:round(x/100, 2)))
    df = df.assign(north_money=df.north_money.apply(lambda x:round(x/100, 2)))

    title = ' 资金流向 - 陆股通(亿元)'
    subtitle = '    GZH: 摸鱼大佬'
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("macarons")
    bar.add("沪股通", df['trade_date'], df['hgt'], bar_category_gap='40%')
    bar.add("深股通", df['trade_date'], df['sgt'], bar_category_gap='40%')
    line = Line()
    line.add("北上资金", df['trade_date'], df['north_money'], mark_line=['average'], mark_point=['min', 'max'])
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line, is_add_xaxis=False)  #是否新增一个 x 坐标轴，默认为 False
    render_path = save_path + 'moneyflow_lgt_' + date_end + '.png'
    # bar.render(path=render_path)
    overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_lgt done: ' + render_path)
    return render_path


# moneyflow_hsgt
def moneyflow_ggt(date_start, date_end, df, save_path_moneyflow_ggt):

    df = df.assign(ggt_ss=df.ggt_ss.apply(lambda x:round(x/100, 2)))
    df = df.assign(ggt_sz=df.ggt_sz.apply(lambda x:round(x/100, 2)))
    df = df.assign(south_money=df.south_money.apply(lambda x:round(x/100, 2)))

    title = ' 资金流向 - 港股通(亿元)'
    subtitle = '    GZH: 摸鱼大佬'
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("macarons")
    bar.add("港股通(沪)", df['trade_date'], df['ggt_ss'], bar_category_gap='40%')
    bar.add("港股通(深)", df['trade_date'], df['ggt_sz'], bar_category_gap='40%')
    line = Line()
    line.add("南下资金", df['trade_date'], df['south_money'], mark_line=['average'], mark_point=['min', 'max'])
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line, is_add_xaxis=False)  #是否新增一个 x 坐标轴，默认为 False
    render_path = save_path + 'moneyflow_ggt_' + date_end + '.png'
    # bar.render(path=render_path)
    overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_ggt done: ' + render_path)
    return render_path


if __name__ == '__main__':
    # date_str_today = last_trade_date()  # 20180713
    now_time = datetime.datetime.now()
    change_time = now_time + datetime.timedelta(days=-60)
    date_start = change_time.strftime('%Y%m%d')

    # date_start = time.strftime("%Y%m%d", time.localtime() + datetime.timedelta(days=-7))
    date_today = time.strftime("%Y%m%d", time.localtime())
    print(date_today)

    df = pro.trade_cal(exchange='', start_date=date_start, end_date=date_today, fields='exchange,cal_date,is_open,pretrade_date', is_open='1')
    date_last_trade_day = df.at[len(df) - 1, 'cal_date']
    print(date_last_trade_day)

    df = pro.moneyflow_hsgt(start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    print(df)
    # print(df['trade_date'])
    moneyflow_lgt(date_start, date_last_trade_day, df, '')
    moneyflow_ggt(date_start, date_last_trade_day, df, '')

    moneyflow_a_stock_all(date_start=date_start, date_end=date_last_trade_day)
    
    print('Done!')
