"""
link = "https://www.filmsfatale.com/blog/2021/8/2/the-best-100-music-videos-of-all-time"
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://www.filmsfatale.com/blog/2021/8/2/the-best-100-music-videos-of-all-time')
soup = BeautifulSoup(response.content, "html.parser")

musics = soup.findAll('strong')

data=[]
for music in musics :
    name = music.get_text(strip='True')
    rank,hjhj = name.split('.',1)
    item ={
        'Rank' : rank,
        'Name' : hjhj
    }
    data.append(item)

df=pd.DataFrame(data)
df.loc[df['Rank']=='1A','Rank']=1.1
df.loc[df['Rank']=='1B','Rank']=1.2

df['Rank']=df['Rank'].astype('float')
df=df.sort_values('Rank').reset_index(drop=True)
df.to_csv("02.The_best_music.csv",index=False,encoding="utf-8-sig")