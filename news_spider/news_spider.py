# !/usr/bin/python
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pymysql.cursors
import threading,time

"""this file to spider the data and into your databases"""

__author__ = 'AidChow'


base_url = 'http://news.scuec.edu.cn/?cat=12&paged='
headers = {'user-agent': 'Chrome/57.0.2987.133'}
result = set()


def get_nes_list(page):
    url = base_url + str(page)
    html_source = requests.get(url=url, headers=headers)
    content = BeautifulSoup(html_source.text, 'html.parser').find_all('div', {'class': 'n-post'})
    for li in content:
        content_url = li.a['href']
        if content_url not in result:
            result.add(content_url)
            id_p = re.findall('\d.*', content_url)[0]
            title = li.a.text
            news_push_time = li.span.text
            news_preview = re.sub('\[…\]', '', li.p.text)
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
    connection = pymysql.connect(host='119.29.3.135',
                                 user='root',
                                 password='dangxuan601',
                                 db='dangxuandb',
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
    while len(get_nes_list(page)) > 0:
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
