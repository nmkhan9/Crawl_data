import requests

api_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=454e679b-6512-b521-394a-35ece2d402da&urlKey=nha-sach-tiki&category=8322&page={}"

def get_url(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(link, headers=headers)
    return response

all_books = []

for page in range(1, 2):
    url = api_url.format(page)
    tiki1 = get_url(url)
    data = tiki1.json()
    products = data.get("data", [])

    for i,product in enumerate( products):
        id_book = product["id"]
        name_book = product["name"]
        link_book = f"https://tiki.vn/api/v2/products/{id_book}"

        sp = get_url(link_book)
        details = sp.json()

        info = details.get('specifications', [])
        attributes = info[0].get('attributes', []) if info else []


        book_info = {"Name": name_book}
        for attr in attributes:
            book_info[attr['name']] = attr['value']

        all_books.append(book_info)

        if i == 10 :
            break


for book in all_books:
    print("=" * 50)
    for key, value in book.items():
        print(f"{key}: {value}")
