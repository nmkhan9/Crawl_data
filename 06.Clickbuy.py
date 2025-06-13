import requests
from bs4 import BeautifulSoup
import pandas as pd

data=[]
for i in range (1,10):
    response = requests.get(f'https://clickbuy.com.vn/dien-thoai?page={i}')
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all('div',class_='list-products__item')

    for item in items :
        a_tag = item.find('a')
        link = 'https://clickbuy.com.vn' + a_tag['href']
        name = a_tag['title']
        info_price = a_tag.find('div',class_='detail')
        new_price = info_price.find('ins',class_='new-price').get_text(strip=True)
        old_price_tag = info_price.find('del',class_='old-price')
        if old_price_tag :
            old_price = old_price_tag.get_text(strip=True)
        else :
            old_price =None
        rate_title = info_price.find('div',class_='rate_title').get_text(strip=True)
        gift_detail_tag = info_price.find('div',class_='gift-detail')
        if gift_detail_tag:
            gift_detail = gift_detail_tag.get_text(strip=True)
        else :
            gift_detail=None
        deal_tag = info_price.find('div',class_='ex_pricesale percent d-none')
        if int(deal_tag['data-price1']) != 0 :
            deal=str(int(round((1-int(deal_tag['data-price'])/int(deal_tag['data-price1']))*100,0))) +'%'
        else :
            deal='0%'
        product = {
            'Name_product':name,
            'New_price':new_price,
            'Old_proce':old_price,
            'Deal':deal,
            'Gift_detail':gift_detail,
            'Number_of_review':rate_title,
            'Link_product' : link
        }
        data.append(product)

df=pd.DataFrame(data)
df.to_csv('clickbuy_mobile.csv', index=False, encoding='utf-8-sig')

