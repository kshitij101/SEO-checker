import sys
import urllib
import urllib.request
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import json
import os
import subprocess
import requests
import socket
from urllib.parse import urlencode
import time
import lxml
from lxml import html
from lxml.html.clean import clean_html
from lxml.html.clean import Cleaner
from urllib.request import Request, urlopen
import geoip2.database
import time
from urllib.error import URLError, HTTPError
from hurry.filesize import size
#import pythonwhois
def linkchecker():
	quality = 0
	mainurl = "https://moz.com"
	locations = []
	broken_links = []
	internal_links = set()
	req = Request(mainurl+"/"+"sitemap_index.xml", headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	#r = requests.get(mainurl+"/"+"blog-sitemap.xml", timeout = 20)
	# xml = r.text
	soup = BeautifulSoup(webpage,'lxml')
	sitemap = soup.find("sitemap")
	for locs in sitemap.find_all("loc"):
		sitemap_loc = locs.text
	r = requests.get(sitemap_loc, timeout = 20)
	xml = r.text
	soup = BeautifulSoup(xml,'lxml')
	locations = [locs.find("loc").text for locs in soup.find_all("url")]
	for line in locations[:30]: #THIS TAKES U ALOT OF TIME. SO CUTTING THE LIST 
		req = Request(line, headers={'User-Agent': 'Mozilla/5.0'})
		page = urlopen(req)
		if((page.getcode() != 404) and (len(page.read()) > 0)):
			internal_links.add(line+' '+'DoFollow')

	page = Request(mainurl,headers={'User-Agent': 'Mozilla/5.0'})
	mainpage = urlopen(page).read()
	soup = BeautifulSoup(mainpage,"html.parser")
	re_internallinks = re.compile('^(#)|(\/)|(https)|(http)')
	for links in soup.find_all('a',href=True):
		if(re.match(re_internallinks,links.get('href')) and (len(links.get('href')) > 1)):
			if(links.get('rel') != 'nofollow'):
				internal_links.add(links.get('href')+' '+'DoFollow')
			else:
				internal_links.add(links.get('href')+' '+'NoFollow')

	return internal_links
def charenc(mainurl):
	resp = requests.get(mainurl)
	if(resp.headers['content-type'] is not None):	
		quality = 1
		print("Character Encoding Provided:{} ".format(str(resp.headers['content-type']).split(';',1)[1].split('=',1)[1]))
		return quality
	else:
		quality = -1
		print("Character Encoding is not Provided:")
		return quality
def HTML5check(page):
	page = str(page).lstrip('\n')
	page = str(page).lstrip(' ')
	re_HTML5 = re.compile('^<!DOCTYPE')
	if(re.match(re_HTML5,str(page))):
		quality = 1
		print("HTML 5 Compliant")
		return quality
	else:
		quality = -1
		print("HTML 5 not Compliant")
		return quality
def serverip(mainurl):
	server_info = []
	page = Request(mainurl,headers={'User-Agent': 'Mozilla/5.0'})
	mainpage = urlopen(page)
	server_info.append("Server: {}".format(mainpage.headers['server']))
	regex  = re.compile("^https://")
	regex1 = re.compile("^http://")
	if(regex.search(mainurl)):
		url = mainurl[8:]
	elif(regex1.search(mainurl)):
		url = mainurl[7:]
	else:
		url = mainurl
	ip_site = socket.gethostbyname(url)
	server_info.append("IP address: {}".format(ip_site))
	reader = geoip2.database.Reader('GeoLite2-City.mmdb')
	response = reader.city(ip_site)
	city = response.location.time_zone
	server_info.append("Location: {}".format(city))
	print("Server Info: {}".format(server_info))
	return server_info
def embeddobj(page):
	embed = page.find('embed',src=True)
	obj = page.find('object',data=True,hidden=False)
	if((embed is not None) and (obj is not None)):
		quality = 1
		print("No embedded objects:")
		return quality
	else:
		quality = -1
		print("Page contains embedded objects")
		return quality
def mobilfr(page):
	meta = page.find('meta',attrs={'name':'viewport','content':['width=device-width','initial-scale=1']})
	if(meta is not None):
		quality = 1
		print("Page is Mobile Friendly")
		return quality
	else:
		quality = -1
		print("Page is not Mobile Friendly")
def pgsec(mainurl):
	returncode = requests.get(mainurl)
	if("https://" in returncode.url):
		print("Site is Secure")
		quality = 1
		return quality
	else:
		print("Site is not Secure")
		quality = -1
		return quality
def emailpr(page):
	number_list = []
	email_list = []
	number_list = re.findall(r"\+\d{2}\s?0?\d{10}",str(page))
	email_list = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",str(page))
	#print(number_list,email_list)
	if(len(email_list) > 0):
		print("Email privacy not maintained")
		quality = -1
		return quality
	else:
		print("Email privacy is maintained")
		quality = 1
		return quality
def sitelang(page,mainurl):
	page_language=""
	page_lang =  page.find('html',lang=True)
	page_language = page_lang.get('lang')
	if(page_language == ""):
		meta = page.find('meta',attrs={"http-equiv":"content-language"})
		page_language = meta.get("content")
	if(page_language == ""):
		mainpage = Request(mainurl,headers={'User-Agent': 'Mozilla/5.0'})
		page = urllopen(mainpage)
		if(page.info().get('Content-Language') is not None):
			page_language = page.info().get('Content-Language')
			print("Language Supported is specified {}".format(page_language))
			quality = 1
			return quality
		else:	
			print("Language Supported not specified")
			quality =  -1
			return quality
	else:
		print("Language Supported is specified: {}".format(page_language))
		quality = 1
		return quality
def googleinsight(mainurl):
	key = "AIzaSyADaZIzi5xTwOHVbwTFXdOMERSxdOhD4Z8"
	google_url = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url="+mainurl+"/&strategy=mobile&key="+key
	page = requests.get(google_url)
	page_insights = json.loads(page.text)
	print("Page Insights Score:{}".format(page_insights["ruleGroups"]["SPEED"]["score"]))
def pagesize(mainurl):
	page = Request(mainurl,headers={'User-Agent': 'Mozilla/5.0'})
	mainpage = urlopen(page)
	page_size = mainpage.info()['content-length']
	if(page_size is not None):
		print("Size of the Page is:{}".format(size(int(page_size))))
	else:
		print("Size of the Page not available")
	start = time.time()
	page = urllib.request.urlopen(mainurl)
	page_load = page.read()
	finsih = time.time()
	page_load_time = finsih-start
	print("Page Load Time:%.2f" % page_load_time+" seconds")
def favicon(page):
	rellink = ["shortcut","icon"]
	favicon = page.find('link',rel=rellink)#not accepting shortcut
	if(favicon.get('href') is not None):
		quality = 1	
		print("Your website has a favicon")
	else:
		quality = -1
		print("Your website doesn't have a FavIcon")
def pageindex(mainurl):
	num_nonindexed_pages = 0
	locations = []
	r = requests.get(mainurl+"/"+"sitemap_index.xml")
	#r = requests.get(mainurl+"/"+"blog-sitemap.xml", timeout = 20)
	xml = r.text
	soup = BeautifulSoup(xml,'lxml')
	sitemap = soup.find("sitemap")
	for locs in sitemap.find_all("loc"):
		sitemap_loc = locs.text
	r = requests.get(sitemap_loc, timeout = 20)
	xml = r.text
	soup = BeautifulSoup(xml,'lxml')
	locations = [locs.find("loc").text for locs in soup.find_all("url")]
	for line in locations[:30]: #THIS TAKES U ALOT OF TIME. SO CUTTING THE LIST 
	    query = {'q': 'info:' + line}
	    google = "https://www.google.com/search?" + urlencode(query)
	    data = requests.get(google)
	    data.encoding = 'ISO-8859-1'
	    soup = BeautifulSoup(str(data.content), "html.parser") 
	    try:
	        check = soup.find(id="rso").find("div").find("div").find("h3").find("a")
	        href = check['href']
	    except AttributeError:
	    	num_nonindexed_pages += 1
	print("Number of Pages Indexed:{}".format(len(locations)-num_nonindexed_pages))
	return len(locations)-num_nonindexed_pages
	
def iframes(page):
	num_iframes = page.find_all('iframe')
	if(len(num_iframes) > 0):
		quality = -1
		print("Your Page contains:{} iframes".format(len(num_iframes)))
		return quality
	else:
		quality = 1
		print("Your Page doesnt contain iframes")
		return quality
	  
def robot(mainurl):
	req = Request(mainurl+"robots.txt", headers={'User-Agent': 'Mozilla/5.0'})
	try:
		xml = urlopen(req).read()
	except URLError as e:
		quality = -1
		print("Robot.txt file doesnt exists")
		return quality
	if("User-agent:" in xml):
		quality = 1
		print("Robot.txt file exists")
		return quality
	else:
		quality =  -1
		print("Robot.txt file doesnt exists")
		return quality
def sitemap(mainurl):
	locations = []
	req = Request(mainurl+"/"+"sitemap_index.xml", headers={'User-Agent': 'Mozilla/5.0'})
	try:
		webpage = urlopen(req).read()
	except URLError as e:
		quality = -1
		print("Your Site doesnt have a XML SiteMap")
		return quality
	soup = BeautifulSoup(webpage,'lxml')
	sitemapTags = soup.find("sitemap").contents
	regex = re.compile('^<loc>')
	for locs in sitemapTags:
		if(regex.match(str(locs))):
			locations.append(locs)
	if(len(locations) > 0):
		quality = 1
		print("Your Site has a SiteMap")
		return quality
	else:
		quality = -1	
		print("Your Site dosent have a SiteMap")
		return quality
def wwwresolve(mainurl):
	returncode = requests.get(mainurl)
	# returncode.url
	if(len(returncode.history) != 0): 
		if((str(returncode.history[0]) == '<Response [301]>') or (str(returncode.history[0]) == '<Response [302]>')):
			quality = 1
			print("Redirection is in place to your domain")
			return quality
		else:
			quality = -1
			print("Redirection is not in place to your domain")
			return quality
	else:
		quality = -1
		print("Redirection is not in place to your domain")
		return quality
def underurl(mainurl):
	num_under = mainurl.count('_')
	if(num_under > 0):
		quality = -1
		print("Your URL has UNDERSOCRES: {}".format(num_under))
		return quality
	else:
		quality = 1
		print("Your URL doesnt have UNDERSOCRES:")
		return quality
def gzip(mainurl):
	res = requests.head(mainurl)
	if(res.headers['Content-Encoding'] == "gzip"):
		quality = 1
		print("Gzip encoding enabled")
		return quality
	else:
		quality = -1
		print("Gzip encoding is not enabled")
		return quality
def txt2html(page):
	size_HTML = int(sys.getsizeof(page))
	cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)
	cleaned_text = cleaner.clean_html(str(page))
	size_text = int(sys.getsizeof(cleaned_text))
	print("Ratio of Text to HTML:{}".format((size_HTML/size_text)*100))
	return (size_HTML/size_text)*100
