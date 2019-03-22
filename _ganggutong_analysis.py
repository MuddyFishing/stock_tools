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

# 存储为txt
def text_save(content1, filename, mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename, mode)
    for i in range(len(content1)):
        file.write(str(content1[i]))
    file.close()


# 读取txt
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename, 'r')
    except IOError:
        error = []
        return error
    content1 = file.readlines()
    file.close()
    return content1


def download_documents(doc_url, save_path):
    f = open(save_path, 'wb')
    # print(save_path)
    picture_data = requests.get(doc_url)
    # print(picture_data.content)
    f.write(picture_data.content)
    f.close()
    print('download_documents done: ' + save_path)
    return save_path


# 裁剪图片每日一图
def crop_picture(picture_path, save_path_crop_pic):
    im = Image.open(picture_path)
    # 图片的宽度和高度
    img_size = im.size
    # print("图片宽度和高度分别是{}".format(img_size))
    ''' 裁剪：传入一个元组作为参数 元组里的元素分别是：
    （距离图片左边界距离x， 距离图片上边界距离y，
    距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h） '''
    # 截取图片中一块宽和高都是250的
    x = 0
    y = 0
    w = img_size[0]
    h = img_size[1] - 100
    region = im.crop((x, y, x + w, y + h))
    region.save(save_path_crop_pic)
    # 截取图片中一块宽是250和高都是300的
    # x = 100
    # y = 100
    # w = 250
    # h = 300
    # region = im.crop((x, y, x+w, y+h))
    # region.save("./crop_test2.jpeg")
    print('crop_picture done: ' + save_path_crop_pic)
    return save_path_crop_pic


# 裁剪图片网易下载的图
def crop_163_stock_picture(picture_path, save_path_crop_pic, cut_pixel):
    im = Image.open(picture_path)
    # 图片的宽度和高度
    img_size = im.size
    # print("图片宽度和高度分别是{}".format(img_size))
    ''' 裁剪：传入一个元组作为参数 元组里的元素分别是：
    （距离图片左边界距离x， 距离图片上边界距离y，
    距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h） '''
    # 截取图片中一块宽和高都是250的
    x = 0
    y = 0
    w = img_size[0]
    h = img_size[1] - cut_pixel
    region = im.crop((x, y, x + w, y + h))
    region.save(save_path_crop_pic)
    # 截取图片中一块宽是250和高都是300的
    # x = 100
    # y = 100
    # w = 250
    # h = 300
    # region = im.crop((x, y, x+w, y+h))
    # region.save("./crop_test2.jpeg")
    print('crop_picture done: ' + save_path_crop_pic)
    return save_path_crop_pic


# 图片压缩
def pic_thumb(pic_path_thumb, save_path_thumb, pic_width):
    im = Image.open(pic_path_thumb).convert('RGB')
    # print('格式', im.format, '，分辨率', im.size, '，色彩', im.mode)
    im.thumbnail((pic_width, int(im.size[1]/(im.size[0]/pic_width))))
    im.save(save_path_thumb, 'JPEG', quality=100)
    print('pic_thumb done: ' + save_path_thumb)
    return save_path_thumb


# 图片放大缩小
def pic_zoom(from_path, save_path_163, zoom_pixel):
    im = Image.open(from_path)
    # print('格式', im.format, '，分辨率', im.size, '，色彩', im.mode)
    out = im.resize((zoom_pixel, int(im.size[1]/(im.size[0]/zoom_pixel))), Image.ANTIALIAS)
    out.save(save_path_163, 'png', quality=100)
    print('pic_zoom done: ' + save_path_163)
    return save_path_163[:-4] + '.png'


# 云财经 龙虎榜评析图片
# www.yuncaijing.com/apps/hdd/observe/id_452.html
def lhb_yuncaijing():
    a = requests.get('http://www.yuncaijing.com/apps/hdd/observelist_1.html')
    url = 'http://stock.10jqka.com.cn/fupan/#fp_item_8'
    url1 = 'http://yuanchuang.10jqka.com.cn/djpingpan_list/'
    # a =requests.get(url1)
    print(a.text)


