import time
import datetime
from requests_html import HTMLSession, HTML
import re
from base import dal
from pymongo import errors, MongoClient


class ArticlesContent:
    BASE_PAGE = 'https://crimestoppers-uk.org'
    BASE_SEARCH_PAGE = 'https://crimestoppers-uk.org/campaigns-media/news?page=1'

    def __init__(self,mongo_client):
        self.mongo_client = mongo_client

    def check_connection(self) -> None:
        """
        Validator - checks connection for DELAY_LITERATIONS*DELAY_UNIT seconds
        if there is a reconnection to the database. If not, raise error.
        """

        DELAY_LITERATIONS = 10 #loops
        DELAY_UNIT = 1 #Sec per iteration

        for _ in range(DELAY_LITERATIONS):
            time.sleep(DELAY_UNIT)
            try:
                self.mongo_client.server_info()
            except errors.ServerSelectionTimeoutError:
                dal.mongo_init()
            else:
                break
        try:
            self.mongo_client.server_info()
        except errors.ServerSelectionTimeoutError as error:
            raise error


    def connection(self) -> MongoClient:
        """
        Connection to mongo db with checker, which checks connection status
        """
        self.check_connection()
        return self.mongo_client


    def main(self):
        # implement limit with envNs
        last_page = self.get_last_page(
                        self.get_content_loop(
                            self.check_bot_mark_return_content,'https://crimestoppers-uk.org/campaigns-media/news?page=1')
                        )


        mongo = MongoDataProc(self.connection())

        for page in range(1,last_page+1):
            self.check_connection()
            result = []        
            # base_html = get_base_search_page_content(base_search_page)
            start_page = f'https://crimestoppers-uk.org/campaigns-media/news?page={page}'
            base_html = self.get_content_loop(self.check_bot_mark_return_content,start_page)
            base_data = self.get_base_info(base_html,page)
            details_data = self.get_detailed_content(base_data)
            # return details_data
            if details_data:
                for article in details_data.items():
                    result.append(article)
            
            mongo.set_data(result)
            mongo.add_articles()
            time.sleep(5)

    def get_content_loop(self,func,url):
    # act as decorator, if func return False will loop over till
    # content is available is used in scrapping functions to reach contant
        content = func(url)
        while content == False:
            time.sleep(5)
            del content
            content = func(url)
        return content


    def check_bot_mark_return_content(self,url):
        # Taking url and checking if we're marked as bot,
        # if yes, then will return False, else url html of url
        session = HTMLSession()
        content = session.get(url).html
        check =  content.xpath('/html/head/meta/@name')
        if check[0] == 'ROBOTS':
            return False
        return content


    def get_last_page(self,content):
        data = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[4]/div/nav/ul/li[13]/a/@href')
        splitted_data = int(data[0].split('/')[-1].split('=')[-1])
        return splitted_data


    def get_detailed_content(self,articles):
        for article in articles:
            inner_content = self.get_content_loop(self.check_bot_mark_return_content,article)
            subtitle = inner_content.find('h2')[0].text.strip()
            try:
                body = self.get_article_body(inner_content)
            except:
                body = ''
                pass
            if body == None: body = ''
            if subtitle != '':
                body = ''.join([subtitle,body])
            articles[article]['content'] = body
        return articles


    def get_base_info(self,content,page):
        # loops over to find title, link, post date of article,
        # returns dict which serve as collection to be extended when reaching for details
        content_with_base_data = {}
        
        # articles which are interesting for us usually have ":" within name
        test = re.compile('\: ')
        
        if page != 1:
            arts = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[2]')

            for i in range(1,len(arts[0].find('div.article-title'))+1):
                    try:
                        title = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/strong')[0].text
                    except: IndexError
                    else:     
                        if test.findall(title):
                            link = self.BASE_PAGE + content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/@href')[0]
                            date = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/time/text()')[0]
                            content_with_base_data[link] = {'title': title, 'post date': date, 'link': link}
        elif page == 1:            

            try:
                lead_title = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[2]/div[1]/article/a/div/strong')[0].text
            except: IndexError
            else:     
                if test.findall(lead_title):
                    lead_link = self.BASE_PAGE + content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[1]/article/a/@href')
                    lead_date = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[1]/article/a/div/time/text()')
                    content_with_base_data[link] = {'title': lead_title, 'post date': lead_date, 'link': lead_link}

            first_half_articles = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[2]')

            for i in range(1,len(first_half_articles[0].find('div.article-title'))):
                    try:
                        title = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[2]/div/div[{i}]/article/a/div/strong')[0].text
                    except: IndexError
                    else:     
                        if test.findall(title):
                            link = self.BASE_PAGE + content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[2]/div/div[{i}]/article/a/@href')[0]
                            date = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/time/text()')[0]
                            content_with_base_data[link] = {'title': title, 'post date': date, 'link': link}

            second_half_articles = content.xpath('//*[@id="main"]/main/article/div[1]/div/div[3]')

            for i in range(1,len(second_half_articles[0].find('div.article-title'))+1):
                    try:
                        title = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[3]/div[{i}]/article/a/div/strong')[0].text
                    except: IndexError
                    else:     
                        if test.findall(title):
                            link = self.BASE_PAGE + content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[3]/div[{i}]/article/a/@href')[0]
                            date = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[3]/div[{i}]/article/a/div/time/text()')[0]
                            content_with_base_data[link] = {'title': title, 'post date': date, 'link': link}
        
        # str to datetime transformation
        for pos in content_with_base_data.items():
            pos[1]['post date'] = datetime.datetime.strptime(pos[1]['post date'],"%d/%m/%Y")

        return content_with_base_data


    def get_article_body(self,content):
        article_body = []
        # adds body of article to dict returned by get_base_info
        def test_for_common(paragraph):
            # check if paragraph is one of common paragraph added to most of articles 
            commons = [
                'Please note: Computer IP addresses are never traced, and no-one',
                '***Information passed directly to police will not qualify for a reward',
                'To give information 100% anonymously and',
                '***Note: Information passed directly to police will not qualify. The reward',
                'If you have information, please fill in our simple and secure '
                    ]
            test = False
            for common in commons:
                if common in paragraph:
                    test = True
                    return test
            return test

        body_box = content.xpath('//*[@id="main"]/main//div[2]/div/div/div/div')[0].text
        body_box_split = [x.strip() for x in body_box.split('\n') if x != '']
        for elem in body_box_split:
            if True == test_for_common(elem):
                continue
            else:
                article_body.append(elem)

        article_body = '\n'.join([x for x in article_body if x != ''])
        return article_body



