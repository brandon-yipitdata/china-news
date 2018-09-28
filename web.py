# -*- coding: utf-8 -*-
import datetime
import demjson
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pandas as pd
import private
import smtplib
import psycopg2
import requests
import time
import uuid

pd.set_option('max_colwidth', 160)

def get_urls(conn):
    '''Query news database to find existing news urls'''
    cur = conn.cursor()
    cur.execute(private.GET_URLS_QUERY)
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
            cur.execute(private.INSERT_QUERY, row)
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
            cur.execute(private.INSERT_QUERY, row)
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
                cur.execute(private.INSERT_QUERY, row)
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
            cur.execute(private.INSERT_QUERY, row)
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
    cur.execute(private.GET_NEWS_QUERY)
    df = pd.DataFrame(cur.fetchall(), columns=['Source', 'Story', 'Url'])

    return df
