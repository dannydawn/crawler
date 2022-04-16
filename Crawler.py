#!/usr/bin/env python
# coding: utf-8

# # 建立每個要放入的list，之後轉成df用

# In[1]:


name = [] #名稱
name_link = [] #名稱連結
tp = [] #種類
live = [] #居住地
num = [] #音樂數量
fans = [] #粉絲
follow = [] #追蹤


# # 對Rock類型的歌爬蟲

# In[ ]:


#import requests
#from bs4 import BeautifulSoup
#
#dom = requests.get("https://streetvoice.com/music/browse/1/recommend/latest/").text
#soup = BeautifulSoup(dom, 'html.parser')


# In[2]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, re


# In[3]:


url = 'https://streetvoice.com/music/browse/1/recommend/latest/'
driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
driver.implicitly_wait(10) #延遲讀網頁，使所有動態跑完
driver.maximize_window()
driver.set_page_load_timeout(60) #最多等60秒
driver.get(url)

element = driver.find_element_by_id('js-loader') #按下點我看更多按鈕
element.click()

for i in range(0, 8):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #卷軸下拉顯示更多的fans
    time.sleep(3) #等待三秒讓網頁讀好

soup = BeautifulSoup(driver.page_source, 'html5lib')
#print(soup)

driver.quit()


# # 主頁: 擷取每個歌手的名稱以及網頁路徑

# In[4]:


ele = soup.find_all("ul", id = "item_box_list")

for i in ele:
    t = i.find_all("h5", "text-truncate")
    for i in t:
        tt = i.text.strip()
        name.append(tt)
        ll =  str("https://streetvoice.com") + str(i.a['href'])
        name_link.append(ll)

print(name)
print(name_link)


# # 抓取name 以及 name_link的唯一值

# In[5]:


name_link = list(set(name_link))

print(name_link)


# # 第二頁: 每個歌手的種類以及居住地

# In[6]:


for i in range(0, len(name_link)):
    
    dom = requests.get(name_link[i], time.sleep(3)).text #連結上面的姓名連結
    soup = BeautifulSoup(dom, 'html.parser')

    e = soup.find_all('span', 'mr-3') #抓取種類以及居住地的sector

    count = 1
    for i in e:
        if count == 1: #第一個為種類
            info = i.text.strip()
            tp.append(info)
            count += 1
        else: #加1之後為居住地
            info = i.text.strip()
            live.append(info)
    
print(tp)
print(live)


# # 第三頁: 抓音樂數量、fans、followers

# In[9]:


num_link = [] #音樂連結
fans_link = [] #粉絲連結
follow_link = [] #追蹤連結


# ## 整理 followers 和 following 連結

# In[10]:


for i in range(0, len(name_link)):
    dom = requests.get(name_link[i], time.sleep(3)).text
    soup = BeautifulSoup(dom, 'html.parser')
    e = soup.find_all('li', 'list-inline-item ml-3')

    count = 1
    for i in e:
        if count == 1: #第一個為followers
            lk = str("https://streetvoice.com") + str(i.a['href']) #followers' link
            fans_link.append(lk)
            count += 1
        else: #加1之後為following
            lk = str("https://streetvoice.com") + str(i.a['href']) #following link
            follow_link.append(lk)

print(fans_link)
print(follow_link)


# ## 爬取有多少followers

# In[11]:


for i in range(0, len(fans_link)):
    url = fans_link[i] #連結fans link
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
    driver.implicitly_wait(10) #延遲讀網頁，使所有動態跑完
    driver.maximize_window()
    driver.set_page_load_timeout(60) #最多等60秒
    driver.get(url)
    
    try:
        element = driver.find_element_by_id('js-loader')#按下點我看更多按鈕
        element.click()
    except Exception as e:
        print("")
    
    for i in range(0, 8):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #卷軸下拉顯示更多的fans
        time.sleep(3) #等待三秒讓網頁讀好
    
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    
    driver.quit()
    
    e = soup.find_all('h4', 'text-truncate') #抓取follower的姓名

    temp = [] #暫時儲存follower的姓名，等之後整個append到fans中
    for name in e:
        temp.append(name.text.strip())

    temp = temp[3:]
    fans.append(temp)


# In[19]:


fans = []


# In[14]:


for i in range(0, 3):
    url = fans_link[i] #連結fans link
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
    driver.implicitly_wait(10) #延遲讀網頁，使所有動態跑完
    driver.maximize_window()
    driver.set_page_load_timeout(60) #最多等60秒
    driver.get(url)
    
    try:
        element = driver.find_element_by_id('js-loader')#按下點我看更多按鈕
        element.click()
    except Exception as e:
        print("")
    
    for i in range(0, 8):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #卷軸下拉顯示更多的fans
        time.sleep(3) #等待三秒讓網頁讀好
    
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    
    driver.quit()
    
    e = soup.find_all('h4', 'text-truncate') #抓取follower的姓名

    temp = [] #暫時儲存follower的姓名，等之後整個append到fans中
    for name in e:
        temp.append(name.text.strip())

    temp = temp[3:]
    fans.append(temp)


# In[16]:


print(fans)


# In[ ]:


import pandas as pd
df = pd.DataFrame (fans)
df


# In[ ]:


export_csv = df.to_csv(r'follower.csv', header = False)


# ## 爬取有多少followings

# In[ ]:


for i in range(0, len(fans_link)):
    url = follow_link[i] #連結follow link
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
    driver.implicitly_wait(10) #延遲讀網頁，使所有動態跑完
    driver.maximize_window()
    driver.set_page_load_timeout(60) #最多等60秒
    driver.get(url)
    
    try:
        element = driver.find_element_by_id('js-loader')#按下點我看更多按鈕
        element.click()
    except Exception as e:
        print("")
    
    try:
        for i in range(0, 8):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #卷軸下拉顯示更多的fans
            time.sleep(3) #等待三秒讓網頁讀好
        
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        
        driver.quit()
        
        e = soup.find_all('h4', 'text-truncate') #抓取follower的姓名
        
        temp = [] #暫時儲存follower的姓名，等之後整個append到fans中
        for name in e:
            temp.append(name.text.strip())
        
        temp = temp[3:]
        follow.append(temp)
    except Exception as e:
        print("")


# In[17]:


for i in range(0, 5):
    url = follow_link[i] #連結follow link
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
    driver.implicitly_wait(10) #延遲讀網頁，使所有動態跑完
    driver.maximize_window()
    driver.set_page_load_timeout(60) #最多等60秒
    driver.get(url)
    
    try:
        element = driver.find_element_by_id('js-loader')#按下點我看更多按鈕
        element.click()
    except Exception as e:
        print("")
    
    try:
        for i in range(0, 8):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #卷軸下拉顯示更多的fans
            time.sleep(3) #等待三秒讓網頁讀好
        
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        
        driver.quit()
        
        e = soup.find_all('h4', 'text-truncate') #抓取follower的姓名
        
        temp = [] #暫時儲存follower的姓名，等之後整個append到fans中
        for name in e:
            temp.append(name.text.strip())
        
        temp = temp[3:]
        follow.append(temp)
    except Exception as e:
        print("")


# In[18]:


print(follow)

