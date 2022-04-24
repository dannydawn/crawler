import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import numpy as np
import pandas as pd

# data 讀檔
d1 = np.array( pd.read_csv('R&B_靈魂_藍調_爵士_拉丁.csv', header=None).transpose() )[0]
d2 = np.array( pd.read_csv('舞曲_Remix_ACG_電音.csv', header=None).transpose() )[0]
d3 = np.array( pd.read_csv('嘻哈_饒舌_雷鬼_Funk.csv', header=None).transpose() )[0]

data = np.concatenate((d1, d2, d3))
data = np.unique(data)

def LikesCrawler(uid):
    url = "https://streetvoice.com" + uid + "likes"
    #print(url)
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
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
        time.sleep(30)
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
            Uid.append(uid[1:-1])
            Song.append(inf[3])
            ArtistUid.append(inf[1])
            
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

# 如果發生 Exception，shell 將會 print 出當前執行的 index 
# 若程式因 Exception 停止，請執行以下步驟：
# 1. 把 count 和 data[<count>:] 的數值改成 index
# 2. 把 df11.csv 的內容存到另一個 csv 檔中
# 3. 再次啟動程式
count = 0
for uid in data[0:]:
    try:
        LikesCrawler(uid)
        count += 1
    except:
        print(count)
        print("======== df11 saving ... ========")
        df11 = pd.DataFrame(zip(Uid, Song, ArtistUid), columns = ['Uid', 'Liked Song', 'ArtistUid'])
        df11.to_csv('df11.csv', index=False)
        
        time.sleep(30)
        LikesCrawler(uid)
        count += 1
  
print("======== df11 complete ========")
df11 = pd.DataFrame(zip(Uid, Song, ArtistUid), columns = ['Uid', 'Liked Song', 'ArtistUid'])
df11.to_csv('df11.csv', index=False)