# tushare获取当日涨跌幅分布,返回各段数据[10,>7,>5>3>1>-1>-3>-5>-7>-10,-10]
def zdf_distribution(date_zdffb, save_path_zdffb):
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
    bar_render_path = save_path_zdffb[:-12] + 'bar_tozoom_' + date_zdffb + '.png'
    bar.render(path=bar_render_path)
    # pie
    attrpie = ['涨', '平', '跌']
    vpie = [validyes0+validyes1+validyes3+validyes5+validyes7+validyes10,valid0, validno0+validno1+validno3+validno5+validno7+validno10]
    pie = Pie("涨跌饼图", title_pos='center', width=400, height=400)
    pie.add("", attrpie, vpie, radius=[6, 15], label_text_color=None, is_label_show=True, legend_orient='vertical', legend_pos='left')
    pie_render_path = save_path_zdffb[:-12] + 'pie_tozoom_' + date_zdffb + '.png'
    pie.render(path=pie_render_path)
    
    pic_zoom(bar_render_path, save_path_zdffb, 740)
    print('zdf_distribution done: ' + save_path_zdffb)
    return save_path_zdffb


# 163大盘分时
# http://img1.money.126.net/chart/hs/time/540x360/0000001.png

# tgbhotstock
def hot_tgb(date_tgbhotstock, save_path_tgbhotstock):
    a = requests.get('https://www.taoguba.com.cn/hotPop')
    b = a.text.split('相关链接')
    c = b[1].split('24小时个股搜索热度')
    d = c[0]
    stockcode = re.findall(r'[sz,sh]{1}\d{6}', d)  # 30
    stockno = re.findall(r'<td>\d+</td>', d)        # 10
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
    bar.render(path=render_path)
    pic_zoom(render_path, save_path_tgbhotstock, 740)
    print('hot_tgb done: ' + save_path_tgbhotstock)
    return save_path_tgbhotstock


# 根据zt_hum_history函数返回的df数据，提取历史涨停数据生成图片
def pic_ztnum_hist_pyecharts(df_ztnum_hist, pic_ztnum_hist_path, date_str_ztnum_hist):

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
    bar.render(path=render_path)
    pic_zoom(render_path, pic_ztnum_hist_path, 740)
    print('pic_ztnum_hist_pyecharts done: ' + pic_ztnum_hist_path)
    return pic_ztnum_hist_path



# 裁剪图片分为三图
def crop_html_picture(date_crop_html_pic, picture_path, save_path_crop_pic):
    im = Image.open(picture_path)
    # 图片的宽度和高度
    img_size = im.size
    # print("图片宽度和高度分别是{}".format(img_size))
    ''' 裁剪：传入一个元组作为参数 元组里的元素分别是：
    （距离图片左边界距离x， 距离图片上边界距离y，
    距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h） '''
    # 截取图片中一块宽和高都是250的
    x = 0
    y = 0
    w = img_size[0]
    h1 = int(img_size[1]/3)
    h2 = int((img_size[1] - h1)/2)
    h3 = img_size[1] - h1 - h2

    region = im.crop((x, y, x + w, y + h1))
    region.save(save_path_crop_pic + date_crop_html_pic + '_h1.png')

    region = im.crop((x, y + h1, x + w, y + h1 + h2))
    region.save(save_path_crop_pic + date_crop_html_pic + '_h2.png')

    region = im.crop((x, y + h1 + h2, x + w, y + h1 + h2 + h3))
    region.save(save_path_crop_pic + date_crop_html_pic + '_h3.png')
    # 截取图片中一块宽是250和高都是300的
    # x = 100
    # y = 100
    # w = 250
    # h = 300
    # region = im.crop((x, y, x+w, y+h))
    # region.save("./crop_test2.jpeg")
    print('crop_html_picture done: ' + save_path_crop_pic + date_crop_html_pic + '_h1.jpeg')
    print('crop_html_picture done: ' + save_path_crop_pic + date_crop_html_pic + '_h2.jpeg')
    print('crop_html_picture done: ' + save_path_crop_pic + date_crop_html_pic + '_h3.jpeg')
    return save_path_crop_pic


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
