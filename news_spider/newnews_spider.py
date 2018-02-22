# !/usr/bin/python
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pymysql.cursors
import threading,time
__author__ = 'Tong'

headers = {
   'user-agent': 'Chrome/57.0.2987.133'
    }
result = set()
first_url='http://www.scuec.edu.cn'
base_url= 'http://www.scuec.edu.cn/s/329/t/1619/p/2/list.htm'
Dbase_url= 'http://www.scuec.edu.cn/s/329/t/1619/p/2/i/'
end_url = '/list.htm'


def get_news_list(page):
    pfc_url=Dbase_url + str(page) + end_url
    html_sourc = requests.get(url=pfc_url, headers=headers)
    content = BeautifulSoup(html_sourc.text, 'html.parser').find_all('table', {'class': 'columnStyle'})
    for li in content:
        content_first_url = li.a['href']
        content_url = first_url + content_first_url 
        if content_url not in result:
            result.add(content_url)
            #正则表达式提取content中的id_p
            id_p = re.findall(r"\d\d\d\d\d\d",content_url)[0]
            title = li.a.text
            news_push_first_time = li.tr.text
            news_push_time = re.findall(r'\d\d\d\d-\d\d-\d\d',news_push_first_time)[0]
            html_source_preview = requests.get(content_url, headers=headers)
            content_preview = BeautifulSoup(html_source_preview.text, 'html.parser').find_all('div', {'class', 'single-content'})
            for item in content_preview:
                #p_content = item.p.text
                news_preview = re.sub('\[…\]','',item.p.text)
            save_list(content_url, id_p, news_preview, news_push_time, title)
            get_news_content(content_url, id_p)
            
    return content
def save_list(content_url, id_p, news_preview, news_push_time, title):
    connection = pymysql.connect(host='59.68.29.90',
                                 user='root',
                                 password='dangxuan601',
                                 db='dangxuanDB',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cur:
        query_sql = 'SELECT news_p_id from news_list WHERE news_p_id=%s'
        cur.execute(query_sql, id_p)
        r = cur.fetchone()
        if r is None:
            print("new content")
            sql = 'INSERT INTO news_list  ' \
                  '(news_url,news_p_id,news_title,news_push_time,news_preview) ' \
                  'VALUES (%s,%s,%s,%s,%s)'
            p = int(id_p)
            cur.execute(sql, (content_url, p, title, news_push_time, news_preview))          
    connection.commit()
    connection.close()

def get_news_content(news_url, id_p):
    html_source = requests.get(news_url, headers=headers)
    content = BeautifulSoup(html_source.text, 'html.parser').find('div', {'class', 'left-content'})
    save_content(content, id_p)

def save_content(content, id_p):
    connection = pymysql.connect(host='59.68.29.90',
                                 user='root',
                                 password='dangxuan601',
                                 db='dangxuanDB',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cur:
        query_sql = 'SELECT news_p_id from news_content WHERE news_p_id=%s'
        cur.execute(query_sql, id_p)
        r = cur.fetchone()
        if r is None:
            sql = 'INSERT INTO news_content (news_p_id,news_content) VALUES (%s,%s)'
            cur.execute(sql, (int(id_p), connection.escape_string(str(content))))
    connection.commit()
    connection.close()

def get_news():
    page = 1
    while len(get_news_list(page)) > 0:
        pStr = 'The %d page' % page
        page += 1
        print(pStr)
    print('spider complete')

def timer(n):
    while True:
        currtime = time.strftime("Savetime:%Y:%m:%d-%H:%M:%S", time.localtime())
        print(currtime)
        get_news()
        time.sleep(n)
timer(300)


