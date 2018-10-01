# -*- coding: utf-8 -*-
import private
import psycopg2
import settings
import time
import web

# Setup ------------------------------------------------------------------------
conn = psycopg2.connect(private.DB_CONNECTION_STRING)
run_id = int(time.time())

list_of_urls = web.get_urls(conn, settings.QUERY_GET_NEWS_URLS)

# Get the news -----------------------------------------------------------------
try:
    web.get_yicai(conn, run_id, list_of_urls)
except Exception as e:
    print e

try:
    web.get_xinhua(conn, run_id, list_of_urls)
except Exception as e:
    print e

try:
    web.get_reuters_china(conn, run_id, list_of_urls)
except Exception as e:
    print e

try:
    web.get_caixin(conn,run_id,list_of_urls)
except Exception as e:
    print e


# Send Report ------------------------------------------------------------------

the_news = web.get_the_news(conn)

subject = "China News Roundup"
recipients = private.EMAIL_RECIPIENTS
email_body = u'The News:\n\n\n{}\n\n\nLove,\nYour China Email Bot'.format(the_news.to_html())

for recipient in recipients:
    print recipient
    web.send_html_email(email_body, recipient, subject)

# Tonghuashun ------------------------------------------------------------------

list_of_urls_tonghuashun = web.get_urls(conn, private.QUERY_TONGHUASHUN_GET_URLS)

list_of_tickers = settings.LIST_TICKERS

for ticker in list_of_tickers:
    try:
        web.get_tonghuashun(ticker, conn, run_id, list_of_urls_tonghuashun)
    except Exception as e:
        print ticker + e
