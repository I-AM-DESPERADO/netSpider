# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import urllib
import time,pymysql

url='http://widget.weibo.com/weiboshow/index.php?language=&width=280&height=800&fansRow=1&ptype=1&speed=0&skin=1&isTitle=1&noborder=1&isWeibo=1&isFans=0&uid=2033961762&verifier=9d3ce531&dpc=1'

def insertData(data):
    connection = pymysql.connect(host='59.68.29.90',
                                 user='root',
                                 password='dangxuan601',
                                 db='dangxuanDB',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cur:
    	judge_sql="select * from t_weibo where text_content='"+data['text']+"';"
    	print(judge_sql)
    	cur.execute(judge_sql)
    	r = cur.fetchone()
    	print(r)
    	if r is None:
    		sql = "insert into t_weibo(text_content,msg_from,cite,img,others_time,post_time,others_repost_num,others_talk_num,self_repost_num,self_talk_num) values('"+data['text']+"','"+data['msg_from']+"','"+data['cite']+"','"+data['img']+"','"+data['others_time']+"','"+data['post_time']+"',"+str(data['others_nums']['repost_num'])+","+str(data['others_nums']['talk_num'])+","+str(data['self_nums']['repost_num'])+","+str(data['self_nums']['talk_num'])+");"
    		print(sql)
    		result=cur.execute(sql)
    		print(result)
    		r=cur.fetchone()
    connection.commit()
    connection.close()



def get_msg(url,data=None):
    web_data=urllib.request.urlopen(url)
    time.sleep(1)
    #解析UTF-8的页面
    soup=BeautifulSoup(web_data.read(),'html.parser')
    talkPlaces=soup.select('div.weiboShow_mainFeed_list.clearfix')
    datas=[]
    data={}
    index=0
    ISOTIME="%Y-%m-%d %X"
    for talkPlace in talkPlaces:
        print("-" * 30)
        text=talkPlace.select('div > p.weiboShow_mainFeed_listContent_txt')[0].text
        print(text)
        
        #转发微博块
        #转发博主
        msg_froms=talkPlace.select('div.relay_container > div.relay_text > a')
        msg_from=msg_froms[0].text if msg_froms != [] else ""
        if msg_from!='':
            print("----"+msg_from+"----")
        #转发内容
        cites = talkPlace.select('cite.relay_user_words')
        cite=cites[0].text if cites != [] else ""
        if cite!='':
            print(cite)
        
        # #内容图
        # img=talkPlace.select('a > img')

        # img=[]
        # # for img in imgs :
        # img=(img.get('src') if img !=[] else "")
        # # 	img_list.append(img)
        # if img!=[]:
        #     print("图片:",img)
                #内容图
        imgs=talkPlace.select('a > img')
        img=(imgs[0].get('src') if imgs !=[] else "")
        if img!='':
            print("图片:"+img)


        #转发原微博时间
        others_times=talkPlace.select('div.relay_container > div.relay_bottom.WB_linkB > div.relay_info > a')
        others_time=(others_times[0].text if others_times !=[] else "")
        if others_time!='' :
            print('---原微博发布时间---'+others_time)
        #转发微博中的转发,评论数
        repost_others_nums = talkPlace.select('div.relay_container > div.relay_bottom.WB_linkB > div.relay_handle > a')
        print(repost_others_nums)
        if repost_others_nums:
            repost_others_num =repost_others_nums[0].text.split('(')[1].split(')')[0] if repost_others_nums[0].text!='转发' else 0
            print('-'*30+'转发:'+str(repost_others_num))
            talk_others_num = repost_others_nums[1].text.split('(')[1].split(')')[0] if repost_others_nums[1].text!='评论' else 0
            print('-' * 30 + '评论:' + str(talk_others_num))
        else :
            repost_others_num=0
            talk_others_num=0
        #发布微博时间
        post_times=talkPlace.select('p.weiboShow_mainFeed_listContent_action.WB_linkB > span.weiboShow_mainFeed_listContent_actionTime > a')
        post_time=(post_times[0].text if post_times !=[] else "")
        if post_time=="今天":
        	post_time=time.strftime(ISOTIME,time.localtime())
        if post_time!='':
            print('发布时间'+post_time)
        #发布微博中的转发评论数
        repost_self_nums=talkPlace.select(' p.weiboShow_mainFeed_listContent_action.WB_linkB > span.weiboShow_mainFeed_listContent_actionMore > a')
        print(repost_self_nums)
        repost_self_num = repost_self_nums[0].text.split('(')[1].split(')')[0] if repost_self_nums[0].text != '转发' else 0
        print('-' * 30 + '转发:' + str(repost_self_num))
        talk_self_num = repost_self_nums[1].text.split('(')[1].split(')')[0] if repost_self_nums[1].text != '评论' else 0
        print('-' * 30 + '评论:' + str(talk_self_num))
        data={
            'text':text,
            'msg_from':msg_from,
            'cite':cite,
            'img':img,
            'others_time':others_time,
            'post_time':post_time,
            'others_nums':{'repost_num':repost_others_num,'talk_num':talk_others_num},
            'self_nums':{'repost_num':repost_self_num,'talk_num':talk_self_num}
        }
        datas.append(data)
        insertData(data)
    #print(datas)
    return datas


def timer(n):
    while True:
        currtime = time.strftime("Savetime:%Y:%m:%d %H:%M:%S", time.localtime())
        print(currtime)
        get_msg(url)
        time.sleep(n)
timer(43200)


