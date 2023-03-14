import time
import random
import requests
from bs4 import BeautifulSoup
import json
import csv

#使用者資訊
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Mobile Safari/537.36',
}

#爬取新聞列表
def get_news_list(page_num=3):
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        #挑選網站即時-不分類頁面為爬蟲目標
        channelId = 1
        cate_id = 99
        type_ = 'breaknews'
        query = f"page={page+1}&channelId={channelId}&cate_id={cate_id}&type={type_}"
        news_list_url = base_url + '?' + query
        print(news_list_url)
        # https://udn.com/api/more?page=2&channelId=1&cate_id=0&type=breaknews
        
        #向聯合新聞網網站請求頁面資訊(回傳json格式)
        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        news_list.extend(news_data['lists'])

        time.sleep(random.uniform(1, 2))

    return news_list

#取得文章內容
def get_content_from_url(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.select_one('section.article-content__editor')
    return content.find_all("p")

news_list = get_news_list(page_num=2) #爬取2頁新聞

#印出前10篇新聞標題
for i in range(len(news_list)):
    print("%d "%(i)+news_list[i]['title'])

print(f"共抓到 {len(news_list)} 篇新聞")

#對"news_list"附加內文的欄位
for i in range(len(news_list)):
    print("抓取第"+str(i)+"篇內文")
    try:
        url = "https://udn.com"+news_list[i]['titleLink']
        content = get_content_from_url(url)
        news_list[i].update({'content': '%s'%(str(content))})
    except:
        news_list[i].update({'content': '內文獲取失敗'})
        print("get text error.")
        continue

#將爬取到的資訊輸出成csv檔
data_file = open('output.csv', 'w', newline='', encoding='UTF-8')
csv_writer = csv.writer(data_file)

count = 0
for data in news_list:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()