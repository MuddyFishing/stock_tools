# -*- coding=utf-8 -*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
# 每天的涨跌停
import re
import time
import xlrd
import xlwt
import sys
import os
import setting
from setting import is_holiday, DATA_PATH
import pandas as pd
import tushare as ts
from setting import llogger
import requests
from send_mail import sender_139
import datetime
# reload(sys)
# sys.setdefaultencoding('gbk')

logger = llogger(__file__)


class GetZDT:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36"
        self.today = time.strftime("%Y%m%d")
        self.path = DATA_PATH
        self.zdt_url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/' + \
            self.today + ".js"
        self.zrzt_url = 'http://hqdata.jrj.com.cn/zrztjrbx/limitup.js'

        self.host = "home.flashdata2.jrj.com.cn"
        self.reference = "http://stock.jrj.com.cn/tzzs/zdtwdj/zdforce.shtml"

        self.header_zdt = {"User-Agent": self.user_agent,
                           "Host": self.host,
                           "Referer": self.reference}

        self.zdt_indexx = [u'代码', u'名称', u'最新价格', u'涨跌幅', u'封成比', u'封流比', u'封单金额', u'最后一次涨停时间', u'第一次涨停时间', u'打开次数',
                           u'振幅',
                           u'涨停强度']

        self.zrzt_indexx = [u'序号', u'代码', u'名称', u'昨日涨停时间', u'最新价格', u'今日涨幅', u'最大涨幅', u'最大跌幅', u'是否连板', u'连续涨停次数',
                            u'昨日涨停强度', u'今日涨停强度', u'是否停牌', u'昨天的日期', u'昨日涨停价', u'今日开盘价格', u'今日开盘涨幅']
        self.header_zrzt = {"User-Agent": self.user_agent,
                            "Host": "hqdata.jrj.com.cn",
                            "Referer": "http://stock.jrj.com.cn/tzzs/zrztjrbx.shtml"
                            }

    def getdata(self, url, headers, retry=5):
        for i in range(retry):
            try:
                resp = requests.get(url=url, headers=headers)
                content = resp.text
                md_check = re.findall('summary|lasttradedate', content)
                if content and len(md_check) > 0:
                    return content
                else:
                    time.sleep(60)
                    logger.info('failed to get content, retry: {}'.format(i))
                    continue
            except Exception as e:
                logger.info(e)
                time.sleep(60)
                continue
        return None

    def convert_json(self, content):
        p = re.compile(r'"Data":(.*)};', re.S)
        if len(content) <= 0:
            logger.info('Content\'s length is 0')
            exit(0)
        result = p.findall(content)
        if result:
            try:
                # print(result)
                t1 = result[0]
                t2 = list(eval(t1))
                return t2
            except Exception as e:
                logger.info(e)
                return None
        else:
            return None

    # 2016-12-27 to do this
    def save_excel(self, date, data):
        # data is list type
        w = xlwt.Workbook(encoding='gbk')
        ws = w.add_sheet(date)
        excel_filename = date + ".xls"
        # sheet=open_workbook(excel_filenme)
        # table=wb.sheets()[0]
        xf = 0
        ctype = 1
        rows = len(data)
        point_x = 1
        point_y = 0
        ws.write(0, 0, u'代码')
        ws.write(0, 1, u'名称')
        ws.write(0, 2, u'最新价格')
        ws.write(0, 3, u'涨跌幅')
        ws.write(0, 4, u'封成比')
        ws.write(0, 5, u'封流比')
        ws.write(0, 6, u'封单金额')
        ws.write(0, 7, u'第一次涨停时间')
        ws.write(0, 8, u'最后一次涨停时间')
        ws.write(0, 9, u'打开次数')
        ws.write(0, 10, u'振幅')
        ws.write(0, 11, u'涨停强度')
        print("Rows:%d" % rows)
        for row in data:
            rows = len(data)
            cols = len(row)
            point_y = 0
            for col in row:
                # print(col)
                # table.put_cell(row,col,)
                # print(col)
                ws.write(point_x, point_y, col)
                # print("[%d,%d]" % (point_x, point_y))
                point_y = point_y + 1

            point_x = point_x + 1

        w.save(excel_filename)

    def save_to_dataframe(self, data, indexx, choice, post_fix):
        engine = setting.get_engine('db_zdt')
        if not data:
            exit()
        data_len = len(data)
        if choice == 1:
            for i in range(data_len):
                data[i][choice] = data[i][choice]

        df = pd.DataFrame(data, columns=indexx)

        filename = os.path.join(
            self.path, self.today + "_" + post_fix + ".xls")

        # 今日涨停
        if choice == 1:
            df['今天的日期'] = self.today
            df.to_excel(filename, encoding='gbk')
            try:
                df.to_sql(self.today + post_fix, engine, if_exists='fail')
            except Exception as e:
                logger.info(e)
        # 昨日涨停
        if choice == 2:
            df = df.set_index(u'序号')
            df[u'最大涨幅'] = df[u'最大涨幅'].map(lambda x: round(x * 100, 3))
            df[u'最大跌幅'] = df[u'最大跌幅'].map(lambda x: round(x * 100, 3))
            df[u'今日开盘涨幅'] = df[u'今日开盘涨幅'].map(lambda x: round(x * 100, 3))
            df[u'昨日涨停强度'] = df[u'昨日涨停强度'].map(lambda x: round(x, 0))
            df[u'今日涨停强度'] = df[u'今日涨停强度'].map(lambda x: round(x, 0))
            try:
                df.to_sql(self.today + post_fix, engine, if_exists='fail')
            except Exception as e:
                logger.info(e)

            avg = round(df['今日涨幅'].mean(), 2)
            current = datetime.datetime.now().strftime('%Y-%m-%d')
            title = '昨天涨停个股今天{}\n的平均涨幅{}\n'.format(current, avg)
            try:
                sender_139(title, title)
            except Exception as e:
                print(e)

    # 昨日涨停今日的状态，今日涨停

    def storedata(self):
        zdt_content = self.getdata(self.zdt_url, headers=self.header_zdt)
        logger.info('zdt Content' + zdt_content)
        zdt_js = self.convert_json(zdt_content)
        self.save_to_dataframe(zdt_js, self.zdt_indexx, 1, 'zdt')
        time.sleep(0.5)
        zrzt_content = self.getdata(self.zrzt_url, headers=self.header_zrzt)
        logger.info('zrzt Content' + zdt_content)

        zrzt_js = self.convert_json(zrzt_content)
        self.save_to_dataframe(zrzt_js, self.zrzt_indexx, 2, 'zrzt')


if __name__ == '__main__':
    # today='2018-04-16'
    # 填补以前的数据
    # x=pd.date_range('20170101','20180312')
    # date_list = [datetime.datetime.strftime(i,'%Y%m%d') for i in list(pd.date_range('20170401','20171231'))

    if is_holiday():
        logger.info('Holiday')
        exit()
    logger.info("start")
    obj = GetZDT()
    obj.storedata()
