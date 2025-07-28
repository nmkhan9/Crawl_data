import requests
from bs4 import BeautifulSoup

url = "https://diemthi.vnexpress.net/index/detail/sbd/21002775/year/2025"

resp = requests.get(url)

soup = BeautifulSoup(resp.content,"html.parser")
person = {}
id_tag = soup.find("h2",class_="o-detail-thisinh__sbd")
sdb_tag = id_tag.find_next("label")
id = sdb_tag.find_next("strong").get_text(strip=True)

person["sbd"] = id

score_tag = soup.find("div",class_="o-detail-thisinh__diemthi")
score_table = score_tag.find("table", class_="e-table")

rows = score_table.find("tbody").find_all("tr")

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 2:
        subject = cols[0].get_text(strip=True)
        score = cols[1].get_text(strip=True)
        person[subject] = score

# In kết quả
print(person)