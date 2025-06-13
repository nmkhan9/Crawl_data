import requests
from bs4 import BeautifulSoup
import pandas as pd


response = requests.get('https://cellphones.com.vn/mobile.html')
soup = BeautifulSoup(response.content, "html.parser")

items = soup.findAll('div',class_='product-info-container product-item')
data =[]
for item in items :
    a_tag = item.find('div',class_='product-info').find('a')
    link =a_tag['href']
    price_show = a_tag.find('p',class_='product__price--show').get_text(strip=True)
    price_tag = a_tag.find('p', class_='product__price--through')
    if price_tag:
        price_through = price_tag.get_text(strip=True)
    else:
        price_through = None
    deal_tag = a_tag.find('p', class_='product__price--percent-detail')
    if deal_tag :
        deal = deal_tag.get_text(strip=True)
    else :
        deal=None
    name = a_tag.find('h3').get_text(strip=True)

    product = {
        'Name':name,
        'Price' : price_show,
        'Original price' : price_through,
        'Deal' : deal,
        'Link' : link

    }
    data.append(product)

df=pd.DataFrame(data)
#df.to_csv('mobile_cellphones.csv', index=False, encoding='utf-8-sig')
print(len(df))