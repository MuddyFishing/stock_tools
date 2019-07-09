# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
'''
记录每天的盈亏情况 完成度100%
'''
import pandas as pd
import os
import tushare as ts
import datetime

def getCodeFromExcel(filename):
    #从excel表中获取代码, 并且补充前面几位000
    #获取股票数目
    df=pd.read_excel(filename)
    code_list = df['证券代码'].values
    quantity_list=df['股票余额'].values
    code=[]
    quantity=[]
    for i in range(len(code_list)):
        code.append(str(code_list[i]).zfill(6))
        #后面学会了map函数，可以直接搞定
        quantity.append(quantity_list[i])

    return code,quantity

def calc(code):
    settlement =  df[df['code']==code]['settlement'].values
    percentage =  df[df['code']==code]['changepercent'].values
    trade =  df[df['code']==code]['trade'].values
    #print(percentage)
    #settlement=df[df['code'==code]]['settlement'].values
    #percentage=df[df['code'==code].index]['changepercent'].values
    #返回四舍五入的结果
    return settlement,percentage,trade


def today_win_lost(filename_path):
    filename=os.path.join(filename_path,'ownstock.xls')
    code,quantity=getCodeFromExcel(filename)
    result=[]
    percentage_list=[]
    trade_list=[]
    for i in range(len(code)):
        settlement,percentage,trade=calc(code[i])
        print("settlement", settlement)
        print("percent", percentage)
        print("trade", trade)
        profit=round(settlement[0]*percentage[0]*quantity[i]*0.01,1)
        result.append(profit)
        percentage_list.append(percentage[0])
        trade_list.append(trade[0])

    return result,code,percentage_list,trade_list

def join_dataframe(filename,today):
    current_profile=today+'当天贡献'
    result,code,percentage_list,trade_list=today_win_lost()
    s1=pd.DataFrame({current_profile:result})
    #s2=pd.DataFrame({'当天涨幅':percentage_list})
    #s3=pd.DataFrame({'当天价钱':trade_list})
    #print(s)
    df=pd.read_excel(filename)
    #del df['交易市场']
    #del df['股东帐户']
    #del df['盈亏比(%)']
    #del df['在途数量']
    #del df['当天贡献']
    #del df['']
    #del df['']
    df['证券代码']=code
    #print(code)
    df['市价']=trade_list
    df['当天涨幅']=percentage_list
    #可以这样直接替换某一列的值
    #df=df.join(s2,how='right')
    df=df.join(s1,how='right')
    #df=df.join(s3,how='right')
    return df


def main(today):
    path=os.path.join(os.path.dirname(__file__),'data')
    filename=os.path.join(path,'each_day_profile.xls')
    org_filename=os.path.join(path,'2016-09-30_all_.xls')
    #df_filename=os.path.join(path,'each_day_profile.xls')
    #df=pd.read_excel(org_filename)
    df=ts.get_today_all()
    new_df=join_dataframe(filename,today)
    save_name=os.path.join(path,"each_day_profile.xls")
    #这样会不会把原来的覆盖掉？
    new_df.to_excel(save_name)


if __name__ == "__main__":
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    if not ts.is_holiday(today):
        main(today)