def altimg(page):
	num_alt = 0
	for alt in page.find_all('img'):
		if(alt.has_attr('alt') == 0):
			num_alt += 1
			print("Number of img tags without alt: {}".format(num_alt))
			return num_alt
		elif(len(alt.get('alt')) < 2):
			num_alt += 1
			print("Number of img tags without alt: {}".format(num_alt))
			return num_alt
		else:
			print("No img tag without alt")
			return num_alt
def headerquality(page):
	h1_count = 0
	quality = 0
	title = page.find('title')
	for header in page.find_all('h1'):
		h1_count += 1
		if(header.text == title.text):
			quality -= 1
		else:
			quality += 1
		if(h1_count == 1):
			quality += 1
		else:
			quality -= 1
		if((len(header.text) > 20) and (len(header.text) < 70)):
			quality += 1
			header_text = header.text
		else:
			quality -= 1
			header_text = header.text
	header_count = [0,0,0,0,0,0]
	header_count[0] = h1_count
	for h2 in page.find_all('h2'):
		header_count[1] += 1	
	for h3 in page.find_all('h3'):
		header_count[2] += 1	
	for h4 in page.find_all('h4'):
		header_count[3] += 1	
	for h5 in page.find_all('h5'):
		header_count[4] += 1	
	for h6 in page.find_all('h6'):
		header_count[5] += 1

	print(header_count)
	return quality

