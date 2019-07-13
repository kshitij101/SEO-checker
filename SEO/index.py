import urllib
import urllib.request
from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup
import fucntions as fl

inpage_links = []

def get_webpage(mainurl):
	req = Request(mainurl,headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req).read()
	soup = BeautifulSoup(page,"html.parser")
	return soup

def features_call(mainurl):
	page = get_webpage(mainurl)

	title_quality = fl.title(page)
	meta_description = fl.metadesc(page)
	headers = fl.headerquality(page)
	num_alt = fl.altimg(page)
	txt_html_ration = fl.txt2html(page)
	gzip_encoding = fl.gzip(mainurl)
	num_urlunderscores = fl.underurl(mainurl)
	www_resolve = fl.wwwresolve(mainurl)
	xml_sitemap = fl.sitemap(mainurl)
	robots_file = fl.robot(mainurl)
	num_iframes = fl.iframes(page)
	num_pagesindexed = fl.pageindex(mainurl)
	favicon = fl.favicon(page)
	Page_load = fl.pagesize(mainurl)
	Google_Insights = fl.googleinsight(mainurl)
	website_language = fl.sitelang(page,mainurl)
	email_privacy = fl.emailpr(page)
	page_security = fl.pgsec(mainurl)
	mobile_friendly = fl.mobilfr(page)
	embedded_objects = fl.embeddobj(page)
	server_info = fl.serverip(mainurl)
	HTML5_compliant = fl.HTML5check(page) 
	character_encoding = fl.charenc(mainurl)

features_call("https://www.webstix.com")


