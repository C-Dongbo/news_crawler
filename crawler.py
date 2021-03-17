import requests
import re
from bs4 import BeautifulSoup
from parser import naver

def get_title_desc(news_info):
    title = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > a')
    desc = news_info.select_one('div.news_wrap.api_ani_send > div.news_area > div.news_dsc > div.dsc_wrap > a')
    return re.sub('\.\.\.','',title.text), re.sub('\.\.\.','',desc.text)

def get_news(query):
    naver_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format(query)
    res = requests.get(naver_url)
    soup = BeautifulSoup(res.content,'html.parser')

    news_info_list = soup.select('#main_pack > section > div.api_subject_bx > div.group_news > ul > li')

    title_list = []
    desc_list = []
    for news_info in news_info_list:
        title, desc = get_title_desc(news_info)
        title_list.append(title)
        desc_list.append(desc)
        print(title + '\t' + desc)


if __name__ == '__main__':
    #get_news('삼성전자')
    parser = naver("삼성전자")
    results = parser.get_news_info()
    print(results[0])