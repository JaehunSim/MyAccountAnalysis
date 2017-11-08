import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt

AugustAccount = pd.read_csv(r"C:\Users\Home\Desktop\myAccount\data.csv", encoding="euc-kr")
AugustAccount.date= pd.to_datetime(AugustAccount.date)

data = AugustAccount.iloc[:,[0,4,6]]
"groupby date"
data2 = data.groupby("date", as_index=False).sum()
data2 = data2[data2.withdrawal<200000]
data2ByWeek = data2.groupby(pd.PeriodIndex(data2.date, freq="m")).sum()
#data2ByWeek.to_csv(r"C:\Users\Home\Desktop\myAccount\dataByWeek.csv")

data3 =data2.withdrawal[data2.withdrawal<200000]
data3 = DataFrame(data3)
data3["date"] = data2.date[data3.index]
data3ByWeek = data3.groupby(pd.PeriodIndex(data3.date, freq="w")).sum()
#data3ByWeek.to_csv(r"C:\Users\Home\Desktop\myAccount\data3ByWeek.csv")

data2ByWeek.plot()
plt.show()
