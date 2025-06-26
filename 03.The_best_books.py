"""
link ="https://www.theguardian.com/books/2019/sep/21/best-books-of-the-21st-century"
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://www.theguardian.com/books/2019/sep/21/best-books-of-the-21st-century')
soup = BeautifulSoup(response.content, "html.parser")

texts = soup.findAll('strong')
texts.pop(0)
texts=texts[::-1]
data =[]

for i,text in enumerate (texts) :
    namebook = text.get_text(strip=True)
    item = {
        'Rank' : i,
        'Book' : namebook
    }
    data.append(item)

df = pd.DataFrame(data)
df.to_csv("03.The_best_books.csv",index=False,encoding="utf-8-sig")
