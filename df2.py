from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re
import numpy as np
import pandas as pd

data = np.array( pd.read_csv('df2_pre.csv', header=None))[1:]
print(data[0][1])

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
    driver = webdriver.Edge(executable_path='msedgedriver.exe')
    driver.implicitly_wait(10) 
    driver.maximize_window()
    driver.set_page_load_timeout(600)
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()

    playcount = soup.find(id="countup-play").getText()
    #print(playcount)
    playcount = playcount.replace(',', '')
    likecount = soup.find(id="countup-like").getText()
    sharecount = soup.find(class_="mb-0 text-center js-share-count").getText()
    temp = soup.find(class_="text-truncate text-white opacity-72")
    catagory = temp.find(href = True).getText()
    publishtime = soup.find(class_="text-gray-light mb-2").getText()[-10:]
        
    Playcount.append(playcount)
    Likecount.append(likecount)
    Sharecount.append(sharecount)
    Catagory.append(catagory)
    PublishTime.append(publishtime)
    
count = 200
for d in data[200:]:
    try:
        informCrawler(d[0], d[1])
        Uid.append(d[0])
        Song.append(d[1])
        count += 1
    except:
        print(count)
        df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                   columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
        df2.to_csv('df2.csv', index=False)
        time.sleep(10)
        informCrawler(d[0], d[1])
        Uid.append(d[0])
        Song.append(d[1])
        count += 1
      
df2 = pd.DataFrame(zip(Uid, Song, Playcount, Likecount, Sharecount, Catagory, PublishTime), 
                   columns = ['Uid', 'Song', 'Play count', 'Like count', 'Share count', 'Catagory', 'Publish time'])
df2.to_csv('df2.csv', index=False)  