# coding=utf-8
import unicodedata
import os
import sys
import urllib
import urllib2
import urlparse
import argparse
import BeautifulSoup


proxy_support = urllib2.ProxyHandler({"http":"http://10.10.78.62:3128"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

def not_combining(char):
        return unicodedata.category(char) != 'Mn'

def strip_accents(text, encoding):
        unicode_text= unicodedata.normalize('NFD', text.decode(encoding))
        return filter(not_combining, unicode_text).encode(encoding)

list_name = []

def main(url, out_folder):
    #fortunef = open("fortune_companies.txt", "w")
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
    c =1	
    for span in soup.findAll("span"):
	if span['class'] == 'name listCol2':
		# we need to first remove accents like french/german companies names have a bar on e or o etc.
		temp = span.text.encode("utf8")
		#print str(c)+" " + temp	
		coname = strip_accents(temp, "utf-8")
		list_name.append(coname)
		#fortunef.write("%s\n"%coname)
		c=c+1
    #fortunef.close()		

def getlogo(base_url, out_folder):
    
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(base_url))
    c =0	
    for image in soup.findAll("img"):
        src = image['src']
	if 'brandsoftheworld' in src: 	
		alt = image['alt']
		#print alt[8:] started with 8 bcause first 7 character are 'LOGO OF '
		_, filename = os.path.split(urlparse.urlsplit(src).path)
		filename2, filext = os.path.splitext(filename)
		filename = alt[8:] + str(c) + filext 
		outpath = os.path.join(out_folder, filename)
	
		url = urlparse.urljoin(base_url, src)
		urllib.urlretrieve(url, outpath)
		c=c+1

if __name__ == "__main__":
    # following url is to crawl and get names of fortune 500 companies	
    url = 'http://money.cnn.com/magazines/fortune/fortune500/2013/full_list/index.html?iid=F500_sp_full' 
    # destination folder where logo will be saved
    out_folder = "getting_brand_logos/logos/"
    # main function get the names of all the companies
    main(url, out_folder)
    # following url is to crwal and and download logos
    url2 = 'http://www.brandsoftheworld.com/search/logo?search_api_views_fulltext='	
    for i in range(0,500):
	    print list_name[i]
	    furl = url2+list_name[i]			
	    # get logo for one particular brand	
	    getlogo(furl,out_folder)	
	
