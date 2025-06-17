import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

response = requests.get('https://www.empireonline.com/movies/features/best-movies-2/')
soup = BeautifulSoup(response.content, "html.parser")

movies = []
all_strong_tags = soup.find_all("strong")

for tag in all_strong_tags:
    title = tag.get_text(strip=True)

    description_tag = tag.find_next("p")
    description = description_tag.get_text(strip=True).split(':',1) if description_tag else ""
    match = re.match(r"(\d+)\)\s+(.*)\s+\((\d{4})\)", title)

    if match :
        movies.append({
            "rank" : int(match.group(1)),
            "title": match.group(2),
            "yop":match.group(3),
            "director": description[-1]
        })

df = pd.DataFrame(movies)
df.to_csv("01.The_best_movies.csv",index=False,encoding="utf-8-sig")