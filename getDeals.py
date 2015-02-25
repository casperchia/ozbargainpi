from bs4 import BeautifulSoup
import urllib2
import datetime
import re

# returns a dict of deals collected from ozbargain.
# deals = {'id': {'votes': int, 'emailed': bool, 'date': date, 'title': str}}
def getDeals(urls):
	deals = {}
	
	for url in urls:
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html.read())
		
		for index, deal in enumerate(soup.find_all(class_="node-ozbdeal")):
			print "######"
			print "#", index
			print "######"

			# print votes
			votes = deal.div.div.span.span.string
			print "Votes:", votes 

			# print deal id
			titleStr = deal.find(class_="title").a.encode('utf-8')
			title = deal.find(class_="title").a.get_text().encode('utf-8')
			regex = re.search('.*node/(\d+)', titleStr)
			deal_id = regex.group(1)
			print "Deal ID:", deal_id
			print title
			print ""

			details = {'votes': votes, 'emailed': 'False', 'date': str(datetime.date.today()), 'title': title}
			deals[deal_id] = details

	return deals	
