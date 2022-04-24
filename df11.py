import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import csv
import numpy as np
import pandas as pd

# data 讀檔
d9 = pd.read_csv('df9-count.csv', header=None)
data = d9[0].values.tolist()

def LikesCrawler(uid, writer):
    url = "https://streetvoice.com" + uid + "likes"
    #print(url)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=chrome_options)
    driver.maximize_window()
    driver.set_page_load_timeout(600)
    driver.get(url)

    try:
        element = driver.find_element_by_id('js-loader') #按下點我看更多按鈕
        element.click()
    except:
        pass

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()

    ele = soup.find_all(class_ = "col-6 col-sm-4 col-md-3 item_box")

    for box in ele:
        a = box.find("a", href = True)
        if a:
            temp = a['href']
            inf = temp.split('/')
            #print(inf)
            writer.writerow([uid[1:-1], inf[3], inf[1]])
'''           
def CollabCrawler(uid):
    url = "https://streetvoice.com" + uid + "songs"
    #print(url)
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html5lib')
    
    collabList = soup.find(id = "item_box_list_wrapper_2")
    if collabList:
        print("Has Collab")
        #collabList = collabList.find(id="item_box_list")
        ele = collabList.find_all(class_ = "work-item mb-5")
        #print(ele)

        for box in ele:
            a = box.find("a", href = True)
            if a:
                temp = a['href']
                inf = temp.split('/')
                #print(inf)
                Uid.append(uid[1:-1])
                Song.append(inf[3])
                CollabUid.append(inf[1])
    else:
        print("No Collab")
        pass

Uid = []
Song = []
ArtistUid = []
CollabUid = []
'''
# 如果發生 Exception，shell 將會 print 出當前執行的 index 
# 若程式因 Exception 停止，請執行以下步驟：
# 1. 把 count 和 data[<count>:] 的數值改成 index
# 2. 把 df11.csv 的內容存到另一個 csv 檔中
# 3. 再次啟動程式
data_01 = data[0:400]
data_02 = data[400:800]
data_03 = data[800:1200]
data_04 = data[1200:1600]
data_05 = data[1600:2000]
data_06 = data[2000:2400]
data_07 = data[2400:2800]
data_08 = data[2800:3200]
data_09 = data[3200:3600]
data_10 = data[3600:]

with open('df11_8.csv', 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    # 如果發生 Exception，會 print 出當前執行的 index (count)
    count = 0
    for d in data_08:
        try:
            LikesCrawler(d, writer)
            count += 1
        except:
            print(count)
            time.sleep(30)
            LikesCrawler(d, writer)
            count += 1
  