def metakey(page):
	num_key = []
	for meta in page.find_all('meta',attrs={'name':'keywords'}):
		num_key = meta.get('content').split(',')
	print("Number of keywords: {} ".format(len(num_key))) 
def metadesc(page):
	quality = 0
	flag = 0
	num_desc = 0
	for meta in page.find_all('meta',attrs={'name':'description'}):
		num_desc += 1
		meta_content = meta.get('content')
		meta_content_len = len(meta_content)
		if(meta_content_len == 0):
			quality -= 1
			flag = 0
		else:
			flag = 1
		if(meta_content_len < 200 and meta_content_len > 100):
			quality += 1
			flag = 1
	if(num_desc > 5):
		quality -= 1
	if(flag == 1):
		print("Your site has Meta Description")
	else:
		print("Your site doesnt have Meta Description")
	return quality	
def title(page):
	quality = 0
	title = page.find('title').text
	if(len(title) == 0):
		quality == -1
	if(quality != -1):
		if(len(title) < 60):
			quality += 1
			if(len(title) > 30):
				quality += 1

		num_occurence = 0
		num_occurence_sub = 0

		num_occurence = title.count(title)

		for sub in title.split(" "):
			num_occurence_sub += title.count(sub)

		if((num_occurence > 1) or (num_occurence_sub > len(title))):
			quality -= 1

	print("Number of characters in your title {}".format(len(title)))
	return quality
	'''
mainurl = "http://www.basicwebsiteexample.com/404"
try:
	page = urllib.request.urlopen(mainurl)
except urllib.error.HTTPError as URLerror:
	if(URLerror.code == 404):
		print("404")

soup = BeautifulSoup(,"html.parser")
print(soup)
'''
'''
mainurl = "http://www.basicwebsiteexample.com/media"
try:
	page = urllib.request.urlopen(mainurl)    
except (http.client.IncompleteRead) as e:
    page = e.partial

soup = BeautifulSoup(page,"html.parser")
'''
'''
regex  = re.compile("^https://")
regex1 = re.compile("^http://")
if(regex.search(mainurl)):
	cmd = "whois"+" "+mainurl[8:]
elif(regex1.search(mainurl)):
	cmd = "whois"+" "+mainurl[7:]
else:
	cmd = "whois"+" "+mainurl
result = subprocess.check_output(cmd,shell=True)
print(result)
'''