class MostWantedContent:
    BASE_PAGE = 'https://crimestoppers-uk.org'
    BASE_SEARCH_PAGE = 'https://crimestoppers-uk.org/give-information/most-wanted?page=1&'

    def __init__(self,mongo_client):
        self.mongo_client = mongo_client


    def check_connection(self) -> None:
        """
        Validator - checks connection for DELAY_LITERATIONS*DELAY_UNIT seconds
        if there is a reconnection to the database. If not, raise error.
        """

        DELAY_LITERATIONS = 10 #loops
        DELAY_UNIT = 1 #Sec per iteration

        for _ in range(DELAY_LITERATIONS):
            time.sleep(DELAY_UNIT)
            try:
                self.mongo_client.server_info()
            except errors.ServerSelectionTimeoutError:
                dal.mongo_init()
            else:
                break
        try:
            self.mongo_client.server_info()
        except errors.ServerSelectionTimeoutError as error:
            raise error


    def connection(self) -> MongoClient:
        """
        Connection to mongo db with checker, which checks connection status
        """
        self.check_connection()
        return self.mongo_client


    def main(self):
        # implement limit with envNs
        last_page = self.get_last_page(
                        self.get_content_loop(
                            self.check_bot_mark_return_content,'https://crimestoppers-uk.org/give-information/most-wanted?page=1&')
                        )
        
        mongo = MongoDataProc(self.connection())

        for page in range(1,last_page+1):
            self.check_connection()
            result = []        
            # base_html = get_base_search_page_content(base_search_page)
            start_page = f'https://crimestoppers-uk.org/give-information/most-wanted?page={page}&'
            base_html = self.get_content_loop(self.check_bot_mark_return_content,start_page)
            base_data = self.get_base_info(base_html)
            details_data = self.get_detailed_content(base_data)
            # return details_data
            if details_data:
                for article in details_data.items():
                    result.append(article)
            
            mongo.set_data(result)
            mongo.add_most_wanted()
            time.sleep(5)

    def get_content_loop(self,func,url):
    # act as decorator, if func return False will loop over till
    # content is available is used in scrapping functions to reach contant
        content = func(url)
        while content == False:
            time.sleep(5)
            del content
            content = func(url)
        return content


    def check_bot_mark_return_content(self,url):
        # Taking url and checking if we're marked as bot,
        # if yes, then will return False, else url html of url
        session = HTMLSession()
        content = session.get(url).html
        check =  content.xpath('/html/head/meta/@name')
        if check[0] == 'ROBOTS':
            return False
        return content


    def get_last_page(self,content):
        data = content.xpath('//*[@id="main"]/main/article/div[3]/div[2]/div/div/nav/ul')[0].text
        splitted_data = int([x.strip() for x in data.split('\n') if x != ''][-1])
        return splitted_data


    def get_detailed_content(self,articles):
        for article in articles:
            inner_content = self.get_content_loop(self.check_bot_mark_return_content,article)
            # subtitle = inner_content.find('h2')[0].text.strip() no subtitle
            try:
                body = self.get_article_body(inner_content)
            except:
                body = ''
                pass
            if body == None: body = ''
            articles[article]['content'] = body
        return articles


    def get_base_info(self,content):
        # loops over to find title, link, post date of article,
        # returns dict which serve as collection to be extended when reaching for details
        content_with_base_data = {}
                
        wanteds = content.xpath('//*[@id="main"]/main/article/div[3]/div[1]/div[2]')

        for i in range(1,len(wanteds[0].absolute_links)+1):
                try:
                    title = content.xpath(f'//*[@id="main"]/main/article/div[3]/div[1]/div[2]/div[{i}]/div/div/span[1]')[0].text
                except: IndexError
                else:                        
                        link = self.BASE_PAGE + content.xpath(f'//*[@id="main"]/main/article/div[3]/div[1]/div[2]/div[{i}]/div/div/a/@href')[0]
                        # date = content.xpath(f'//*[@id="main"]/main/article/div[1]/div/div[2]/div[{i}]/article/a/div/time/text()')[0] no date
                        content_with_base_data[link] = {'title': title, 'link': link}
    
        
        # str to datetime transformation / no date in content
        # for pos in content_with_base_data.items():
        #     pos[1]['post date'] = datetime.datetime.strptime(pos[1]['post date'],"%d/%m/%Y")

        return content_with_base_data

    def get_article_body(self,content):
        article_body = []
        # adds body of article to dict returned by get_base_info
        def test_for_common(paragraph):
            # check if paragraph is one of common paragraph added to most of articles 
            commons = [
                'Recognise this person',
                'Call us anonymously',
                'To give information 100% anonymously and',
                '***Note: Information passed directly to police will not qualify. The reward',
                'If you have information, please fill in our simple and secure ',
                'Fill in our anonymous online form'
                    ]
            test = False
            for common in commons:
                if common in paragraph:
                    test = True
                    return test
            return test

        body_box = content.xpath('//*[@id="main"]/main/article/div[2]/div/div/div')[0].text
        body_box_split = [x.strip() for x in body_box.split('\n') if x != '']
        for elem in body_box_split:
            if True == test_for_common(elem):
                continue
            else:
                article_body.append(elem)

        article_body = '\n'.join([x for x in article_body if x != ''])
        return article_body


