#! /anaconda2/bin/python
# -*- coding: utf-8 -*-

import demjson
from lxml import etree
import pandas as pd
import requests
import send_me_email

pd.set_option('max_colwidth', 160)

def get_xinhua_news():
    """Access Xinhua News API to get stories"""
    url = 'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=5&tp=1&orderby=1'
    res = requests.get(url)
    raw_json = demjson.decode(res.content[1:-2])

    df = pd.DataFrame(raw_json['data']['list'])
    df_to_send = df[['Title','LinkUrl']]

    return df_to_send

def get_ft_stories():
    """Get's most recent FT stories on China"""
    url = 'https://www.ft.com/world/asia-pacific/china'
    response = requests.get(url)
    root = etree.HTML(response.content)

    heading = root.xpath("//a[@class='js-teaser-heading-link']/text()")
    urls = root.xpath("//a[@class='js-teaser-heading-link']/@href")

    df = pd.DataFrame()
    df['news_title'] = heading
    df['url'] = urls

    df['url'] = 'https://www.ft.com' + df['url']
    df['news_title'] = df['news_title'].str.strip()

    return df

def get_yicai():
    """Get stories from Yicai"""
    url = 'https://www.yicai.com/api/ajax/getjuhelist?action=news&page=1&pagesize=5'
    res = requests.get(url)
    df = pd.DataFrame(res.json())
    df['url'] = 'https://www.yicai.com' + df['url']

    df_to_send = df[['NewsTitle','url']]

    return df_to_send

def get_reuters_china():
    """Get Reuters stories from the China feed"""

    url = 'https://wireapi.reuters.com/v7/feed/rapp/us/tabbar/feeds/china'
    res = requests.get(url)

    stories = len(res.json()['wireitems'])
    empty_list = []

    for i in range(stories):
        try:
            _dict = res.json()['wireitems'][i]['templates'][1]['story']
            _dict['url'] = res.json()['wireitems'][i]['templates'][2]['template_action']['url']
            empty_list.append(_dict)

        except:
            continue

    df = pd.DataFrame(empty_list)
    df = df[['hed','url']].head()
    return df
