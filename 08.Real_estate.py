import requests
import pandas as pd

base = "https://muaban.net/listing/v1/classifieds/listing"
params = {
    "subcategory_id": 169,
    "category_id": 33,
    "limit": 20,
    "offset":0
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(base,params=params, headers=headers)
data = res.json()
items = data["items"]


def parse_item(item):
    attributes = item.get("attributes", [])

    def get_attr(idx):
        try:
            return attributes[idx]["value"]
        except IndexError:
            return ""

    return {
        "ID": item.get("id"),
        "Tiêu đề": item.get("title"),
        "Tóm tắt": item.get("summary", ""),
        "Diện tích": get_attr(0),
        "Phòng ngủ": get_attr(1),
        "WC": get_attr(2),
        "Giá": item.get("price_display"),
        "Giá gốc": item.get("price"),
        "Khu vực": item.get("location"),
        "Ngày đăng": item.get("publish_at", "")[:10],
        "Số ảnh": item.get("total_images"),
        "Link": f"https://muaban.net{item.get('url')}",
        "SĐT (hiển thị)": item.get("phone_display"),
        "SĐT (mã hóa)": item.get("phone_enc"),
    }
all_items =[]
seen_ids = set()
for page in range(10):
    params["offset"] = page * 20
    res = requests.get(base, params=params, headers=headers)
    data = res.json()
    items = data.get("items", [])
    for item in items:
        item_id = item.get("id")
        if item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        all_items.append(parse_item(item))


df = pd.DataFrame(all_items)
df.to_csv("08.muaban_bds.csv", index=False, encoding="utf-8-sig")

