import requests
from bs4 import BeautifulSoup
import pandas as pd

data =[]
for i in range (1,100) :
    response = requests.get(f'https://www.utc.edu.vn/tin-tuc/trang/{i}')

    soup = BeautifulSoup(response.content, "html.parser")

    hjhj = soup.find('div',class_='lastest-news')
    titles =hjhj.find_all('div',class_='i-lastest')

    for title in titles :
        a_tag = title.find('a')

        link=a_tag['href']
        img_tag = a_tag.find('img')
        name = img_tag['alt']

        time_tag = title.find('div',class_='i-date').find('a')
        time = time_tag.get_text(strip=True)
        item ={
            'New news' : name,
            'Time' : time,
            'Link' : link
        }
        data.append(item)

df = pd.DataFrame(data)
df.to_csv('04.news_utc.csv', index=False, encoding='utf-8-sig')
print(len(df))
