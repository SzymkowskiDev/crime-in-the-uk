import time
import datetime
from requests_html import HTMLSession, HTML
import re
try: from .base import dal
except: pass
try: from base import dal
except: pass


base_page = 'https://crimestoppers-uk.org'
# testing with page 2
base_search_page = 'https://crimestoppers-uk.org/campaigns-media/news?page=2'


def get_base_search_page_content(url):
    # Taking url and checking if we're marked as bot, if yes, then will return False, else url html of url
    session = HTMLSession()
    url = session.get(url).html
    if 'robots' in url.xpath('/html/head/meta/@name'):
        time.slee(5)
        return False
    return url

def getContentLimit(data):    
    for k,l in enumerate(data):
        if "***" in l.text:
            return k

def get_base_info(url_html):
    arts_info = {}
    arts = url_html.xpath('//*[@id="main"]/main/article/div[1]/div/div[2]')
    test = re.compile('\: ')
    for i in range(1,len(arts[0].find('div.article-title'))+1):
            title = url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/strong')[0].text
            if test.findall(title):
                link = 'https://crimestoppers-uk.org' + url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/@href')[0]
                date = url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/time/text()')[0]
                arts_info[link] = {'title': title, 'post date': date, 'link': link}
    return arts_info

def get_detailed_info(data):
    datax = data
    # print(data)
    # print("***")
    for i in datax:
        # print(i)
        try:
            inner_content = get_base_search_page_content(i)
            subtitle = inner_content.find('h2')[0].text.strip()
            partContent = inner_content.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/span')
            Comment = ''.join([x.text.replace('“','').replace('”','').replace('\n\n',' ')
                for x in inner_content \
                .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/span')])
            limit = getContentLimit(partContent)
            content = ''.join([x.text for x in partContent[:limit]])
            commentAuthor = inner_content \
                .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/span')[0].text
            authorTitle = inner_content \
                .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/cite')[0].text
            datax[i]['subtitle'] = subtitle
            datax[i]['Comment'] = Comment
            datax[i]['content'] = content
            datax[i]['comment author'] = commentAuthor
            datax[i]['author title'] = authorTitle
            datax[i]['content'] = content
        except: pass

    return datax






def checkForArticles(myClient,content):
    final = []
    db = myClient["web_content"]
    col = db["articles"]
    # appcoll.find({},{ "_id": 0, "name": 1, "address": 1 })
    col_content = col.find({},{'link':1,'_id':0})
    # match = [x[0] for x in col_content]
    for i in content.items():        
            final.append(i)
    return final


def insertArticle(myClient, content):
    appdb = myClient["web_content"]
    appcoll = appdb["articles"]
    for i in content.items():
        appcoll.insert_one(i[1])



def main(myClient):
    # try connect to the site
    # if no bot then process
    # if bot drop session and create new and wait
    
    base_html = get_base_search_page_content(base_search_page)
    base_data = get_base_info(base_html)
    details_data = get_detailed_info(base_data)
    # filtered_data = checkForArticles(myClient,details_data)
    insert_to_mongo = insertArticle(myClient,details_data)



if __name__ == '__main__':
    if dal.connection == None:
        dal.mongo_init()

    myClient = dal.connection

    # while True:
    #     time.sleep(10)
        
    main(myClient)

