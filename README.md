# crawler
妍伶：我把總共 795 名的音樂人ID 透過 sorted()的方式進行字母由小到大排序，  
因為 df6 的資料量過於龐大，一次爬蟲須爬超過10小時，所以我將 795 名音樂人切分成 8 個區段（如下），  
分別產出 df6-0.csv、df6-1.csv 到 df6-7.csv。

```python
musicianID_list = sorted(list(musicianID))

# 總共 795 人
# 0-99
musicianID_list0 = musicianID_list[0:100]
# 100-199
musicianID_list1 = musicianID_list[100:200]
# 200-299
musicianID_list2 = musicianID_list[200:300]
# 300-399
musicianID_list3 = musicianID_list[300:400]
# 400-499
musicianID_list4 = musicianID_list[400:500]
# 500-599
musicianID_list5 = musicianID_list[500:600]
# 600-699
musicianID_list6 = musicianID_list[600:700]
# 700-794
musicianID_list7 = musicianID_list[700:795]
```
