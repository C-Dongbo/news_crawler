import configparser
import requests
import re
import json

from bs4 import BeautifulSoup

class naver():
    def __init__(self, query):
        super()
        config = configparser.ConfigParser()
        self.query = query
        self.url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format(self.query)
        self.id = 0 # 색인되어 있는 뉴스 id의 최댓값 가져오기
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.content, 'html.parser')

    def get_news_html(self, soup):
        news_info_list = soup.select('#main_pack > section > div.api_subject_bx > div.group_news > ul > li')
        return news_info_list
    
    def get_page_info(self, soup=None):
        if soup == None:
            page_info_list = self.soup.select_one('#main_pack > div.api_sc_page_wrap > div.sc_page > div.sc_page_inner')
            page_list = ['https://search.naver.com/search.naver'+data['href'] for data in page_info_list.find_all('a')]
            return page_list
        else:
            page_info_list = soup.select_one('#main_pack > div.api_sc_page_wrap > div.sc_page > div.sc_page_inner')
            page_list = ['https://search.naver.com/search.naver'+data['href'] for data in page_info_list.find_all('a')]
            return page_list
            

    def get_cluster_news_info(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        page_list = self.get_page_info(soup)

        results = []
        first_news_flag = True

        for page_url in page_list:
            res = requests.get(page_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            news_info_list = self.get_news_html(soup)
            for news_info in news_info_list:
                if first_news_flag and first_page_flag: ## 클러스터 뉴스 페이지의 첫 뉴스는 대상 뉴스이므로 제외
                    first_news_flag = False
                    continue
                title = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > a').text
                desc = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > div.news_dsc > div.dsc_wrap > a').text
                news_url = news_info.find("a")["href"]
                results.append({"title": title, "desc":desc, "url":news_url})

        return results

    def get_news_info(self):
        page_list = self.get_page_info()
        results_list = []
        for page_url in page_list:
            res = requests.get(page_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            news_info_list = self.get_news_html(soup)
            results = {}
            for news_info in news_info_list:
                self.id += 1
                title = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > a').text
                desc = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > div.news_dsc > div.dsc_wrap > a').text
                news_url = news_info.find("a")["href"]
                cluster = news_info.select_one('a.news_more')  # 숫자만 빼내야댐
                if cluster != None:
                    cluster_str = str(cluster)
                    idx = cluster_str.find("news_submit_related_option('") + len("news_submit_related_option('")
                    num = cluster_str[idx:idx+13]
                    cluster_news_url = 'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid={}&nso=&mynews=0&refresh_start=0&related=1'.format(self.query, num)
                    cluster_news_results = self.get_cluster_news_info(cluster_news_url)
                results[self.id] = {"title":title, "desc":desc, "url":news_url, "cluster_news_list":cluster_news_results}
                results_list.append(results)
        return results_list

        
if __name__ == '__main__':
    parser = naver('삼성전자')
    news = parser.get_news_info()

    with open("news.json", "w", encoding='utf8') as json_file:
        json.dump(news, json_file)



