import json

import requests
from bs4 import BeautifulSoup
import Article
import db.db_accumulator as db_conx
import config.config as cfg

def scrap_ap_news():

    conf = cfg.read_config()
    d_base = db_conx.db_connection(conf)

    httpurls = []
    newlink = "https://apnews.com/hub/ap-top-news"
    H = requests.get(newlink.format(newlink))
    soapTest = BeautifulSoup(H.content, 'html.parser')
    project_href = [i['href'] for i in soapTest.find_all('a', href=True, attrs={'data-key':'card-headline'})]
    for i in project_href:
        httpurls.append("https://apnews.com" + i)
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

        #Author
        Author = "N/A"
        try:
            Names = soap.find('div', class_='Component-signature')
            Author = Names.get_text()
        except:
            #fallback
            try:
                meta_data = soap.find('script', attrs={'type':'application/ld+json'})
                json_data = json.loads(meta_data.get_text())
                if json_data["author"] and len(json_data["author"]) != 0:
                    Author = json_data["author"][0]
                else:
                    print("No author found for {}".format(url))
            except:
                print("Error getting author")

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
                    limit = limit + 1
                else:
                    break
        except AttributeError:
            print("Error getting content")

        # content 200 chars for now
        Content = Content[0:200]

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
            try:
                meta_data = soap.find('script', attrs={'type':'application/ld+json'})
                json_data = json.loads(meta_data.get_text())
                if json_data["image"] and len(json_data["image"]) != 0:
                    image_url = json_data["image"]
                else:
                    print("No image found for {}".format(url))
            except AttributeError:
                print("Error getting image url")

        article = Article.Article()
        article.category = Category
        article.headline = Headline
        article.authors = [Author]
        article.link = url
        article.description = Content
        article.publish_date = format_date
        article.img_url = image_url
        c = c + 1

        # write to mysql
        cur = d_base.cursor()
        cur.execute("INSERT INTO article (headline, category, author, description, link, imageurl, publishDate) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)" , (article.headline, article.category, article.authors[0],
                                     article.description, article.link, article.img_url, article.publish_date))

    d_base.commit()
    d_base.close()

if __name__ == "__main__":
    scrap_ap_news()