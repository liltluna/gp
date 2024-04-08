import tushare as ts
import pandas as pd
import shutil
import os


start_year = 2009
gap_year = 9  # 9年作为训练，之后一年用来测试， 2009-2018 2019
pro = pro = ts.pro_api(
    '19c1ab37c30ca784d8658cf1050c0aba8eef6cb8d7cda5d0744d6bfb')
columns_to_drop = ['ts_code', 'change', 'pct_chg', 'amount']  # 删除指定的列

if not os.path.exists('dataset'):
    os.mkdir('dataset')
else:
    shutil.rmtree('dataset')
    os.mkdir('dataset')

df = pro.daily(ts_code='000001.SZ', start_date='20090101', end_date='20240101')
df.drop(columns=columns_to_drop, inplace=True)
df['trade_date'] = pd.to_datetime(df["trade_date"], format="%Y%m%d")
df_reversed = df[::-1]
df_reversed.to_csv('./dataset/reversed_all_data.csv',
                   index=False, header=False)  # index=False 防止保存索引列


for i in range(4):  # 切割训练预测数据
    dir = './dataset/set-{}'.format(i)
    os.mkdir(dir)
    start_date = '{}-01-01'.format(start_year + i)
    end_date = '{}-01-01'.format(start_year + i + gap_year)
    test_start_date = end_date
    test_end_date = '{}-01-01'.format(start_year + i + gap_year + 1)

    selected_data = df[(df['trade_date'] >= pd.to_datetime(start_date)) & (
        df['trade_date'] <= pd.to_datetime(end_date))]
    reversed_selected_data = selected_data[::-1]

    test_selected_data = df[(df['trade_date'] >= pd.to_datetime(test_start_date)) & (
        df['trade_date'] <= pd.to_datetime(test_end_date))]
    test_reversed_selected_data = test_selected_data[::-1]

    reversed_selected_data.to_csv(
        dir + '/reversed_train_data.csv', index=False, header=False)
    test_reversed_selected_data.to_csv(
        dir + '/reversed_test_data.csv', index=False, header=False)  # index=False 防止保存索引列
    print('sd:{}, ed:{}, tsd:{}, ted:{}'.format(
        start_date, end_date, test_start_date, test_end_date))
    print('save {}...'.format(dir))