class MongoDataProc:     
    
    def __init__(self, client):
        self.client = client


    def set_data(self, data):
        self.data = data


    def add_most_wanted(self):
        filtered_data = self.check_for_most_wanted(self.client, self.data)
        if filtered_data:
            self.insert_most_wanted(self.client, filtered_data)

    def check_for_most_wanted(self, myClient, content):
        # check with link if most wanted was already processed if no then will add it to mongo

        db = myClient["web_content"]
        col = db["most_wanted"]
        final = []
        
        col_content = [x['link'] for x in col.find({},{'_id':0,'link':1})]
        for article in content:
            if article[1]['link'] not in col_content and article[1]['content'] != '' :
                final.append(article)
        return final


    def insert_most_wanted(self, myClient, content):
        db = myClient["web_content"]
        col = db["most_wanted"]
        for i in content:
                col.insert_one(i[1])


    def add_articles(self):
        filtered_data = self.check_for_articles(self.client, self.data)
        if filtered_data:
            self.insert_articles(self.client, filtered_data)


    def check_for_articles(self, myClient, content):
        # check with link if article was already processed if no then will add it to mongo

        db = myClient["web_content"]
        col = db["articles"]
        final = []
        
        col_content = [x['link'] for x in col.find({},{'_id':0,'link':1})]
        for article in content:
            if article[1]['link'] not in col_content and article[1]['content'] != '' :
                final.append(article)
        return final


    def insert_articles(self, myClient, content):
        db = myClient["web_content"]
        col = db["articles"]
        for i in content:
                col.insert_one(i[1])


if __name__ == '__main__':
    if dal.connection == None:
        dal.mongo_init()

    my_client = dal.connection
    
    # maybe add multi proc there
    article_processor = ArticlesContent(my_client)
    article_processor.main()

    most_wanted_processor = MostWantedContent(my_client)
    most_wanted_processor.main()