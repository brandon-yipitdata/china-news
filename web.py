# -*- coding: utf-8 -*-
import datetime
import demjson
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pandas as pd
import private
import settings
import smtplib
import psycopg2
import re
import requests
import time
import uuid

pd.set_option('max_colwidth', 160)

def get_urls(conn, GET_URLS_QUERY):
    '''Query news database to find existing news urls'''
    cur = conn.cursor()
    cur.execute(GET_URLS_QUERY)
    list_of_urls = [tuple_[0] for tuple_ in cur.fetchall()]

    return list_of_urls

def get_yicai(conn, run_id, list_of_urls):
    '''Get Yicai stories and write to database'''
    url = 'https://www.yicai.com/api/ajax/getjuhelist?action=news&page=1&pagesize=50'
    res = requests.get(url)
    data = res.json()
    cur = conn.cursor()

    for d in data:
        row = {
            'run_id' : run_id,
            'uuid': str(uuid.uuid4()),
            'date_story': datetime.datetime.strptime(d['CreateDate'], '%Y-%m-%dT%H:%M:%S'),
            'source' : 'Yicai',
            'title' : d['NewsTitle'],
            'url' : 'https://www.yicai.com' + d['url'],
        }

        if row['url'] not in list_of_urls:
            cur.execute(settings.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']


def get_xinhua(conn, run_id, list_of_urls):
    '''Get Xinhua stories and write to DB'''
    url = 'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=50&tp=1&orderby=1'
    res = requests.get(url)
    raw_json = demjson.decode(res.content[1:-2])
    data = raw_json['data']['list']
    cur = conn.cursor()

    for d in data:
        row = {
            'run_id' : run_id,
            'uuid': str(uuid.uuid4()),
            'date_story': datetime.datetime.strptime(d['PubTime'], '%Y-%m-%d %H:%M:%S'),
            'source' : 'Xinhua',
            'title' : d['Title'],
            'url' : d['LinkUrl'],
        }

        if row['url'] not in list_of_urls:
            print 'We need this: ' + row['url']
            cur.execute(settings.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']


def get_reuters_china(conn, run_id, list_of_urls):
    '''Get Reuters stories on China'''
    url = 'https://wireapi.reuters.com/v7/feed/rapp/us/tabbar/feeds/china'
    res = requests.get(url)
    data = res.json()['wireitems']
    cur = conn.cursor()

    for d in data:
        try:
            row = {
                'run_id' : run_id,
                'uuid': str(uuid.uuid4()),
                'date_story': datetime.datetime.strptime(d['templates'][1]['story']['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
                'source' : 'Reuters',
                'title' : d['templates'][1]['story']['hed'],
                'url' : d['templates'][1]['template_action']['url'],
            }

            if row['url'] not in list_of_urls:
                print 'We need this: ' + row['url']
                cur.execute(settings.QUERY_INSERT, row)
                conn.commit()
            else:
                print 'We good on this: ' + row['url']

        except Exception as e:
            print e


def get_caixin(conn, run_id, list_of_urls):
    '''Get Caixin Stories on China'''
    url = 'https://gateway.caixin.com/api/data/getNewsListByPids?page=1&size=50&pids=101267062'
    res = requests.get(url)
    data = res.json()['data']['list']
    cur = conn.cursor()

    for d in data:
        row = {
            'run_id' : run_id,
            'uuid': str(uuid.uuid4()),
            'date_story': datetime.datetime.fromtimestamp(int(d['timestamp'])/1000),
            'source' : 'Xinhua',
            'title' : d['desc'],
            'url' : d['url'],
        }

        if row['url'] not in list_of_urls:
            print 'We need this: ' + row['url']
            cur.execute(settings.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']

def send_html_email(email_body, recipient, subject):
	"""This function sends an HTML email from my personal email"""

	fromaddress = private.EMAIL_FROM_ADDRESS

	message = MIMEMultipart("alternative", None, [MIMEText(email_body,'html','utf-8')])
	message['From'] = fromaddress
	message['Subject'] = subject

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddress, private.EMAIL_PASSWORD)
	text = message.as_string()
	server.sendmail(fromaddress, recipient, text)
	server.quit()

def get_the_news(conn):
    '''Get only the most recent set of news stories'''
    pd.set_option('max_colwidth', 160)

    cur = conn.cursor()
    cur.execute(settings.QUERY_GET_THE_NEWS)
    df = pd.DataFrame(cur.fetchall(), columns=['Source', 'Story', 'Url'])

    return df


def get_tonghuashun(ticker, conn, run_id, list_of_urls):
    '''Write new ticker-based stories from Tonghuashun to the database'''
    url = 'https://mnews.hexin.cn/listv2/us/{}_1.json'.format(ticker)
    print url

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'If-None-Match': 'W/"5baf85b7-11cd"',
    }

    res = requests.get(url, headers=headers)
    data = res.json()['pageItems']
    cur = conn.cursor()

    for d in data:
        try:
            row = {
                'run_id' : run_id,
                'uuid': str(uuid.uuid4()),
                'ticker' : ticker,
                'date_story' : int(d['ctime']),
                'source' : d['source'],
                'title' : d['title'],
                'url' : d['url']
            }

            if row['url'] not in list_of_urls:
                print 'We need this: ' + row['url']
                cur.execute(settings.QUERY_TONGHUASHUN_INSERT,row)
                conn.commit()
            else:
                print 'We already have this: ' + row['url']

        except Exception as e:
            print e



def get_newsapi(ticker, conn, run_id, newsapi, list_of_urls):
    '''Get China business news and write to DB'''
    cur = conn.cursor()
    headlines = newsapi.get_top_headlines(q='{}'.format(ticker), category='business',language='en', country = 'us')
    data = headlines['articles']
    print ticker

    for d in data:

        row = {
                'run_id': run_id,
                'uuid' : str(uuid.uuid4()),
                'ticker': ticker,
                'date_story' : datetime.datetime.strptime(d['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                'source': d['source']['name'],
                'url' : d['url'],
                'title' : d['title'][:250],
                'description' : d['description'][:250],
            }

        if row['url'] not in list_of_urls:
            try:
                cur.execute(settings.QUERY_NEWSAPI_INSERT, row)
                conn.commit()
            except Exception as e:
                print row['url']
                print e
                conn.rollback()
        else:
            print 'We good on this: ' + row['url']


def get_webhose(conn, run_id, webhoseio, list_of_urls, org, ticker):
    '''Get webhose news data and write to DB'''
    cur = conn.cursor()
    query_params = {
        "q": "language:english organization:{} site_type:news".format(org),
        "sort": "crawled"
    }

    output = webhoseio.query("filterWebContent", query_params)
    data = output['posts']

    for d in data:

        row = {
                'run_id': run_id,
                'uuid' : str(uuid.uuid4()),
                'ticker' : ticker,
                'date_story' : datetime.datetime.strptime(d['published'][0:19], '%Y-%m-%dT%H:%M:%S'),
                'source': d['thread']['site'][:490],
                'url' : d['url'][:490],
                'title' : d['title'][:490],
                'description' : d['text'][:490],
            }

        if row['url'] not in list_of_urls:
            try:
                cur.execute(settings.QUERY_WEBHOSE_INSERT, row)
                conn.commit()
            except Exception as e:
                print row['url']
                print e
                conn.rollback()
        else:
            print "We already have this: " + row['url']

def get_API_results(conn):
    '''Get only the most recent set of news stories'''
    pd.set_option('max_colwidth', 160)

    cur = conn.cursor()
    cur.execute(settings.QUERY_SUMMARIZE_API_RESULTS)
    df = pd.DataFrame(cur.fetchall(), columns=['API Service', 'Story Count'])

    return df.to_html()


def get_wallstreet_cn(conn, run_id, list_of_urls, ticker):
    '''Get Yicai stories and write to database'''
    url = 'https://api-prod.wallstreetcn.com/apiv1/search/article?order_type=time&cursor=&limit=20&search_id=&query={}'.format(ticker)
    res = requests.get(url)
    data = res.json()['data']['items']
    cur = conn.cursor()

    for d in data:
        row = {
            'run_id' : run_id,
            'uuid': str(uuid.uuid4()),
            'date_story': datetime.datetime.fromtimestamp(int(d['display_time'])),
            'source' : 'WallstreetCN',
            'title' : re.sub('<[^<]+?>', '', d['title']),
            'url' : d['uri'],
        }

        if row['url'] not in list_of_urls:
            try:
                cur.execute(settings.QUERY_INSERT, row)
                conn.commit()
            except Exception as e:
                print e
                print row['url']
                conn.rollback()
        else:
            print 'We already have this: ' + row['url']



def get_21jingji(conn, run_id, list_of_urls, ticker):
    '''Get Yicai stories and write to database'''
    url = 'http://www.21jingji.com/dynamic/content/search/index/{}/1'.format(ticker)
    res = requests.get(url)
    data = res.json()
    cur = conn.cursor()

    for d in data:
        row = {
            'run_id' : run_id,
            'uuid': str(uuid.uuid4()),
            'date_story': datetime.datetime.fromtimestamp(int(d['inputtime'])),
            'source' : '21 Jingji',
            'title' : re.sub('<[^<]+?>', '', d['title']),
            'url' : d['url'],
        }

        if row['url'] not in list_of_urls:
            try:
                cur.execute(settings.QUERY_INSERT, row)
                conn.commit()
            except Exception as e:
                print e
                print row['url']
                conn.rollback()
        else:
            print 'We already have this: ' + row['url']
