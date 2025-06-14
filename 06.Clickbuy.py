import requests
from bs4 import BeautifulSoup
import pandas as pd
products = []

for i in range (1,10):
    response = requests.get(f'https://clickbuy.com.vn/dien-thoai?page={i}')
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all('div',class_='list-products__item')
    for item in items :

        a_tag = item.find('a')
        link0 = 'https://clickbuy.com.vn' + a_tag['href']


        response1 = requests.get(link0)
        soup1 = BeautifulSoup(response1.content, "html.parser")
        related_versions = soup1.find_all('div', class_='related_versions__item')
        version_links = []

        for version in related_versions:
            a_tag = version.find('a')
            onclick = a_tag.get('onclick')
            if onclick:
                link1 = onclick.split("'")[1]
                full_link = 'https://clickbuy.com.vn' + link1
                version_links.append(full_link)


        for url in version_links:
            response2 = requests.get(url)
            soup2 = BeautifulSoup(response2.content, "html.parser")

            product = {}

            name_tag = soup2.find('h1', class_="product-name")
            product_name = name_tag.get_text(strip=True) if name_tag else None

            price_new_tag = soup2.find("p", class_="price")
            price_new_text = price_new_tag.get_text(strip=True) if price_new_tag else None

            price_old_tag = soup2.find("p", class_="price-old")
            price_old_text = price_old_tag.get_text(strip=True) if price_old_tag else None



            product = {
                'Product_Name': product_name,
                'Product_Link': url,
                'New_Price': price_new_text,
                'Old_Price': price_old_text
            }


            details = soup2.find_all('tbody')
            if details:
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

                table = details[-1]
                for key, label in fields.items():
                    tag = table.find('th', string=label)
                    value = tag.find_next('td').get_text(strip=True) if tag else None
                    product[key] = value

            products.append(product)


df = pd.DataFrame(products)
df = df.drop_duplicates(subset=['Product_Name', 'Product_Link'], keep='first')

df.to_csv('clickbuy_mobile.csv', index=False, encoding='utf-8-sig')
