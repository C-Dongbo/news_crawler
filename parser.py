import configparser
import requests
import re

from bs4 import BeautifulSoup

class naver():
    def __init__(self, query):
        super()
        config = configparser.ConfigParser()
        self.query = query
        self.url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format(self.query)
        self.id = 0 # 색인되어 있는 뉴스 id의 최댓값 가져오기

    def get_news_html(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content,'html.parser')
        news_info_list = soup.select('#main_pack > section > div.api_subject_bx > div.group_news > ul > li')
        return news_info_list

    def get_cluster_news_info(self):
        return

    def get_news_info(self):
        news_info_list = self.get_news_html()
        results = {}
        for news_info in news_info_list:
            self.id += 1
            title = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > a').text
            desc = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > div.news_dsc > div.dsc_wrap > a').text
            news_url = news_info.find("a")["href"]
            cluster = news_info.select_one('a.news_more')  # 숫자만 빼내야댐
            if cluster == None:

            print(cluster)
            cluster_news_url = 'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid={}&nso=&mynews=0&refresh_start=0&related=1'.format(self.query, "test")
            results[self.id] = {"title":title, "desc":desc, "url":news_url}

        return results

        