import os
import glob
from numpy import NAN, nan
import pandas as pd
import langid

# 1. 先把空字串、google翻譯字串清除
# 2. 合併成一個檔案
# 3. 建立斷句標準
# 4. 太長或太短的就刪除

# for file in glob.glob(r"data\raw_data\*.csv"):

with open(r"data\raw_data\3皇3家文化店__reviews_.csv", 'r', encoding='utf-8') as file:
    data = pd.read_csv(file)


# 刪除空字串
data = data.dropna()
# 刪除其他語言
index_c = 0
for i in data['caption']:
    if(type(i) == str):
        if("由 Google 提供翻譯" in i):
            data = data.drop(index=int(index_c))
    index_c += 1
data.reset_index(inplace=True, drop=True)
print(data)
