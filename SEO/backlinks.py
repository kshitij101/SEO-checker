import urllib.request
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re 
from selenium import webdriver
from tqdm import tqdm
import time

query = "eve v review"
owned_domain = 'eve-tech.com'

exclude_urls = ['forums', 'forum', 'comment', 'comments', 'wikipedia',
                'youtube', 'facebook', 'instagram', 'pinterest', 'ebay',
                'tripadvisor', 'reddit', 'twitter', 'flickr', 'amazon', 'etsy',
                'dailymotion', 'linkedin', 'google', 'aliexpress']

for exclude in exclude_urls:
    query = query # + " -inurl:" + exclude

import urllib
query = urllib.parse.quote_plus(query)

number_result = 20 # You may define more, but it will take longer

ua = UserAgent()
links = []

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = { 'User-Agent' : user_agent }

google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
req = urllib.request.Request(google_url,None, headers)
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, "html.parser")
for result_div in soup.find_all('div', attrs = {'class': 'r'}):
	link = result_div.find('a',href=True)
	links.append(link.get("href"))

#print(links)
backlinks = []
for url in links:
	req = urllib.request.Request(url,None, headers)
	html = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(html, "html.parser")
	for link in soup.find_all('a',href=True):
		if(owned_domain in link.get('href')):
			backlinks.append(link)

print("Number of Backlinks:{}".format(len(backlinks)))
'''

'''