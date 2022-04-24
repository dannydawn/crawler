from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import numpy as np
import pandas as pd

data = np.array( pd.read_csv('df2_pre.csv', header=None))[1:]
#print(data[0][1])

Uid = []
Song = []
Playcount = []
Likecount = []
Sharecount = []
Catagory = []
PublishTime = []

def informCrawler(uid, song):
    url = "https://streetvoice.com/" + uid + "/songs/" + song
    #print(url)
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    #driver.implicitly_wait(10) 
    driver.maximize_window()
    driver.set_page_load_timeout(600)
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()
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
        Uid.append(uid)
        Song.append(song)
        Playcount.append(playcount)
        Likecount.append(likecount)
        Sharecount.append(sharecount)
        Catagory.append(catagory)
        PublishTime.append(publishtime)

 
count = 4000
for d in data[4000:5000]:
    try:
        informCrawler(d[0], d[1])
        count += 1
    except:
        print(count)
        df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                   columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
        df2.to_csv('df2_040.csv', index=False)
        time.sleep(30)
        informCrawler(d[0], d[1])
        count += 1
      
df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                   columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
df2.to_csv('df2_040.csv', index=False)  
