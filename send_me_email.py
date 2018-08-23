# -*- coding: utf-8 -*-
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib


def send_html_email(html, recipient, subject):
	"""This function sends an HTML email from my personal email"""

	fromaddress = 'emailbot4data@gmail.com'

	message = MIMEMultipart("alternative", None, [MIMEText(html,'html','utf-8')])
	message['From'] = fromaddress
	message['Subject'] = subject

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddress, 'phmtwvkyhbptfejf')
	text = message.as_string()
	server.sendmail(fromaddress, recipient, text)
	server.quit()
