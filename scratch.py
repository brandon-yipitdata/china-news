import requests
import pandas as pd
import send_me_email
import web

ft = web.get_ft_stories().head().to_html(index = False)
xinhua = web.get_xinhua_news().to_html(index = False)
yicai = web.get_yicai().to_html(index = False)
reuters = web.get_reuters_china().to_html(index = False)

subject = "China Hourly Roundup"
message = u'FT:\n{}\n\nReuters:\n{}\n\nXinhua:\n{}\n\nYicai:\n{}'.format(ft,reuters,xinhua,yicai)
recipients = ['bemmerich@Yipitdata.com','emailbot4data@gmail.com']


for recipient in recipients:
    print recipient
    send_me_email.send_html_email_3(message, recipient, subject)
