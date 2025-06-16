import requests
import pandas as pd


api_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=454e679b-6512-b521-394a-35ece2d402da&urlKey=nha-sach-tiki&category=8322&page={}"


def get_url(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(link, headers=headers)
    return response


all_books = []

for page in range(1, 10):
    url = api_url.format(page)
    tiki1 = get_url(url)
    data = tiki1.json()
    products = data.get("data", [])

    for i,product in enumerate (products):
        id_book = product.get("id")
        name_book = product.get("name", "")
        link_book = f"https://tiki.vn/api/v2/products/{id_book}"

        sp = get_url(link_book)
        if sp.status_code == 200:
            try:
                details = sp.json()
            except Exception as e:
                print(f"Lỗi parse JSON từ {link_book}: {e}")
                continue
        else:
            print(f"Lỗi kết nối đến {link_book}, mã lỗi: {sp.status_code}")
            continue
        info = details.get('specifications', [])
        attributes = info[0].get('attributes', []) if info else []

        price_new = details.get("price", 0)
        price_old = details.get("list_price", 0)
        price_original = details.get("original_price", 0)
        description = details.get("short_description", "")

        quantity_sold = details.get("quantity_sold", {}).get("value", 0)
        discount = details.get("discount", 0)
        discount_rate = details.get("discount_rate", 0)
        rating_average = details.get("rating_average", 0)
        review_count = details.get("review_count", 0)

        authors = details.get("authors", [])
        author_name = authors[0]["name"] if authors else "N/A"

        book_info = {
            "Name": name_book,
            "Price (new)": price_new,
            "Price (old)": price_old,
            "Price (original)": price_original,
            "Description": description,
            "Sold": quantity_sold,
            "Discount": discount,
            "Discount Rate": discount_rate,
            "Rating": rating_average,
            "Review Count": review_count,
            "Author": author_name,
        }
        for attr in attributes:
            book_info[attr['name']] = attr['value']
        all_books.append(book_info)


df=pd.DataFrame(all_books)
df.to_csv("07.Books_Tiki.csv", index=False, encoding='utf-8-sig')
