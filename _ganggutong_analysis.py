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
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

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
    print(df0)

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


def get_float(x):
    if '亿元' in x:
        x = x.replace('亿元', '')
        return float(x) * 100
    if '万元' in x:
        x = x.replace('万元', '')
        return float(x) / 100
    pass


def get_moneyflow_hsgt_today(browser, trade_date):
    url_1 = "http://quote.eastmoney.com/center/hsgt.html"

    # table class 'dataTable no-footer'
    browser.get(url_1)
    imgelement = browser.find_element_by_class_name('dataTable')
    print(imgelement.text)

    # 类型 板块 板块涨跌幅 资金方向 交易状态 资金净流入 当日资金余额 当日资金限额 上涨数 持平数 下跌数 相关指数
    # 沪港通 沪股通 -1.51% 北向 收盘 12.16亿元 507.84亿元 520.00亿元 89 3 488 上证指数
    # 港股通(沪) -0.10% 南向 额度可用 7.10亿元 412.90亿元 420.00亿元 140 20 164 恒生指数
    # 深港通 深股通 -1.95% 北向 收盘 1.39亿元 518.61亿元 520.00亿元 106 11 620 深成指数
    # 港股通(深) -0.10% 南向 额度可用 4.00亿元 416.00亿元 420.00亿元 203 30 246 恒生指数
    list1 = imgelement.text.split('\n')
    
    # #    trade_date  ggt_ss  ggt_sz      hgt      sgt  north_money  south_money
    # # 0    20180808  -476.0  -188.0   962.68   799.94      1762.62       -664.0
    # # 1    20180807  -261.0   177.0  2140.85  1079.82      3220.67        -84.0
    tab_dict = {}
    # hgt     = list1[1].split(' ')[5].replace('亿元', '')
    # hgt     = list1[1].split(' ')[5][:-2]
    # ggt_ss  = list1[2].split(' ')[4].replace('亿元', '')
    # sgt     = list1[3].split(' ')[5].replace('亿元', '')
    # ggt_sz  = list1[4].split(' ')[4].replace('亿元', '')
    tab_dict['trade_date'] = trade_date
    # tab_dict['ggt_ss'] = float(ggt_ss) * 100
    # tab_dict['ggt_sz'] = float(ggt_sz) * 100
    # tab_dict['hgt'] = float(hgt) * 100
    # tab_dict['sgt'] = float(sgt) * 100
    tab_dict['ggt_ss'] = get_float(list1[2].split(' ')[4])
    tab_dict['ggt_sz'] = get_float(list1[4].split(' ')[4])
    tab_dict['hgt'] = get_float(list1[1].split(' ')[5])
    tab_dict['sgt'] = get_float(list1[3].split(' ')[5])
    tab_dict['north_money'] = tab_dict['hgt'] + tab_dict['sgt']
    tab_dict['south_money'] = tab_dict['ggt_ss'] + tab_dict['ggt_sz']

    tab_list = []
    # tab_list.append(tab_dict.values)
    tab_list.append(tab_dict['trade_date'])
    tab_list.append(tab_dict['ggt_ss'])
    tab_list.append(tab_dict['ggt_sz'])
    tab_list.append(tab_dict['hgt'])
    tab_list.append(tab_dict['sgt'])
    tab_list.append(tab_dict['north_money'])
    tab_list.append(tab_dict['south_money'])
    
    print(tab_dict)
    print(tab_list)
    return tab_dict, tab_list


if __name__ == '__main__':
    
    now_time = datetime.datetime.now()
    change_time = now_time + datetime.timedelta(days=-60)
    date_start = change_time.strftime('%Y%m%d')

    # date_start = time.strftime("%Y%m%d", time.localtime() + datetime.timedelta(days=-7))
    date_today = time.strftime("%Y%m%d", time.localtime())
    print(date_today)

    df = pro.trade_cal(exchange='', start_date=date_start, end_date=date_today, fields='exchange,cal_date,is_open,pretrade_date', is_open='1')
    date_last_trade_day = df.at[len(df) - 1, 'cal_date']
    print(date_last_trade_day)

    #    trade_date  ggt_ss  ggt_sz      hgt      sgt  north_money  south_money
    # 0    20180808  -476.0  -188.0   962.68   799.94      1762.62       -664.0
    # 1    20180807  -261.0   177.0  2140.85  1079.82      3220.67        -84.0
    df = pro.moneyflow_hsgt(start_date=date_start, end_date=date_last_trade_day).sort_index(ascending=False)
    print(df)
    # print(df['trade_date'])
    temp1, temp2 = get_moneyflow_hsgt_today(driver, date_last_trade_day)
    df = df.append(temp1, ignore_index=True)
    print(df)

    moneyflow_lgt(date_start, date_last_trade_day, df, '')
    moneyflow_ggt(date_start, date_last_trade_day, df, '')

    moneyflow_a_stock_all(date_start=date_start, date_end=date_last_trade_day)

    print('Done!')
