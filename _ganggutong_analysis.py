# -*- coding: utf-8 -*-
# author: 微信号 pp_LoveSmile
# author: 公众号 摸鱼大佬
__author__ = 'Roy T.Burns'

import pymongo
from PIL import Image
import json
import re
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
driver = webdriver.Chrome(options=chrome_options)

import tushare as ts
# ts.set_token('your token here')
pro = ts.pro_api()

from pyecharts import Line, Bar, Pie, configure, Overlap, Page
# configure(output_image=True)

save_path = 'E:\\temp\\'


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
    # render_path = save_path + 'moneyflow_a_stock_all_' + date_end + '.png'
    render_path = save_path + 'moneyflow_a_stock_all_' + date_end + '.html'
    # bar.render(path=render_path)
    # overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_ggt done: ' + render_path)
    return render_path, overlap


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
    # render_path = save_path + 'moneyflow_lgt_' + date_end + '.png'
    render_path = save_path + 'moneyflow_lgt_' + date_end + '.html'
    # bar.render(path=render_path)
    # overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_lgt done: ' + render_path)
    return render_path, overlap


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
    # render_path = save_path + 'moneyflow_ggt_' + date_end + '.png'
    render_path = save_path + 'moneyflow_ggt_' + date_end + '.html'
    # bar.render(path=render_path)
    # overlap.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('moneyflow_ggt done: ' + render_path)
    return render_path, overlap


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


# 根据zt_hum_history函数返回的df数据，提取历史涨停数据生成图片
def zt_hum_history_render(df_ztnum_hist, pic_ztnum_hist_path, date_str_ztnum_hist):

    # 为什么取最前的21天的数据，因为和历史K线每月有21根，相对应
    ztnum = df_ztnum_hist.head(21)

    # 提取月份
    # month = (ztnum.iloc[:, 0].str[4:8])
    month = (ztnum.iloc[:, 0].str[0:8]) #如果是2019年01月，这里排序就会出问题，
    month = np.sort(month.map(lambda c: c)) 
    attr = ['{}'.format(i) for i in month]

    # 切片
    v1 = ztnum.iloc[:, 1]
    # v1 = ['{}'.format(i) for i in v1.values]
    v11 = []
    for x in v1:
        a = min(10000, int(x))
        v11.append(a)
    v22 = []
    v2 = ztnum.iloc[:, 3]
    for x in v2:
        a = min(10000, int(x))
        v22.append(a)
    # print(v11)
    # print(v22)
    # pyecharts参数
    title = ' 历史数据 - 每日涨跌停'
    subtitle = '    GZH: 摸鱼大佬'
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("infographic")
    bar.add("涨停数", attr, v11[::-1],   mark_line=['average'])
    bar.add("跌停数", attr, v22[::-1],   mark_line=['average'])
    render_path = pic_ztnum_hist_path[:-12] + 'tozoom_' + date_str_ztnum_hist + '.png'
    # bar.render(path=render_path)
    # pic_zoom(render_path, pic_ztnum_hist_path, 740)
    # print('zt_hum_history_render done: ' + pic_ztnum_hist_path)
    return render_path, bar


