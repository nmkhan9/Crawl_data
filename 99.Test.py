import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get(f'https://clickbuy.com.vn/dien-thoai?page=1')
soup = BeautifulSoup(response.content, "html.parser")
items = soup.find_all('div',class_='list-products__item')
products = []
for i in range (1,10):
    response = requests.get(f'https://clickbuy.com.vn/dien-thoai?page={i}')
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all('div',class_='list-products__item')
    for item in items:
        a_tag = item.find('a')
        link = 'https://clickbuy.com.vn' + a_tag['href']
        name = a_tag.get('title', '').strip()

        # Khối chứa giá và mô tả
        info_price = a_tag.find('div', class_='detail')

        # Giá mới (giá đang bán)
        new_price_tag = info_price.find('ins', class_='new-price')
        new_price = new_price_tag.get_text(strip=True) if new_price_tag else None

        # Giá cũ (nếu có)
        old_price_tag = info_price.find('del', class_='old-price')
        old_price = old_price_tag.get_text(strip=True) if old_price_tag else None

        # Đánh giá số lượt review (nếu có)
        rate_title_tag = info_price.find('div', class_='rate_title')
        number_of_reviews = rate_title_tag.get_text(strip=True) if rate_title_tag else None

        # Quà tặng kèm (nếu có)
        gift_detail_tag = info_price.find('div', class_='gift-detail')
        gift_detail = gift_detail_tag.get_text(strip=True) if gift_detail_tag else None

        # Tính phần trăm giảm giá (deal)
        deal_tag = info_price.find('div', class_='ex_pricesale percent d-none')
        if deal_tag and deal_tag.has_attr('data-price') and deal_tag.has_attr('data-price1'):
            try:
                price = int(deal_tag['data-price'])
                price1 = int(deal_tag['data-price1'])
                deal = f"{round((1 - price / price1) * 100)}%" if price1 != 0 else "0%"
            except ValueError:
                deal = "0%"
        else:
            deal = "0%"

        # Tạo dictionary sản phẩm
        product = {
            'product_name': name,
            'new_price': new_price,
            'old_price': old_price,
            'discount': deal,
            'gift_detail': gift_detail,
            'number_of_reviews': number_of_reviews,
            'product_link': link
        }

        response1 = requests.get(link)
        soup1 = BeautifulSoup(response1.content, "html.parser")

        details =soup1.find_all('tbody')

        fields = {
            "screen_size": "Kích thước màn hình",
            "cpu": "CPU",
            "os": "Hệ điều hành",
            "internal_storage": "Bộ nhớ trong",
            "ram": "RAM",
            "battery_capacity": "Dung lượng pin",
            "color": "Màu sắc",
            "product_condition": "Tình trạng SP",
            "brand": "Hãng sản xuất",
            "main_camera": "Camera chính",
            "selfie_camera": "Camera phụ",
            "resolution": "Độ phân giải màn hình",
            "fast_charging": "Sạc nhanh"
        }

        for key, label in fields.items():
            tag = details[-1].find('th', string=label)
            value = tag.find_next('td').get_text(strip=True) if tag else None
            product[key] = value

        products.append(product)

df=pd.DataFrame(products)

df.to_csv('99.testtest.csv', index=False, encoding='utf-8-sig')

