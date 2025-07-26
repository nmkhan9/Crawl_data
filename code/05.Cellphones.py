"""
link = "https://cellphones.com.vn/mobile.html"
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

data_base = []

def get_url(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def make_payload(page):
    return {
        "query": """
            query GetProductsByCateId {
                products(
                    filter: {
                        static: {
                            categories: ["3"],
                            province_id: 30,
                            stock: { from: 0 },
                            stock_available_id: [46, 56, 152, 4920],
                            filter_price: { from: 0 to: 50000000 }
                        },
                        dynamic: {}
                    },
                    page: %d,
                    size: 20,
                    sort: [{ view: desc }]
                ) {
                    general {
                        name
                        manufacturer
                        sku
                        url_path
                    }
                    filterable {
                        price
                        special_price
                        thumbnail
                    }
                }
            }
        """ % page,
        "variables": {}
    }

url = "https://api.cellphones.com.vn/v2/graphql/query"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

page = 1
crawled_links = set()

while page <= 10:
    res = requests.post(url, headers=headers, json=make_payload(page))
    data = res.json()
    items = data["data"]["products"]

    for item in items:
        link_item = "https://cellphones.com.vn/" + item["general"]["url_path"]
        soup_product = get_url(link_item)

        details = soup_product.find("div", class_="list-linked")
        if not details:
            continue

        abcs = details.find_all("a")
        if not abcs:
            continue

        for prodcut in abcs:
            link_in4 = "https://cellphones.com.vn" + prodcut["href"]

            if link_in4 in crawled_links:
                continue
            crawled_links.add(link_in4)

            soup_detail = get_url(link_in4)

            title_tag = soup_detail.find("div", class_="box-product-name")
            title = title_tag.find("h1").get_text(strip=True) if title_tag else None

            new_price_tag = soup_detail.find("div", class_="sale-price")
            new_price = new_price_tag.get_text(strip=True) if new_price_tag else None

            old_price_tag = soup_detail.find("del", class_="base-price")
            old_price = old_price_tag.get_text(strip=True) if old_price_tag else None

            rate_tag = soup_detail.find("span", class_="total-rating")
            rate = rate_tag.get_text(strip=True) if rate_tag else None

            ls_sp = {
                "Name": title,
                "Link": link_in4,
                "New_price": new_price,
                "Old_price": old_price,
                "Review": rate
            }

            details_sp = soup_detail.find_all("tr", class_="technical-content-item")
            for sp in details_sp:
                key_tag = sp.find("td")
                value_tag = key_tag.find_next("td") if key_tag else None

                if key_tag and value_tag:
                    key = key_tag.get_text(strip=True)
                    value_p = value_tag.find("p")
                    value = value_p.get_text(strip=True) if value_p else value_tag.get_text(strip=True)
                    ls_sp[key] = value

            data_base.append(ls_sp)

    page += 1

df = pd.DataFrame(data_base)
df.to_csv('05.mobile_cellphones.csv', index=False, encoding='utf-8-sig')
print("Doneeeee!")
