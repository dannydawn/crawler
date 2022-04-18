import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import numpy as np
import pandas as pd

d1 = np.array( pd.read_csv('R&B_靈魂_藍調_爵士_拉丁.csv', header=None).transpose() )[0]
d2 = np.array( pd.read_csv('舞曲_Remix_ACG_電音.csv', header=None).transpose() )[0]
d3 = np.array( pd.read_csv('嘻哈_饒舌_雷鬼_Funk.csv', header=None).transpose() )[0]

data = np.concatenate((d1, d2, d3))
data = np.unique(data)

def LikesCrawler(uid):
    url = "https://streetvoice.com" + uid + "likes"
    #print(url)
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.implicitly_wait(2) 
    driver.maximize_window()
    driver.set_page_load_timeout(7)
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
            Uid3.append(uid[1:-1])
            Song3.append(inf[3])
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
                Uid4.append(uid[1:-1])
                Song4.append(inf[3])
                CollabUid.append(inf[1])
    else:
        print("No Collab")
        pass

while True:    
    index = input("輸出表三 or 表四? (3/4)")
    if index == '3' or index == '4':
        break
    else:
        print("invalid input. try again. (3/4)")

Uid3 = []
Uid4 = []
Song3 = []
Song4 = []
ArtistUid = []
CollabUid = []

if index == '3':
    count = 0
    for uid in data[0:]:
        try:
            LikesCrawler(uid)
            count += 1
        except:
            print(count)
            time.sleep(10)
            LikesCrawler(uid)
            count += 1
# df3可能會因為 driver 的版本問題在執行過程出現 WebDriverException
# 若重覆發生，請確認 driver 版本，搜尋 stackoverflow，或移至 jupyter notebook 更改 count 值手動處理
# 細節可詢問 manchenlee
# (其實可以再加個 try except 輸出當前的 dataframe 但我好懶zz)  
    print("======== df3 complete ========")
    df3 = pd.DataFrame(zip(Uid3, Song3, ArtistUid), columns = ['Uid', 'Liked Song', 'ArtistUid'])
    #print(df)
    df3.to_csv('df3.csv', index=False)
elif index == '4':
    count = 0
    for uid in data:
        try:
            CollabCrawler(uid)
            count += 1
        except:
            print(count)
            time.sleep(5)
            CollabCrawler(uid)
            count += 1
            
    print("======== df4 complete ========")

    df4 = pd.DataFrame(zip(Uid4, Song4, CollabUid), columns = ['Uid', 'Collab Song', 'CollabUid'])
    #print(df)
    df4.to_csv('df4.csv', index=False)