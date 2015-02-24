#!/usr/bin/python

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getDeals import getDeals
from byteify import byteify
import datetime
import urllib2
import re
import json
import os.path
import smtplib


DAYS_TO_KEEP = 5 # How long to keep deals in deals_data file
VOTE_DIFF = 5 # Number of change in votes required to include deal in the email
THRESHOLD = 50 # Any deal with votes above the threshold will be included in the email
SENDER = "you@email.com"
RECIPIENTS = ["hello@email.com", "world@email.com"]
USERNAME = "you@email.com"
PASSWORD = "your password"
FILE_DIR = "/your/working/directory/here/deals_data"
URLS = []
URLS.append("http://ozbargain.com.au/deals?page=0")
URLS.append("http://ozbargain.com.au/deals?page=1")
URLS.append("http://ozbargain.com.au/deals?page=2")
URLS.append("http://ozbargain.com.au/deals?page=3")
URLS.append("http://ozbargain.com.au/deals?page=4")


newDeals = getDeals(URLS)
newDeals = byteify(newDeals)
print newDeals

if os.path.isfile(FILE_DIR):
	f = open(FILE_DIR, 'r')
	oldDeals = json.load(f)
	f.close()
	oldDeals = byteify(oldDeals)
	mailContent = ""
	htmlContent = ""
	for id in newDeals:
		if id in oldDeals:
			print "Votes: ", oldDeals[id]['votes'], "->", newDeals[id]['votes']
			if ((int(newDeals[id]['votes']) - int(oldDeals[id]['votes']) >= VOTE_DIFF) or int(newDeals[id]['votes']) >= THRESHOLD) and (str(oldDeals[id]['emailed']) == 'False'):
				print "#####################################"
				print "ID: ", id
				print "Votes: ", oldDeals[id]['votes'], "->", newDeals[id]['votes']
				print "Added to mailContent"
				print "#####################################"
				oldDeals[id]['emailed'] = 'True'
				mailContent += 'www.ozbargain.com.au/node/' + id + '\n'
				htmlContent += '<p><a href="http://www.ozbargain.com.au/node/' + id + '">' + oldDeals[id]['title'] + '</a></p>\n'
			oldDeals[id]['votes'] = newDeals[id]['votes']

			# remove deals older than DAYS_TO_KEEP
			oldDate = datetime.datetime.strptime(oldDeals[id]['date'], '%Y-%m-%d')
			diff = datetime.date.today() - oldDate.date()
			print datetime.date.today(), " - ", oldDate.date(), " = ", diff.days
			if diff.days > DAYS_TO_KEEP:
				del oldDeals[id]
		else:
			details = {'votes': newDeals[id]['votes'], 'emailed': 'False', 'date': newDeals[id]['date'], 'title': newDeals[id]['title']}
			oldDeals[id] = details

	# send mail here
	if mailContent:
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Ozbargain Deals'
		msg['From'] = SENDER
		msg['To'] = ""
		html = "<html><head></head><body>" + htmlContent + "</body></html>"
		part1 = MIMEText(mailContent, 'plain')
		part2 = MIMEText(html, 'html')
		msg.attach(part1)
		msg.attach(part2)

		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(USERNAME, PASSWORD)
		server.sendmail(SENDER, RECIPIENTS, msg.as_string())
		server.quit()
		print "Email successfully sent to", ", ".join(RECIPIENTS)
				
	f = open(FILE_DIR, 'w')
	json.dump(oldDeals, f)
	f.close()

else:
	f = open(FILE_DIR, 'w')
	json.dump(newDeals, f)
	f.close()
	

