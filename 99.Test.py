import requests
from bs4 import BeautifulSoup
import pandas as pd

data=[]

response = requests.get(f'https://clickbuy.com.vn/dien-thoai?page=1')
soup = BeautifulSoup(response.content, "html.parser")

items = soup.find_all('div',class_='list-products__item')
a_tag = items[1].find('a')
link = 'https://clickbuy.com.vn' + a_tag['href']
response1 = requests.get(link)
soup1 = BeautifulSoup(response1.content, "html.parser")
print(soup1)
