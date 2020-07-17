# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:17:31 2020

@author: seko
"""

import pandas as pd
import datetime

def get_startdate(row):
    a = '0000' + str(row['測定投入時間'])
    mydate = row['測定投入日']
    mystr = str(mydate) + a[-4:]
    return pd.to_datetime(mystr,format='%Y%m%d%H%M')

def get_compdate(row):
    a = '0000' + str(row['測定完了時間'])
    mydate = row['測定完了日']
    mystr = str(mydate) + a[-4:]
    return pd.to_datetime(mystr,format='%Y%m%d%H%M')


def split_datetime(order_no,start_date,comp_date):
    range_date = comp_date - start_date
    lst = []
    for i in range(range_date.days + 2):
        from_date = start_date.replace(hour=0,minute=0) + datetime.timedelta(days=i)
        to_date = start_date.replace(hour=0,minute=0) + datetime.timedelta(days=i + 1)
        if start_date > from_date:
            from_date = start_date
        if comp_date < to_date:
            to_date = comp_date
        if from_date < to_date:
            lst.append({'オーダー№':order_no,'from_date':from_date,'to_date':to_date})
        #print(from_date,to_date,to_date-from_date)
    return lst




df = pd.read_csv('sample_data.txt',delimiter=' ')
df['startdate'] = df.apply(get_startdate,axis=1)
df['compdate'] = df.apply(get_compdate,axis=1)


lst =[]
for index, row in df.iterrows():
    order_no, start_date, comp_date = row['オーダー№'],row['startdate'],row['compdate']
    mydic = split_datetime(order_no,start_date,comp_date)
    print(order_no, start_date, comp_date)
    print(mydic)
    #lst = lst + split_datetime(order_no,start_date,comp_date)

order_no = '10FVE20100'
start_date = datetime.datetime(2020,6,28,21,18)
comp_date = datetime.datetime(2020,6,29,12,29)
a=split_datetime(order_no,start_date,comp_date)
