import requests
from bs4 import BeautifulSoup

url = "https://bonbanh.com/xe-nissan-sunny-xl-2013-6314454"

resp = requests.get(url)
soup = BeautifulSoup(resp.content, "html.parser")

import requests
from bs4 import BeautifulSoup
import re

def in4(soup):
    specs = {}

    # Lấy phần tên thô
    name_tag = soup.find("div", class_="title")
    raw_name = name_tag.find_next("h1").get_text(separator=" ", strip=True) if name_tag else None

    if raw_name:
        match = re.match(r"(Xe\s+)?(.+?)\s*-\s*([\d.,]+)\s*Triệu", raw_name, re.IGNORECASE)
        if match:
            name_only = match.group(2).strip()
            price_number = int(float(match.group(3).replace(",", ".")) * 1_000_000)
        else:
            name_only = raw_name.replace("Xe", "").strip()
            price_number = None

        specs["Name"] = name_only
        specs["Price"] = price_number

    # Lấy ngày đăng
    notes_div = soup.find("div", class_="notes")
    if notes_div:
        note_text = notes_div.get_text(strip=True)
        match_date = re.search(r"Đăng ngày (\d{2}/\d{2}/\d{4})", note_text)
        if match_date:
            specs["Ngày đăng"] = match_date.group(1)

    # Lấy các thông tin chi tiết khác
    spec_section = soup.find("div", class_="box_car_detail")
    if spec_section:
        rows = spec_section.find_all("div", class_="row")
        for row in rows:
            label_div = row.find("div", class_="label")
            value_div = row.find("div", class_="txt_input")
            if label_div and value_div:
                label = label_div.get_text(strip=True).replace(":", "")
                value = value_div.get_text(strip=True)
                specs[label] = value

    return specs



specs = in4(soup)

for key, value in specs.items():
    print(f"{key} - {value}")
