"""
link = https://www.nhaccuatui.com/bai-hat/bai-hat-moi.1.html
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

music_data = []
for i in range(1,51,1):
    url = f"https://www.nhaccuatui.com/bai-hat/bai-hat-moi.{i}.html"

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")


    items = soup.find_all("div", class_="box-content-music-list")


    for item in items:
        try:
            link = item.find("a")
            if link and "title" in link.attrs:
                title_tag = link["title"]
                if "-" in title_tag:
                    name, singer = map(str.strip, title_tag.split("-", 1))
                    music_data.append({"Name": name, "Singer": singer})
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue

df = pd.DataFrame(music_data)

df.to_csv("10.Nhaccuatui.csv", index=False, encoding="utf-8-sig")