key = "key"
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=key)

uploads = "UUt7fwAhXDy3oNFTAzF2o8Pw"
res = youtube.playlistItems().list(playlistId=uploads, part='snippet', maxResults=4000, ).execute()
dict = {}
token = None

while True:
    try:
        res = youtube.playlistItems().list(playlistId=uploads, part='snippet', maxResults=50, pageToken=token).execute()
        for i in res['items']:
            dict[i['snippet']['title']] = i['snippet']['description']
        token = res['nextPageToken']
        if token is None:
            break
    except KeyError:
        for i in res['items']:
            dict[i['snippet']['title']] = i['snippet']['description']
        break

f = open("ratings.txt", "wb")
for i in dict:
    f.write(f"{i}|||{dict[i]}\n|||".encode("utf-8"))
f.close()

import re

with open('ratings.txt', "rb") as file:
    all = file.read().decode("utf-8")
    all = all.split("|||")
    all = all[:-1]
    ratings_dict = {}
    for n, i in enumerate(all):
        if n % 2 == 0:
            rating = re.findall("10/10", all[n + 1])
            if rating:
                ratings_dict[i] = rating
            if not rating:
                rating = re.findall("\d/10", all[n + 1])
                ratings_dict[i] = rating
            else:
                ratings_dict[i] = "no rating found in video description"

    f = open("results.txt", "wb")
    for i in ratings_dict:
        f.write(f"{i}, {ratings_dict[i]}\n".encode("utf-8"))
