import json

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import Article

def scrap_ap_news():
    httpurls = []
    upilink="https://www.upi.com/Top_News/2023/p{}"
    newlink = "https://apnews.com/hub/ap-top-news"
    H = requests.get(newlink.format(newlink))
    soapTest = BeautifulSoup(H.content, 'html.parser')
    project_href = [i['href'] for i in soapTest.find_all('a', href=True, attrs={'data-key':'card-headline'})]
    for i in project_href:
        httpurls.append("https://apnews.com" + i)

    mycsv = open('Final_AP_News.csv', 'a',encoding = 'utf-8')
    fieldnames = ['category','headline','author', 'link' , 'description', 'publish_date', 'img_url']
    writer = csv.DictWriter(mycsv,fieldnames=fieldnames)

    frame=[]

    c= len(httpurls)
    Headline = "N/A"
    #will start from here again
    for url in httpurls[:]:
        print(c)
        print(url)
        HTML =requests.get(url)
        soap = BeautifulSoup(HTML.content, 'html.parser')
        if soap is None:
            continue
        try:
            Headline = soap.title.get_text()
            print(Headline)
        except AttributeError:
            print ("error: Getting headline")
            continue

        #Author
        Author = "N/A"
        try:
            Names = soap.find('div', class_='Component-signature')
            Author = Names.get_text()
        except:

            #fallback
            meta_data = soap.find('script', attrs={'type':'application/ld+json'})
            json_data = json.loads(meta_data.get_text())
            if json_data["author"] and len(json_data["author"]) != 0:
                Author = json_data["author"][0]
            else:
                print("No author found for {}".format(url))

        #timestamp
        format_date = "N/A"
        date = soap.find('span', attrs={'data-key':'timestamp'})
        date1 = date.get_text()
        date2 = date1.replace('\t', '')
        format_date = date2.split('/')[0].strip()

        #content
        Content = "N/A"
        limit = 0
        try:
            article = soap.find('div', class_="Article", attrs={'data-key':'article'})
            for tag in article.find_all('p'):
                if limit < 3:
                    Content += tag.text + '\n'
                    limit = limit  + 1
                else:
                    break
        except AttributeError:
            print("Error getting content")


        #Category
        Category = "N/A"
        Category_tag = soap.find('meta', attrs={'property':'article:tag'})
        Category = Category_tag.get("content")

        #image
        image_url = "N/A"
        try:
            image = soap.find('meta', attrs={'property':'og:image'})
            image_url = image.get("content")
        except AttributeError:
            #fallback
            meta_data = soap.find('script', attrs={'type':'application/ld+json'})
            json_data = json.loads(meta_data.get_text())
            if json_data["image"] and len(json_data["image"]) != 0:
                image_url = json_data["image"]
            else:
                print("No image found for {}".format(url))

        article = Article()
        article.category = Category
        article.headline = Headline
        article.authors = Author
        article.link = url
        article.description = Content
        article.publish_date = format_date
        article.img_url = image_url
        # frame.append((Category,Headline,Author,url,Content,format_date, image_url))
        writer.writerow(article.get_dict())
        c=c+1
    mycsv.close()

#data=pd.DataFrame(upperframe, columns=['Headline','Link','Date','Content','Author'])
#data = pd.DataFrame(frame, columns=['category','headline','author','link','description','date', 'img_url'])

if __name__ == "__main__":
    scrap_ap_news()
