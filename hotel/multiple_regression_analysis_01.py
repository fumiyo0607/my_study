import sys
sys.path.append('/Users/fumiyo_ito/Documents/git/my_study/hotel')
import functions
import pandas as pd

'''
column名：
'hostel.name', 'City', 'price.from', 'Distance','summary.score', 'rating.band', 'atmosphere', 'cleanliness',
'facilities', 'location.y', 'security', 'staff', 'valueformoney', 'lon','lat'
'''

# 'City', 'price.from', 'atmosphere', 'cleanliness', 'facilities', 'location.y', 'security', 'staff', 'valueformoney' を使用して予測
# モデルには重回帰分析を使用
df = pd.read_csv('Hostel.csv')

# 欠損値を含む列を削除
df.dropna()

# 説明変数
x = df[['City', 'price.from', 'atmosphere', 'cleanliness', 'facilities', 'location.y', 'security', 'staff', 'valueformoney']]
x = pd.get_dummies(x)

# 目的変数
y = df['summary.score']

result = functions.multiple_regression_analysis(x, y)

# 結果を表示
result.summary()