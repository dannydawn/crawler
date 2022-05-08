from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver import Edge
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import csv
#import concurrent.futures
import numpy as np
import pandas as pd

# 讀取 uid 和 song 的 df2_pre
data = np.array( pd.read_csv('df3-2_pre.csv', header=None))[1:]
#print(data[0][1])

def informCrawler(uid, song, writer):
    url = "https://streetvoice.com/" + uid + "/songs/" + song
    #print(url)
    # 設定不顯示視窗
    chrome_options = Options()
    
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=chrome_options)
    #driver.implicitly_wait(10) 
    driver.maximize_window()
    driver.set_page_load_timeout(600)
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()
    # 如果樂曲還存在就爬取資訊
    if soup.find(class_ = "list-inline list-item-buttons align-items-center justify-content-end"):
        playcount = soup.find(id="countup-play").getText()
        #print(playcount)
        playcount = playcount.replace(',', '')
        likecount = soup.find(id="countup-like").getText()
        likecount = likecount.replace(',', '')
        sharecount = soup.find(class_="mb-0 text-center js-share-count")['data-share-count']
        temp = soup.find(class_="text-truncate text-white opacity-72")
        catagory = temp.find(href = True).getText()
        publishtime = soup.find(class_="text-gray-light mb-2").getText()[-10:]
        #print(likecount)
        #print(sharecount)
        writer.writerow([uid, song, playcount, likecount, sharecount, catagory, publishtime])
'''
Uid = []
Song = []
Playcount = []
Likecount = []
Sharecount = []
Catagory = []
PublishTime = []
'''

data_01 = data[0:400]
data_02 = data[400:800]
data_03 = data[800:1200]
data_04 = data[1200:1600]
data_05 = data[1600:2000]
data_06 = data[2000:2400]
data_07 = data[2400:2800]
data_08 = data[2800:3200]
data_09 = data[3200:3600]
data_10 = data[3600:4000]
data_11 = data[4000:4400]
data_12 = data[4400:4800]
data_13 = data[4800:5200]
data_14 = data[5200:5600]
data_15 = data[5600:6000]
data_16 = data[6000:6400]
data_17 = data[6400:]

with open('df3-2_1.csv', 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    # 如果發生 Exception，會 print 出當前執行的 index (count)
    count = 0
    for d in data_01[0:]:
        try:
            informCrawler(d[0], d[1], writer)
            count += 1
        except:
            print(count)
            time.sleep(30)
            informCrawler(d[0], d[1], writer)
            count += 1


'''
def scrape(count, data):
    path = "df2_" + str(count) + ".csv"
    for d in data:
        try:
            informCrawler(d[0], d[1])
            #count += 1
        except:
            print(count)
            df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                    columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
            df2.to_csv(path, index=False)  
            time.sleep(30)
            informCrawler(d[0], d[1])
            #count += 1
      
    df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                    columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
    df2.to_csv(path, index=False)  


data_for_multi = [(4000, data_05), 
                  (5000, data_06),
                  (6000, data_07),
                  (7000, data_08),
                  (8000, data_09),
                  (9000, data_10),
                  (10000, data_11),
                  (11000, data_12),]
with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor:
    executor.map(scrape, data_for_multi)
'''