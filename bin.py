#! /anaconda2/bin/python
# -*- coding: utf-8 -*-

import send_me_email
import web

ft = web.get_ft_stories().head().to_html(index = False)
xinhua = web.get_xinhua_news().to_html(index = False)
yicai = web.get_yicai().to_html(index = False)
reuters = web.get_reuters_china().to_html(index = False)
caixin = web.get_caixin().to_html(index = False)

subject = "China Hourly Roundup"
message = u'FT:\n{}\n\nReuters:\n{}\n\nCaixin Business & Tech:\n{}\n\nXinhua:\n{}\n\nYicai:\n{}'.format(ft,reuters,caixin,xinhua,yicai)
recipients = ['bemmerich@Yipitdata.com','jyoo@yipitdata.com']


for recipient in recipients:
    print recipient
    send_me_email.send_html_email(message, recipient, subject)
