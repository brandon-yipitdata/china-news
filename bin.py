# -*- coding: utf-8 -*-
import private
import psycopg2
import time
import web

conn = psycopg2.connect(private.DB_CONNECTION_STRING)
run_id = int(time.time())

list_of_urls = web.get_urls(conn)

web.get_yicai(conn, run_id, list_of_urls)
web.get_xinhua(conn, run_id, list_of_urls)
web.get_reuters_china(conn, run_id, list_of_urls)
web.get_caixin(conn,run_id,list_of_urls)

the_news = web.get_the_news(conn)

subject = "China News Roundup"
recipients = private.EMAIL_RECIPIENTS
email_body = u'The News:\n\n\n{}\n\n\nLove,\nYour China Email Bot'.format(the_news.to_html())

for recipient in recipients:
    print recipient
    web.send_html_email(email_body, recipient, subject)
