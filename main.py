import requests
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}
base_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=454e679b-6512-b521-394a-35ece2d402da&urlKey=nha-sach-tiki&category=8322&page={}"

total = 0

for page in range(1,2):
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    data = response.json()
    products = data.get("data", [])

product=products[0]

ad_list = product.get('advertisement', {}).get('ad', [])
if ad_list:
    props = ad_list[0].get('properties', {})
    print(props['url'])
else:
    print("Không có dữ liệu quảng cáo.")