# 历史涨跌停数量，最近一个月的,递归算法
# api = 'http://home.flashdata2.jrj.com.cn/limitStatistic/month/201807.js'
def zt_hum_history(zt_his_text, date_zt_his, zt_next_num):

    # 如果递归数字<0，那就终止递归 return df，此处是统计数据
    # 第一次递归的zt_his_text=''是空的，逐步延长，最后一次递归统计此字符串
    if zt_next_num < 0:
        zt_np = []
        # 分割，提取，循环append成list
        zt_list = re.split(r'],\[', zt_his_text[1:-2])
        for j in range(0, len(zt_list), 1):
            zt_list_one = re.split(r',', zt_list[j])
            for k in range(0, len(zt_list_one), 1):
                if len(zt_list_one[k]) == 0:
                    zt_list_one[k] = 0
                zt_np.append(zt_list_one[k])
        # 转成数组，转成矩阵，转成df
        zt_np = np.array(zt_np)
        matrix = [[0 for p in range(0, len(zt_list_one), 1)] for q in range(0, len(zt_list), 1)]
        for m in range(0, len(zt_np)):
            a, b = divmod(m, 7)
            matrix[a][b] = zt_np[m]  # 将切分后的数据存入df中
            # print(a, b, matrix[a][b])
        df = pd.DataFrame(matrix, columns=pd.MultiIndex.from_product([['date', 'ztnum', 'ztnumcmp', 'dtnum', 'dtnumcmp',  'cash', 'cashcmp']]))
        print('zt_hum_history done: df数据已生成')
        return df

    month0 = int(date_zt_his[4:6])
    year0 = int(date_zt_his[0:4])
    month0url = date_zt_his[0:6]
    month0_data_tmp = requests.get('http://home.flashdata2.jrj.com.cn/limitStatistic/month/' + month0url + '.js')
    month0_data = month0_data_tmp.text
    month0_split1 = re.split(r'\[\[', month0_data)
    month0_split2 = re.split(r']]', month0_split1[1])
    if month0-1 == 0:
        month1 = 12
        year1 = year0-1
    else:
        month1 = month0-1
        year1 = year0
    month0_data_list = zt_his_text + '[' + month0_split2[0] + '],'
    zt_next_num -= 1
    print('zt_hum_history done: 还需递归次数 ' + str(zt_next_num + 1))
    return zt_hum_history(month0_data_list, str(year1) + str(month1).zfill(2), zt_next_num)


