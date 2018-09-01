"""
股票市值--低价-策略选股，最小市值的(k1,k2)倍之间的股票列表
建议每天收盘后分析
@author: 488361685@qq.com
"""
import tushare as ts
import pandas as data_f
import datetime
import csv

today=datetime.date.today()

filename="e:\\test\\自选股数据\\当天所有数据%s.csv" % (today)
### 写入当前全部数据write csv file
data_f01=ts.get_today_all()
data_f01.to_csv(filename,sep=',')

# 找到市盈率per>0的最小流通市值nmc--默认单位：万元
nmc_min=200000
code_min=0
nmc_max=200000
code_max=0
for index, row in data_f01.iterrows():
    if row['nmc'] < 10:
        continue;
    elif (600000 <= int(row['code']) <= 603999) or (300001 <= int(row['code']) <= 300999) or (1 <= int(row['code']) <= 2999) :
        if (row['nmc'] < nmc_min) and (row['per']>0):
            nmc_min=row['nmc']
            code_min=row['code']
        elif (row['nmc']>nmc_max):
            nmc_max=row['nmc']
            code_max=row['code']
        else:
            continue;
    else:
        continue;    
nmc_min_yi=nmc_min/10000 # 单位--万元-->亿元
nmc_max_yi=nmc_max/10000
print('\n最小市值股票代码为(%s)' % code_min, '最小市值为(%.2f)亿元' % nmc_min_yi)
print('最大市值股票代码为(%s)' % code_max, '最大市值为(%.2f)亿元' % nmc_max_yi)

# 筛选最小流通市值k1-k2倍之间、低价（<20元）沪深A股股票(600,601,603,300,000,001,002)    
k1=1.2 # 最小市值倍率底部
k2=20 # 最小市值倍率顶部
k3=20 # 股价＜20元
csv_file=open(filename)
csv_lines=csv.reader(csv_file) #逐行读取csv数据
data_small=[] #创建列表准备接收csv各行数据
num_small=0
num_big=0
num_turnover=0
for one_line in csv_lines:
    if one_line[15] == str('nmc'):
        data_small.append(one_line) # 逐行写入新列表--参数说明行
    elif (600000 <= int(row['code']) <= 603999) or (300001 <= int(row['code']) <= 300999) or (1 <= int(row['code']) <= 2999) :
        if (k1*nmc_min) < float(one_line[15]) < (k2*nmc_min) and (1 < float(one_line[12]) < 50) :  # 小市值、正-低市盈率
            if (1 < float(one_line[4]) < 20) and ((7 < float(one_line[10]) < 20)):  # 低价1-20元，换手率7-20
                data_small.append(one_line) # 逐行写入新列表
                num_small=num_small+1
            else:
                num_turnover=num_turnover+1
                pass
        else:
            num_big=num_big+1
            continue;
    else:
        continue;
print('\n筛选后的小市值股票数量为(%s)个' % num_small, '筛选后的剩余股票数量为(%s)个' % num_big)
print('换手率不合适股票数量为(%s)个',num_turnover)
# 写入小市值csv表格
filename_small="e:\\test\\自选股数据\\当天所有数据-市值per-%s.csv" % (today)
data_small01=data_f.DataFrame(data_small)
data_small01.to_csv(filename_small,sep=',')

