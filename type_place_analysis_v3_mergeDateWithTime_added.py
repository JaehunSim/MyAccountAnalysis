#-*- coding: utf-8 -*-
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandas.tseries.offsets import Day, MonthEnd, Minute, Hour

pd.set_option('display.unicode.east_asian_width',True) #한국어 있으면 column 맞춰서 정렬
pd.set_option("display.float_format", '{0:,.0f}'.format)


"""
u'\uccb4\ud06c\uce74\ub4dc' 체크카드
u'\ub300\uccb4', u'\ud604\uae08' 대체
u'\uc0c1\ud638\ubd80\uae08' 현금
u'\ud0c0\ud589\uc774\uccb4' 상호부금
u'\ub2f9\ud589\uc1a1\uae08' 타행이체
u'\uc608\uae08\uc774\uc790' 당행송금
u'\ud0c0\ud589\uc1a1\uae08' 예금이자
u'\ud558\ub098\uce74\ub4dc' 타행송금
u'\uccb4\ud06c\ud1b5\uc2e0' 하나카드
u'\uae30\ud0c0' 기타
"""
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
    

def is_refund(data): #r=refund dataframe
    "환불은 체크카드로 이루어지는것만 생각하기! 가장 일반적이다."
    "if it's refund row, return both deposit, withdrawal index"
    deposit = data[data["deposit"]!=0] #deposit case
    checkDeposit = deposit[deposit["type"] == u'\uccb4\ud06c\uce74\ub4dc'] #checkCard type of deposit
    temp = data[data["withdrawal"] != 0] #withdrawal case
    checkWithdrawal = temp[temp["type"] == u'\uccb4\ud06c\uce74\ub4dc']
    tempList = []
    #return checkDeposit
    for i in range(len(checkDeposit)):
        data = checkDeposit.iloc[i]
        date = data.date
        #print date
        place = data.place
        value = data.deposit
        temp = checkWithdrawal[checkWithdrawal["date"] <= date]
        temp = temp[temp["date"] >= date-Day(3)]
        #tempList.append(temp)
        temp2 = list(temp.withdrawal)
        if value in temp2:
            WRefundindex = temp.withdrawal.index[temp2.index(value)]
            tempList.append(checkDeposit.index[i])
            tempList.append(WRefundindex)
    return tempList
 
AugustAccount = pd.read_csv(r"C:\Users\Home\Desktop\myAccount\myAccountInCSVv3_201303~201610.csv", encoding="euc-kr")
AugustAccount.date= pd.to_datetime(AugustAccount.date)
datetime = mergeDateWithTime(AugustAccount.date,AugustAccount.trade_time)
AugustAccount.date = datetime
AugustAccount.pop("trade_time")

t = AugustAccount.iloc[:,1] #type
#p = AugustAccount.iloc[:,2] #place
#td = AugustAccount.iloc[:,[0,1,3]] #date,type, deposit
#tw = AugustAccount.iloc[:,[0,1,4]] #date,type, withdrawal
#r = AugustAccount.iloc[:,[0,2,3,4]] #refund 
#tu = t.unique()
#pu = p.unique()

#p[t[t==u'\ub300\uccb4'].index] #대체인 경우

#type unique value count
t_unique_counts = unique_count(t)


#"상호부금 항목" #내 계좌간 거래
tradeBetweenOwnAccount = list(t[t== u'\uc0c1\ud638\ubd80\uae08'].index)


#체크카드 환불된 항
checkRefund = is_refund(AugustAccount)

"2건 제외(체크통신-시험접수환불)"
#체크통신 환불된 항
checkCommunicationRefund = [652,653]

totalDeleteIndex = []
for i in tradeBetweenOwnAccount:
    totalDeleteIndex.append(i)
for i in checkRefund:
    totalDeleteIndex.append(i)
for i in checkCommunicationRefund:
    totalDeleteIndex.append(i)

data = AugustAccount.drop(totalDeleteIndex) #Refund dropped
data.index = pd.Index(range(len(data)))

data.to_csv(r"C:\Users\Home\Desktop\myAccount\DatetimeRefundDeleted_v2.csv",encoding='euc-kr', index=None)

