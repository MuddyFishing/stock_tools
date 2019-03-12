# -*-coding=utf-8-*-
import re

__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
# 交割单处理 保存交割单到数据库
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from setting import get_engine, get_mysql_conn

engine = get_engine('db_stock', local=True)
pd.set_option('display.max_rows', None)


class Delivery_Order():

    def __init__(self):

        path = os.path.join(os.getcwd(), 'private/2019/GJ')
        if os.path.exists(path) == False:
            os.mkdir(path)
        os.chdir(path)

    # 合并一年的交割单
    def years_ht(self):
        df_list = []
        for i in range(1, 2):
            # 固定一个文件
            filename = 'HT_2018-05_week4-5.xls'
            # filename='2018-%s.xls' %str(i).zfill(2)
            # filename='HT_2018_%s.xls' %str(i).zfill(2)
            print(filename)
            try:
                t = pd.read_table(filename, encoding='gbk',
                                  dtype={u'证券代码': np.str})
            except Exception as e:
                print(e)
                continue
            # fee=t[u'手续费'].sum()+t[u'印花税'].sum()+t[u'其他杂费'].sum()
            # print(i," fee: ")
            # print(fee)
            df_list.append(t)
            # result.append(fee)
        df = pd.concat(df_list)
        df = df.reset_index()
        # df[u'xxxx']=df[u'成交日期']+df[u'成交时间']
        # df[u'成交日期']=pd.to_datetime(df[u'xxxx'],format='%Y%m%d %H:%M:%S')
        df[u'成交日期'] = map(lambda x: datetime.datetime.strptime(
            str(x), "%Y%m%d"), df[u'成交日期'])
        df = df[df[u'摘要'] != u'申购配号']
        df = df[df[u'摘要'] != u'质押回购拆出']
        df = df[df[u'摘要'] != u'拆出质押购回']
        # print(df.info())
        # print(df)
        # print(df['2017-01'])
        del df[u'合同编号']
        del df[u'备注']
        del df[u'股东帐户']
        del df[u'结算汇率']

        del df[u'Unnamed: 16']
        df = df.sort_values(by=u'成交日期')
        df = df.set_index(u'成交日期')

        df.to_sql('tb_delivery_HT', engine, if_exists='append')
        # df=df[(df[u'摘要']==u'证券卖出') | (df[u'摘要']==u'证券买入')]
        # df= df.groupby(df[u'证券名称'])
        # print(df.describe())
        # print(df[u'手续费'].sum())
        # print(df[u'印花税'].sum())
        # df1=df[[u'证券名称',u'证券代码',u'成交数量',	u'成交均价'	,u'成交金额',u'手续费',	u'印花税',u'发生金额',u'操作']]
        # print(df1[u'证券名称'].value_counts())
        # print(df.groupby(by=[u'证券名称'])[u'发生金额'].sum())
        # df1.to_excel('2017-all.xls')
        # print(df1.groupby(df1[u'证券名称']).describe())
        # print(df1['2017-02'])
        # df.to_excel('2016_delivery_order.xls')
        # self.caculation(df)
        # plt.plot(j,result)
        # plt.show()

    def caculation(self, df):
        fee = df[u'手续费'].sum() + df[u'印花税'].sum() + df[u'其他杂费'].sum()
        print(fee)

    # 计算每个月的费用

    def month(self):
        pass

    # 国金账户 2018-01 到 11月数据入库， 这个函数不用动了。保留csv格式
    def years_gj(self):
        df_list = []
        k = [str(i) for i in range(1, 13)]
        j = [i for i in range(1, 13)]
        result = []
        for i in range(2, 12):
            # filename='GJ_2018_0{}.csv'.format(i)
            # filename = 'GJ_2018_04.csv'
            filename = 'GJ_2018_%s.csv' % str(i).zfill(2)
            # filename='GJ_2018_%s.xls' %str(i).zfill(2)
            print(filename)
            try:
                # t=pd.read_table(filename,encoding='gbk',dtype={u'证券代码':np.str})
                t = pd.read_csv(filename, encoding='gbk', dtype={u'证券代码': np.str})
                # t = pd.read_excel(filename, encoding='gbk',dtype={u'证券代码': np.str})
            except Exception as e:
                print(e)
                # return
                # continue
            # fee=t[u'手续费'].sum()+t[u'印花税'].sum()+t[u'其他杂费'].sum()
            df_list.append(t)
            # result.append(fee)
        df = pd.concat(df_list)
        df = df.reset_index(drop='True')

        # df[u'成交时间'] = df[u'成交时间'].map(lambda x: x.zfill(8))
        df[u'成交日期'] = df[u'成交日期'].astype(np.str) + df[u'成交时间']
        # for i in df[u'成交日期'].values:
        #     try:
        #         x = datetime.datetime.strptime(
        #             i, "%Y%m%d%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        #     except Exception as e:
        #         print(e)
        df['成交日期'] = df['成交日期'].map(lambda x: datetime.datetime.strptime(
            x, "%Y%m%d%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S'))
        try:

            df['成交日期'] = pd.to_datetime(df['成交日期'])
        except Exception as e:
            print(e)
        # df=df[df[u'摘要']!=u'申购配号']
        # df=df[df[u'摘要']!=u'质押回购拆出']
        # df=df[df[u'摘要']!=u'拆出质押购回']
        # print(df.info())
        # print(df)
        # print(df['2017-01'])
        # del df[u'合同编号']
        # del df[u'备注']

        del df['股东帐户']
        del df['成交时间']

        # del df[u'结算汇率']
        # del df[u'Unnamed: 17']

        df = df.sort_values(by='成交日期', ascending=False)
        df = df.set_index('成交日期')
        # print(df.info())
        # print(df)
        #
        df.to_sql('tb_delivery_gj', engine, if_exists='replace')
        # df=df[(df[u'摘要']==u'证券卖出') | (df[u'摘要']==u'证券买入')]
        # df= df.groupby(df[u'证券名称'])
        # print(df.describe())
        # print(df[u'手续费'].sum())
        # print(df[u'印花税'].sum())
        # df1=df[[u'证券名称',u'证券代码',u'成交数量',	u'成交均价'	,u'成交金额',u'手续费',	u'印花税',u'发生金额',u'操作']]
        # print(df1[u'证券名称'].value_counts())
        # print(df.groupby(by=[u'证券名称'])[u'发生金额'].sum())
        # df1.to_excel('2017-all.xls')
        # print(df1.groupby(df1[u'证券名称']).describe())
        # print(df1['2017-02'])
        # df.to_excel('2016_delivery_order.xls')
        # self.caculation(df)
        # plt.plot(j,result)
        # plt.show()
        #

    # 单独处理某个文件（单独一个月的数据） 文件格式：国金-保存为xls，然后另存为csv 或者按照天也可以
    def years_gj_each_month_day(self):
        filename = '2019-02-11_02-12.csv'
        try:
            # 根据不同的格式选用不同的函数
            # t=pd.read_table(filename,encoding='gbk',dtype={u'证券代码':np.str})
            t = pd.read_csv(filename, encoding='gbk', dtype={'证券代码': np.str})
            # t = pd.read_excel(filename, encoding='gbk',dtype={u'证券代码': np.str})
        except Exception as e:
            print(e)
            # continue
        # fee=t[u'手续费'].sum()+t[u'印花税'].sum()+t[u'其他杂费'].sum()
        else:
            # df_list.append(t)
            # result.append(fee)
            df = t
        # df = pd.concat(df_list)
        df = df.reset_index(drop='True')

        # df[u'成交时间'] = df[u'成交时间'].map(lambda x: x.zfill(8))
        df[u'成交日期'] = df[u'成交日期'].astype(np.str) + df[u'成交时间']
        # for i in df[u'成交日期'].values:
        #     try:
        #         x = datetime.datetime.strptime(
        #             i, "%Y%m%d%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        #     except Exception as e:
        #         print(e)
        df['成交日期'] = df['成交日期'].map(lambda x: datetime.datetime.strptime(
            x, "%Y%m%d%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S'))
        try:

            df['成交日期'] = pd.to_datetime(df['成交日期'])
        except Exception as e:
            print(e)
        # df=df[df[u'摘要']!=u'申购配号']
        # df=df[df[u'摘要']!=u'质押回购拆出']
        # df=df[df[u'摘要']!=u'拆出质押购回']
        # print(df.info())
        # print(df)
        # print(df['2017-01'])
        # del df[u'合同编号']
        # del df[u'备注']

        del df['股东帐户']
        del df['成交时间']

        # del df[u'结算汇率']
        # del df[u'Unnamed: 17']

        df = df.sort_values(by='成交日期', ascending=False)
        conn = get_mysql_conn('db_stock', 'local')
        cursor = conn.cursor()
        insert_cmd = '''
        insert into tb_delivery_gj_django (成交日期,证券代码,证券名称,操作,成交数量,成交均价,成交金额,余额,发生金额,手续费,印花税,过户费,本次金额,其他费用,交易市场) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        check_dup = '''
        select * from tb_delivery_gj_django where 成交日期=%s and 证券代码=%s and 操作=%s and 成交数量=%s and 余额=%s
        '''
        for index, row in df.iterrows():
            date=row['成交日期']
            date=date.to_pydatetime()
            # print(type(date))

            # print(date)
            cursor.execute(check_dup, (date, row['证券代码'], row['操作'], row['成交数量'], row['余额']))
            if cursor.fetchall():
                print('有重复数据，忽略')

            else:
                cursor.execute(insert_cmd, (
                    date, row['证券代码'], row['证券名称'], row['操作'], row['成交数量'], row['成交均价'], row['成交金额'], row['余额'],
                    row['发生金额'], row['手续费'], row['印花税'], row['过户费'], row['本次金额'], row['其他费用'], row['交易市场']))

        conn.commit()
        conn.close()
        # df.to_sql('tb_delivery_gj', engine, if_exists='append')
        # df=df[(df[u'摘要']==u'证券卖出') | (df[u'摘要']==u'证券买入')]
        # df= df.groupby(df[u'证券名称'])
        # print(df.describe())
        # print(df[u'手续费'].sum())
        # print(df[u'印花税'].sum())
        # df1=df[[u'证券名称',u'证券代码',u'成交数量',	u'成交均价'	,u'成交金额',u'手续费',	u'印花税',u'发生金额',u'操作']]
        # print(df1[u'证券名称'].value_counts())
        # print(df.groupby(by=[u'证券名称'])[u'发生金额'].sum())
        # df1.to_excel('2017-all.xls')
        # print(df1.groupby(df1[u'证券名称']).describe())
        # print(df1['2017-02'])
        # df.to_excel('2016_delivery_order.xls')
        # self.caculation(df)
        # plt.plot(j,result)
        # plt.show()

    def pretty(self):
        df = pd.read_sql('tb_delivery_GJ', engine, index_col=u'成交日期')
        # print(df)
        # del df[u'Unnamed: 17']
        del df['index']
        df.to_sql('tb_delivery_GJ', engine, if_exists='replace')

    # 数据同步到另一个django数据库
    def data_sync(self):
        conn = get_mysql_conn('db_stock', 'local')
        cursor = conn.cursor()
        # 最新的数据库
        select_cmd = '''select * from tb_delivery_gj'''
        cursor.execute(select_cmd)
        ret = list(cursor.fetchall())
        print('new db ', len(ret))
        # 旧的数据库
        select_cmd2 = '''select * from tb_delivery_gj_django'''
        cursor.execute(select_cmd2)
        ret2 = list(cursor.fetchall())
        print('old db ', len(ret2))
        ret_copy = ret.copy()

        for item in ret:
            # print(item)
            for item2 in ret2:
                if item[0] == item2[0] and item[1] == item2[1] and item[2] == item2[2] and item[4] == item2[4] and item[
                    5] == item2[5]:
                    try:
                        ret_copy.remove(item)
                    except Exception as e:
                        # print(e)
                        # print()
                        pass

        # print(ret_copy)
        for i in ret_copy:
            # print(i)
            update_sql = '''
            insert into tb_delivery_gj_django (成交日期,证券代码,证券名称,操作,成交数量,成交均价,成交金额,)
            '''

        print('diff len ', len(ret_copy))


# 银转证
def bank_account():
    folder_path = os.path.join(os.path.dirname(__file__), 'private')
    os.chdir(folder_path)

    df_list = []
    for file in os.listdir(folder_path):
        if re.search('2', file.decode('gbk')):
            df = pd.read_table(file, encoding='gbk')
            # df[df['']]
            # print(df)
            # df_list.append(df[[u'日期',u'操作',u'发生金额']])
            df_list.append(df)
    total_df = pd.concat(df_list)
    # total_df=total_df.reset_index()
    # del total_df[u'level_0']
    del total_df[u'货币单位']
    del total_df[u'合同编号']
    del total_df[u'Unnamed: 8']
    del total_df[u'银行名称']
    # print(total_df)
    # f=total_df[total_df[u'操作']==u'证券转银行'][u'发生金额']*-1
    total_df[u'发生金额'] = map(lambda x, y: x * -1 if y ==
                                                   u'证券转银行' else x, total_df[u'发生金额'], total_df[u'操作'])
    # print(total_df.columns)
    # print(total_df5)
    # total_df=total_df.reset_index()
    # total_df=total_df.set_index('index')
    # total_df=total_df.reset_index(drop=True)
    total_df[u'委托时间'] = map(lambda x: str(x).zfill(6), total_df[u'委托时间'])

    total_df[u'日期'] = map(lambda x, y: str(x) + " " + y,
                          total_df[u'日期'], total_df[u'委托时间'])
    total_df[u'日期'] = pd.to_datetime(total_df[u'日期'], format='%Y%m%d %H%M%S')
    total_df = total_df.set_index(u'日期')

    df = total_df[total_df[u'备注'] == u'成功[[0000]交易成功]']
    # print(df)
    # print(total_df.iloc[131])
    # print(total_df[u'备注'].values)
    print(df[u'发生金额'].sum())
    # df.dropna('')
    del df[u'备注']
    del df[u'委托时间']
    df.to_sql('tb_bank_cash', engine, if_exists='replace')
    # print(df['2018'])


def main():
    obj = Delivery_Order()
    # obj.data_sync()
    obj.years_gj_each_month_day()
    # obj.years_gj_each_month()
    # obj.years_gj()
    # obj.years_ht()
    # bank_account()
    # obj.pretty()


if __name__ == '__main__':
    main()
