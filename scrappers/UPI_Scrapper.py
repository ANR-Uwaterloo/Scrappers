import requests
from bs4 import BeautifulSoup
import Article
import db.db_accumulator as db_conx


def scrap_upi():
    d_base = db_conx.db_connection()
    httpurls = []
    upilink="https://www.upi.com/Top_News/2023/p{}"
    for page in range(1, 15):
        H = requests.get(upilink.format(page))
        print(upilink.format(page))
        soapTest = BeautifulSoup(H.content, 'html.parser')
        project_href = [i['href'] for i in soapTest.find_all('a', href=True, class_='row')]
        for i in project_href:
            httpurls.append(i)

    frame=[]

    c=210
    #will start from here again
    for url in httpurls[:]:
        print(c)
        print(url)
        HTML =requests.get(url)
        soap = BeautifulSoup(HTML.content, 'html.parser')
        if soap is None:
            continue
        try:
            Headline =soap.title.get_text()
            print(Headline)
        except AttributeError:
            print ("error: -")
            continue
        #article = soap.find('article', class_= 'trun')
        Category = soap.find('div', class_= 'breadcrumb')
        Category = Category.get_text().replace('\n','')
        Category= Category.strip()
        #print(Category)
        try:
            image = soap.find('div', class_ = "slide-image-container").find('img')

            if(image['src'] and image):
                image_url = image['src']
            elif(image['data-src'] and image):
                image_url = image['data-src']
            else:
                continue
        except AttributeError:
            continue
        Name = soap.find('div', class_ = 'author')
        Author= Name.get_text()
        article = soap.find('article')
        for tag in article.find_all('p'):
            Content=tag.text+'\n'
        date = soap.find('div', class_='article-date')
        date1= date.get_text()
        date2= date1.replace('\t', '')
        date2= date2.split('/')[0].strip()
        frame.append((Category,Headline,Author,url,Content,date2, image_url))

        article = Article.Article()
        article.category = Category
        article.headline = Headline
        article.authors = Author
        article.link = url
        article.description = Content
        article.publish_date = date2
        article.img_url = image_url

        # write to mysql
        cur = d_base.cursor()
        cur.execute("INSERT INTO article (headline, category, author, description, link, imageurl, publishDate) \
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (article.headline, article.category, article.authors[0],
                     article.description, article.link, article.img_url, article.publish_date))

        c = c + 1

    d_base.commit()
    d_base.close()

if __name__ == "__main__":
    scrap_upi()
