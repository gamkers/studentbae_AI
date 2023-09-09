from bs4 import BeautifulSoup
import requests
import streamlit as st
from scripts.functions import *

def webscrape_MainNews(type):
    try:
        info = ["HEAD LINES", "NEWS", "AUTHOR", "DATE", "COUNTRY", "CATEGORY"]
        Date = []
        news = []
        authors = []
        catogory = []
        headlines = []
        country = []
        images=[]
        for i in range(0, 5):
            url = f"https://www.ndtv.com/{type}/page-{i}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            hl = data.find_all('h2', class_="newsHdng")
            new = data.find_all('p', class_="newsCont")
            author = data.find_all('span', class_="posted-by")
            image = data.find_all('div', class_="news_Itm-img")
            for h in hl:
                headlines.append(h.text)
            for i in new:
                i = i.text.replace("\n", "")
                news.append(i)
            for j in author:
                j = j.text.split("|")
                j = j[0]
                if "by" in j:
                    s = j.split("by")
                    j = s[-1]
                authors.append(j[:-3])
            for k in author:
                k = k.text.split("|")
                k = k[-1]
                k = k.split(",")
                if len(k) == 2:
                    Date.append(",".join(k[0:2])[:-112])
                else:
                    Date.append(",".join(k[0:2]))
            for l in new:
                catogory.append(type)
            for m in author:
                m = m.text.split("|")
                m = m[-1]
                m = m.split(",")
                m = m[-1]
                country.append(m[:-112].replace("2022", "NA"))

            for im in image:
                link =im.find('img').get('src')
                
                images.append(link)

        data = [list(item) for item in list(zip(headlines, news, authors, Date, country, catogory,images))]

        return data
    except:
        st.error("Out Of Services, Come Back Later")

def webscrape_News(cat,n):
    try:
        Date = []
        news = []
        authors = []
        catogory = []
        headlines = []
        country = []
        images=[]
        for i in range(1, 5):
            url = f"https://www.ndtv.com/page/topic-load-more/from/allnews/type/news/page/{i}/query/{cat}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            hl = data.find_all('div', class_="src_itm-ttl")
            new = data.find_all('div', class_="src_itm-txt")
            author = data.find_all('span', class_="src_itm-stx")
            image =data.find_all('img', class_="img_brd marr10")

            for h in hl:
                headlines.append(h.text)
            for i in new:
                i = i.text
                news.append(i[25:-20])
            for j in author:
                j = j.text.split("|")
                j = j[0]
                if "by" in j:
                    s = j.split("by")
                    j = s[-1]
                    authors.append(j)
                else:
                    authors.append(j[25:])
            for k in author:
                k = k.text.split("|")
                k = k[-1]
                Date.append(k[:-20])
            for l in new:
                catogory.append("Sports")
            for m in author:
                country.append("India")
            for im in image:
                link = im.get('src')
                images.append(link)

        data = [list(item) for item in list(zip(headlines, news, authors, Date, country, catogory,images))]

        return data
    except:
        st.error("Out Of Service")


