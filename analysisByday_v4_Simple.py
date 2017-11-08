#-*- coding: utf-8 -*-
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandas.tseries.offsets import Day, MonthEnd, Minute, Hour
from pylab import polyfit

pd.set_option('display.unicode.east_asian_width',True) #한국어 있으면 column 맞춰서 정렬
pd.set_option("display.float_format", '{0:,.0f}'.format)
pd.set_option('display.width', 1000) #열들이 넓게 프린트 될수 있게함 
#pd.set_option('display.max_rows', 500)

"""
u'\uccb4\ud06c\uce74\ub4dc' 체크카드
u'\ub300\uccb4' 대체, u'\ud604\uae08' 현금
u'\uc0c1\ud638\ubd80\uae08' 상호부금
u'\ud0c0\ud589\uc774\uccb4' 타행이체
u'\ub2f9\ud589\uc1a1\uae08' 당행송금
u'\uc608\uae08\uc774\uc790' 예금이자
u'\ud0c0\ud589\uc1a1\uae08' 타행송금
u'\ud558\ub098\uce74\ub4dc' 하나카드
u'\uccb4\ud06c\ud1b5\uc2e0' 체크통신
u'\uae30\ud0c0' 기타
"""
data = pd.read_csv(r"C:\Users\Home\Desktop\myAccount\data.csv", encoding="euc-kr")
data.date= pd.to_datetime(data.date)

def unique_count(series):
    e = series.groupby(series.values).value_counts()
    unique_counts = Series(e.values,e.index.get_level_values(0))
    unique_counts.sort_values(inplace=True)
    return unique_counts

def mergeDateWithTime(dateSeries,timeSeries):
    "date in Timestamp ####-##-##, time in ##-##"
    templist= []
    for i in range(len(dateSeries)):
        temp = timeSeries[i].split(":")
        time = dateSeries[i] + Hour(temp[0])+Minute(temp[1])
        templist.append(time)
    return Series(templist)

def pt(data,type1):
    "Print by Type"
    print data[data.type==type1]



data2 = data.iloc[:,[0,1,2,3,4]]

df= data2[data2["type"] == u'\uccb4\ud06c\uce74\ub4dc'] #체크카드
#withdrawalCheck = withdrawalCheck[withdrawalCheck["withdrawal"] !=0]
#pt(data,u'\uccb4\ud06c\uce74\ub4dc')

days = {0:'MON',1:'TUE',2:'WED',3:'THU',4:'FRI',5:'SAT',6:'SUN'}
df['day_of_week'] = df['date'].dt.dayofweek
df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])
df2 = df.iloc[:,[4,5]]
df2 = df2.sort_values(by='day_of_week')
df2 = df2[df2.withdrawal<=20000]
df2.to_csv(r"C:\Users\Home\Desktop\myAccount\day_analysis_v2.csv", encoding="euc-kr")

df['hour'] = df['date'].apply(lambda x: x.hour)
df3 = df.iloc[:,[4,6]]
df3 = df3[df3.withdrawal<=20000]
df3.to_csv(r"C:\Users\Home\Desktop\myAccount\hour_analysis_v2.csv", encoding="euc-kr")

df4 = df.iloc[:,[0,4]]
df4 = df4[df4.withdrawal<=20000]
df4.to_csv(r"C:\Users\Home\Desktop\myAccount\time_analysis_v2.csv", encoding="euc-kr")


