# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:07:58 2018

@author: Allwell997
"""

import numpy as np
import pandas as pd


import requests


#调用新浪api
def get_current_price(stock,stock_name):
    if stock.startswith('6') or stock=='000001':
        url = 'http://hq.sinajs.cn/?format=json&list=sh' + str(stock)
    else:
        url = 'http://hq.sinajs.cn/?format=json&list=sz' + str(stock)
    content=requests.get(url).text
    price_list = content.split(',')
    current_price = eval(price_list[3])
    open_price = eval(price_list[2])
    raise_persent = (current_price-open_price)/open_price * 100
    if raise_persent>=0:
        print('%s price:%.2f  raise:\033[1;31m %.2f%% \033[0m !'%(stock_name,current_price,raise_persent))
    else:
        print('%s price:%.2f  raise:\033[1;32m %.2f%% \033[0m !'%(stock_name,current_price,raise_persent))       
    return current_price,raise_persent,price_list

def get_currency_rmb():
    url = 'http://hq.sinajs.cn/?format=json&list=fx_susdcny'
    content = requests.get(url).text
    currency_list = content.split(',')
    real_currency = eval(currency_list[2])
    yesterday_close = eval(currency_list[3])
    currency_gap = (real_currency - yesterday_close) * 10000
    if currency_gap >=0:
        print('USD:RMB%.4f   raise:\033[1;31m %d \033[0m !'%(real_currency,currency_gap))
    else:
         print('USD:RMB%.4f   raise:\033[1;32m %d \033[0m !'%(real_currency,currency_gap))
    
    return currency_list[2]

get_currency_rmb()
shanghai = get_current_price('000001','shanghai')

tcl = get_current_price('000100','tcl')


