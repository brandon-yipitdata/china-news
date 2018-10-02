# -*- coding: utf-8 -*-
import private
import psycopg2
import settings
import time
import web

# Setup ------------------------------------------------------------------------
run_id = int(time.time())
conn = psycopg2.connect(private.DB_CONNECTION_STRING)

list_of_urls = web.get_urls(conn, settings.QUERY_GET_NEWS_URLS)

# Get the news -----------------------------------------------------------------
try:
    web.get_yicai(conn, run_id, list_of_urls)
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

list_tuples_org_and_ticker = settings.LIST_ORGANIZATIONS_CHINESE
list_of_organizations_chinese = [tuple_[0] for tuple_ in list_tuples_org_and_ticker]

[web.get_wallstreet_cn(conn, run_id, list_of_urls, org_name_chinese) for org_name_chinese in list_of_organizations_chinese]
[web.get_21jingji(conn, run_id, list_of_urls, org_name_chinese) for org_name_chinese in list_of_organizations_chinese]

# Send Report ------------------------------------------------------------------

the_news = web.get_the_news(conn)
subject = "China News Roundup"
recipients = private.EMAIL_TEST_RECIPIENTS

if run_id == web.get_max_run_id(conn):
    email_body = u'The News:\n\n\n{}\n\n\nLove,\nYour China Email Bot'.format(the_news.to_html())
else:
    email_body = u'No new news this run. See you next time!\nLove,\nYour China Email Bot'

for recipient in recipients:
    print recipient
    web.send_html_email(email_body, recipient, subject)

conn.close()
