# !/usr/bin/python
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import pymysql.cursors

"""run this file to create your databases"""

__author__ = 'AidChow'

# Connect to the database
connection = pymysql.connect(host='59.68.29.90',
                             user='root',
                             password='dangxuan601',
                             db='dangxuanDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
CREATE_DATA_BASE = 'CREATE DATABASE IF NOT EXISTS minda_news'
connection.cursor().execute(CREATE_DATA_BASE)
connection.cursor().execute('USE minda_news')

CREATE_NEWS_LIST = 'CREATE TABLE IF NOT EXISTS news_list(' \
                   'id INT AUTO_INCREMENT PRIMARY KEY,' \
                   'news_url VARCHAR(100)  CHARACTER SET utf8mb4  COLLATE utf8mb4_unicode_ci,' \
                   'news_p_id INT ,' \
                   'news_title CHAR(100)  CHARACTER  SET utf8mb4  COLLATE  utf8mb4_unicode_ci,' \
                   'news_push_time CHAR(30)  CHARACTER  SET utf8mb4  COLLATE  utf8mb4_unicode_ci,' \
                   'news_preview TEXT  CHARACTER  SET utf8mb4  COLLATE  utf8mb4_unicode_ci' \
                   ') DEFAULT CHARACTER SET utf8mb4'

CREATE_NEWS_CONTENt = 'CREATE TABLE IF NOT EXISTS news_content(' \
                      'id INT AUTO_INCREMENT PRIMARY KEY,' \
                      'news_p_id INT,' \
                      'news_content TEXT  CHARACTER  SET utf8mb4  COLLATE  utf8mb4_unicode_ci' \
                      ') DEFAULT CHARACTER SET utf8mb4'
connection.cursor().execute(CREATE_NEWS_LIST)

connection.cursor().execute(CREATE_NEWS_CONTENt)

connection.close()