# tushare获取当日涨跌幅分布,返回各段数据[10,>7,>5>3>1>-1>-3>-5>-7>-10,-10]
def zd_fenbu():
    # tushare
    stockbasicinfo = ts.get_stock_basics()

    '''代码排序'''
    stockbasicinfo = stockbasicinfo.sort_index()

    '''股票总数'''
    stocknum = len(stockbasicinfo)
    # stockcode = stockbasicinfo.index[0]

    # 所有票的url拼接地址，用sina api去获取数据，因为tushare获取实时数据不稳定
    urllist = []
    for i in range(0, stocknum):
        stockcode = stockbasicinfo.index[i]
        stockcodeint = int(stockbasicinfo.index[i])
        if stockcodeint >= 600000:
            urllist.append('sh' + str(stockcode))
        else:
            urllist.append('sz' + str(stockcode))
    urllen = len(urllist)
    # print(urllen, urllist)
    (x, y) = divmod(urllen, 9)
    urlchar = ','.join(urllist)
    # print(urlchar)
    # 总共分成9份，因为sina每次请求不超过800
    urlbase = 'http://hq.sinajs.cn/list='
    url1 = urlbase + urlchar[0:9*x-1]
    url2 = urlbase + urlchar[9*x*1:9*x*2-1]
    url3 = urlbase + urlchar[9*x*2:9*x*3-1]
    url4 = urlbase + urlchar[9*x*3:9*x*4-1]
    url5 = urlbase + urlchar[9*x*4:9*x*5-1]
    url6 = urlbase + urlchar[9*x*5:9*x*6-1]
    url7 = urlbase + urlchar[9*x*6:9*x*7-1]
    url8 = urlbase + urlchar[9*x*7:9*x*8-1]
    url9 = urlbase + urlchar[9*x*8:]
    datatemp1 = requests.get(url1)
    datatemp2 = requests.get(url2)
    datatemp3 = requests.get(url3)
    datatemp4 = requests.get(url4)
    datatemp5 = requests.get(url5)
    datatemp6 = requests.get(url6)
    datatemp7 = requests.get(url7)
    datatemp8 = requests.get(url8)
    datatemp9 = requests.get(url9)
    # 获取的数据进行合并
    urldata = datatemp1.text + datatemp2.text + datatemp3.text + datatemp4.text + datatemp5.text + datatemp6.text + datatemp7.text + datatemp8.text + datatemp9.text
    urlsplit = re.split(r'=', urldata)
    # print(len(urlsplit))
    validnum = 0
    validzflist = []
    validyes10 = 0
    validyes7 = 0
    validyes5 = 0
    validyes3 = 0
    validyes1 = 0
    validyes0 = 0
    valid0 = 0
    validno0 = 0
    validno1 = 0
    validno3 = 0
    validno5 = 0
    validno7 = 0
    validno10 = 0
    # 数据分割，提取，整理
    for i in range(1, len(urlsplit)):
        if len(urlsplit[i]) > 100:
            urldataone = re.split(r',', urlsplit[i])
            yesprice = float(urldataone[2])
            nowprice = float(urldataone[3])
            amount = float(urldataone[9])
            buyonevol = float(urldataone[10])
            sellonevol = float(urldataone[20])
            if amount < 0.1:
                pass
            else:
                if nowprice < 0.1:
                    pass
                else:
                    if yesprice < 0.1:
                        pass
                    else:
                        zdf = int(10000*(nowprice/yesprice - 1) + 0.5)/100
                        if abs(zdf) < 11:
                            validnum += 1
                            validzflist.append(zdf)
                            if zdf >= 9.8 and sellonevol < 0.1:
                                validyes10 += 1
                            if zdf >= 7 and sellonevol > 0.1:
                                validyes7 += 1
                            if 5 <= zdf < 7:
                                validyes5 += 1
                            if 3 <= zdf < 5:
                                validyes3 += 1
                            if 1 <= zdf < 3:
                                validyes1 += 1
                            if 0.0001 <= zdf < 1:
                                validyes0 += 1
                            if abs(zdf) <= 0.0001:
                                valid0 += 1
                            if -1 < zdf < -0.0001:
                                validno0 += 1
                            if -3 < zdf <= -1:
                                validno1 += 1
                            if -5 < zdf <= -3:
                                validno3 += 1
                            if -7 < zdf <= -5:
                                validno5 += 1
                            if zdf <= -7 and buyonevol > 0.1:
                                validno7 += 1
                            if zdf <= -9.8 and buyonevol < 0.1:
                                validno10 += 1
    # 数据整理
    v11 = [0, 0, 0, 0, 0, 0, 0, validyes0, validyes1, validyes3, validyes5, validyes7, 0]
    v22 = [0, validno7, validno5, validno3, validno1, validno0, 0, 0, 0, 0, 0, 0, 0]
    v00 = [0, 0, 0, 0, 0, 0, valid0, 0, 0, 0, 0, 0, 0]
    vzt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, validyes10]
    vdt = [validno10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    attr = ['-10%', '>-7%', '-7~5%', '-5~3%', '-3~1%', '-1~0%', '0', '0~1%', '1~3%', '3~5%', '5~7%', '>7%', '10%']

    # 调用pyecharts
    title = ' 涨跌分布：↑' + str(validyes0+validyes1+validyes3+validyes5+validyes7+validyes10) +  \
            ' ↓' + str(validno0+validno1+validno3+validno5+validno7+validno10) + '  →' + str(valid0)
    subtitle = '    GZH: 摸鱼大佬'
    # bar
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("shine")
    bar.add("涨", attr, v11, bar_category_gap=0, mark_point=['max', 'average'])
    bar.add("", attr, vzt, bar_category_gap=0, mark_point=['max'])
    bar.add("平", attr, v00, bar_category_gap=0, mark_point=['max'])
    bar.add("跌", attr, v22, bar_category_gap=0, mark_point=['max', 'average'])
    bar.add("", attr, vdt,  bar_category_gap=0, mark_point=['max'])
    # bar_render_path = save_path_zdffb[:-12] + 'bar_tozoom_' + date_zdffb + '.png'
    # bar.render(path=bar_render_path)
    # pie
    attrpie = ['涨', '平', '跌']
    vpie = [validyes0+validyes1+validyes3+validyes5+validyes7+validyes10,valid0, validno0+validno1+validno3+validno5+validno7+validno10]
    pie = Pie("涨跌饼图", title_pos='center', width=400, height=400)
    pie.add("", attrpie, vpie, radius=[6, 15], label_text_color=None, is_label_show=True, legend_orient='vertical', legend_pos='left')
    # pie_render_path = save_path_zdffb[:-12] + 'pie_tozoom_' + date_zdffb + '.png'
    # pie.render(path=pie_render_path)
    
    # pic_zoom(bar_render_path, save_path_zdffb, 740)
    # print('zdf_distribution done: ' + save_path_zdffb)
    # return bar_render_path
    return bar, pie


# 弹股吧 搜索热度
def hot_tgb(date_tgbhotstock, save_path_tgbhotstock):
    a = requests.get('https://www.taoguba.com.cn/hotPop')
    b = a.text.split('相关链接')
    c = b[1].split('24小时个股搜索热度')
    d = c[0]
    # stockcode = re.findall(r'[sz,sh]{1}\d{6}', d)  # 30
    # stockno = re.findall(r'<td>\d+</td>', d)        # 10
    stockhotvalue = re.findall(r'<td >\d+</td>', d)  # 20
    stockname_ = re.findall(r'[\*ST,ST,\*,SST,GQY,S,N,TCL,XD,G,XR]{0,1}[\u4e00-\u9fa5]{2,4}', d)  # 10
    v1 = []  # 今日搜索
    v2 = []  # 最近7天搜索
    for i in range(0, len(stockhotvalue)):
        (x, y) = divmod(i, 2)
        if y == 0:
            v1.append(int(stockhotvalue[i].replace('<td >', "").replace('</td>', "")))
        else:
            v2.append(int(stockhotvalue[i].replace('<td >', "").replace('</td>', "")))
    
    stockname = []
    for j in range(0, len(stockname_)):
        # print(len(stockname[j]))
        if len(stockname_[j]) > 2:
            stockname.append(stockname_[j])

    title = ' 搜索热度 - 人气妖股'
    subtitle = '    GZH: 摸鱼大佬'
    bar = Bar(title, subtitle, title_pos=0.1, subtitle_text_size=15, subtitle_color='#aa8')
    # bar.use_theme("macarons")
    bar.add("today", stockname, v1, bar_category_gap='80%', is_stack=True)
    bar.add("7day", stockname, v2, bar_category_gap='80%', is_stack=True)
    render_path = save_path_tgbhotstock[:-12] + 'hot_stock_tgb_' + date_tgbhotstock + '.png'
    # bar.render(path=render_path)
    # pic_zoom(render_path, save_path_tgbhotstock, 740)
    # print('hot_tgb done: ' + save_path_tgbhotstock)
    return render_path, bar


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

    _, overlap_1 = moneyflow_lgt(date_start, date_last_trade_day, df, '')
    _, overlap_2 = moneyflow_ggt(date_start, date_last_trade_day, df, '')
    _, overlap_3 = moneyflow_a_stock_all(date_start=date_start, date_end=date_last_trade_day)
    
    _, bar_1 = zt_hum_history_render(zt_hum_history('', date_last_trade_day, 1), './', date_last_trade_day)
    bar_2, pie_2 = zd_fenbu()
    # _, bar_3 = hot_tgb(date_last_trade_day, './')

    # 
    page = Page()
    page.add(overlap_3)
    page.add(overlap_1)
    page.add(overlap_2)
    
    page.add(bar_1)
    page.add(bar_2)
    page.add(pie_2)
    # page.add(bar_3)

    page.render(save_path + "daily_report_%s.html" % date_last_trade_day)

    print('Done!')

    # from pyecharts import Bar
    # bar = Bar("我的第一个图表", "这里是副标题")
    # bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
    # bar.show_config()
    # bar.render(save_path + 'xxx.png')
