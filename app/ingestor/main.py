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

class Web_content:
    pass



def get_content_loop(func,url):
    # act as decorator, if func return False will loop over till
    # content is available is used in scrapping functions to reach contant
    content = func(url)
    while content == False:
        time.sleep(5)
        del content
        content = func(url)
    return content



def get_base_search_page_content(url):
    # Taking url and checking if we're marked as bot,
    # if yes, then will return False, else url html of url
    session = HTMLSession()
    url = session.get(url).html
    check =  url.xpath('/html/head/meta/@name')
    if check[0] == 'ROBOTS':
        return False
    return url

def getContentLimit(data):
    # used to reach part of article where we find uninteresting data     
    for k,l in enumerate(data):
        if "***" in l.text:
            return k

def get_base_info(url_html):
    # loops over to find title, link, post date of article, returns dict which serve as collection to be extended when reaching for details
    arts_info = {}
    arts = url_html.xpath('//*[@id="main"]/main/article/div[1]/div/div[2]')
    test = re.compile('\: ')
    for i in range(1,len(arts[0].find('div.article-title'))+1):
            try:
                title = url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/strong')[0].text
            except: IndexError
            else:     
                if test.findall(title):
                    link = 'https://crimestoppers-uk.org' + url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/@href')[0]
                    date = url_html.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/time/text()')[0]
                    arts_info[link] = {'title': title, 'post date': date, 'link': link}
    return arts_info

def content_scenarios(data):
    # adds content of article to dict returned by get_base_info
    reward_line1 = getContentLimit(
            data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/span'))
    if isinstance(reward_line1,int):
        partContent = data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/span')
        content = ''.join([x.text for x in partContent[:reward_line1+1]])
        return content
    if isinstance(reward_line1,int) == False:
        reward_line2 = data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/p[2]/strong[1]')
        if '***' in reward_line2:
            partContent = data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/p[1]/text()')
            content = ''.join(reward_line2,[x for x in partContent if x != ''])
            return content
        if len(reward_line2) == 0:
            partContent = data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/p[1]/text()')
            strong = data.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/p[1]/strong/text()')
            content = ''.join([*strong,*[x for x in partContent if x != '']])
            return content

def get_detailed_info(data):
    datax = data
    for i in datax:
        # print(i)
        
        inner_content = get_content_loop(get_base_search_page_content,i)
        subtitle = inner_content.find('h2')[0].text.strip()
        # Comment = ''.join([x.text.replace('“','').replace('”','').replace('\n\n',' ')
        #     for x in inner_content \
        #     .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/span')])
            
        # partContent = inner_content.xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/span')

        # limit = getContentLimit(partContent) +1
        # content = ''.join([x.text for x in partContent[:limit]])
        try:
            content = content_scenarios(inner_content)
        except:
            content = ''
            pass
        if content == None: content = ''
        if subtitle != '':
            ''.join([subtitle,content])
        # try:
        #     commentAuthor = inner_content \
        #         .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/span')[0].text
        # except IndexError as index:
        #     commentAuthor = inner_content \
        #         .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/span/text()')
        #     if commentAuthor == None:
        #         commentAuthor = inner_content \
        #         .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/b/span/b/span/text()')
        # try:
        #     authorTitle = inner_content \
        #         .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/cite')[0].text
        # except IndexError as index:
        #      authorTitle = inner_content \
        #         .xpath('//*[@id="main"]/main/article/div[2]/div/div/div/div/blockquote/footer/cite/text()')
        
        # datax[i]['subtitle'] = subtitle
        # datax[i]['Comment'] = Comment
        datax[i]['content'] = content
        # datax[i]['comment author'] = commentAuthor
        # datax[i]['author title'] = authorTitle
    if datax:    
        return datax
    else:
        return


class Mongo_obj:     
    
    def __init__(self, client):
        self.client = client
        
    def set_data(self, data):
        self.data = data

    def add_content(self):
        filtered_data = self.check_For_Articles(self.client, self.data)
        self.insert_articles(self.client, filtered_data)

    def check_For_Articles(self, myClient, content):
        final = []
        db = myClient["web_content"]
        col = db["articles"]
        # col_content = [] 
        # for x in col.find({},{'_id':0,'title':1}):
        #     col_content.append([x['link']])
        return content
        # if len(a) == 0:
        #     return content
        # else:   
        #     col_content = [x['link'] for x in col.find({},{'link':1,'_id':0})]
        #     for i in content:        
        #             if i['link'] not in col_content:
        #                 final.append(i)
        #     return final
        

    def insert_articles(self, myClient, content):
        db = myClient["web_content"]
        col = db["articles"]
        for i in content:
            if i[1]['content'] != '':
                col.insert_one(i[1])

def findMostRecentArticle(content):
    pass

def get_last_page(content):
    # xpath = '//*[@id="main"]/main/article/div[1]/div/div[3]/div/nav/ul/li[15]/a'
    data = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[3]/div/nav/ul/li[15]/a/@href')
    splitted_data = int(data[0].split('/')[-1].split('=')[-1])
    return splitted_data

def main(myClient):

    # implement limit with envNs
    last_page = get_last_page(
                get_content_loop(
                    get_base_search_page_content,'https://crimestoppers-uk.org/campaigns-media/news?page=2'))
    
    mongo = Mongo_obj(myClient)

    for page in range(2,last_page):
        res = []        
        # base_html = get_base_search_page_content(base_search_page)
        start_page = f'https://crimestoppers-uk.org/campaigns-media/news?page={page}'
        base_html = get_content_loop(get_base_search_page_content,start_page)
        base_data = get_base_info(base_html)
        details_data = get_detailed_info(base_data)
        # return details_data
        if details_data:
            for article in details_data.items():
                res.append(article)
        
        mongo.set_data(res)
        mongo.add_content()
        time.sleep(5)
    

if __name__ == '__main__':
    if dal.connection == None:
        dal.mongo_init()

    myClient = dal.connection

    # while True:
    #     time.sleep(10)
        
    print(main(myClient))

