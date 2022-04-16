#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup

OUT_FILE = "data.csv"
CSV_HEADER = ['rank', 'title', 'score', 'flair', 'url']
LIMIT=100
DOMAIN="https://old.reddit.com"
SUBREDDIT="apple"
SORT_BY="new"
# Use https://curlconverter.com
COOKIES = {} 
HEADERS = {}

file = open(OUT_FILE, "w")
writer = csv.writer(file)
writer.writerow(CSV_HEADER)
count = 0
rank = 0
after = None
while rank < LIMIT:
    resource = f"{DOMAIN}/r/{SUBREDDIT}/{SORT_BY}/?sort={SORT_BY}&t=all&count={count}"
    if after:
        resource += f"&after={after}"
    response = requests.get(resource, headers=HEADERS, cookies=COOKIES)
    print(f"Fetched URL {resource}")
    count += 25
    soup = BeautifulSoup(response.content, "html.parser")
    things = soup.find_all("div", class_="thing")
    last_thing = things[-1]
    after = last_thing.get("data-fullname")
    nsfw_things = [thing for thing in things if "over18" in thing.get("class")]
    things_count = len(nsfw_things)
    print(f"NSFW posts found: {things_count} ({rank + things_count} overall)")
    for thing in nsfw_things:
        rank += 1
        title = thing.find("a", class_="title").text
        score = thing.get("data-score")
        flair = thing.find("span", class_="flair")
        url = DOMAIN + thing.get("data-permalink")
        writer.writerow([rank, title, score, flair, url])
        if rank == LIMIT:
            break
