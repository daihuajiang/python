import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#設定一組資料id:1~5,共11個欄位a~k
data = {'id':[1,2,3,4,5],
        'a':[1,1,0,0,0],
        'b':[1,1,0,0,1],
        'c':[1,1,1,1,0],
        'd':[0,1,1,0,0],
        'e':[1,1,0,0,1],
        'f':[1,1,1,1,1],
        'g':[0,1,1,1,0],
        'h':[0,0,0,1,1],
        'i':[0,0,0,1,0],
        'j':[1,1,0,0,1],
        'k':[0,0,0,1,0]}

#將data轉換成dataframe
df = pd.DataFrame(data)
df = df[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']]
print("df=")
print(df)
#使用apriori找出哪些項目常一起出現，最小支持度0.5
frequent_itemsets = apriori(df[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']], min_support =0.50, use_colnames=True)
print("========================")
print("frequent_itemsets=")
print(frequent_itemsets)
#找出規則
# min_threshlod = 1 最小的lift值須等於1 不然沒有意義
rules = association_rules(frequent_itemsets, metric = 'lift', min_threshold=1)
print("========================")
print("rules=")
print(rules)