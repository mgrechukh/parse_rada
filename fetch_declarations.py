#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import urllib2, sys, re
from BeautifulSoup import BeautifulSoup

full_list_url = 'http://w1.c1.rada.gov.ua/pls/site2/fetch_mps?skl_id=9'
info_page_prefix = 'http://itd.rada.gov.ua/mps/info/page'

decl_page_pattern = "http://itd.rada.gov.ua/declview/Home/Main/%s/%s" # % dep_id, year

def soupize(url):
	page = urllib2.urlopen(url)
	return BeautifulSoup(page)

def read_deps(url_list):
	soup = soupize(url_list)
	print "-- parsing titles", name
	for p in soup.findAll(name = 'p', attrs = {'class': 'title'}):
  		a = p.find('a')

		if not a.get('href').startswith(info_page_prefix):
			print 'Bad link format', a.get('href'), a.text
			continue

		dep_id = a.get('href').split('/')[-1]
		dep_name = a.text
		yield (dep_name, dep_id)


def read_decl(dep_id, year = 2015):
	decl_page_url = decl_page_pattern % (dep_id, year)
	#page = urllib2.urlopen(decl_page_url)
	#with open("decl-%s.txt" % dep_id, 'w') as f:
	#	f.write(page.read())
	soup = soupize(decl_page_url)
	heritage = soup.find('td', text = "спадщина".decode('utf-8'))
	if heritage:
		amounts = heritage.parent.parent.findAll('td', {'style': 'text-align: center'})
		own = amounts[0].text.strip() or 0 # look on html
		fam = amounts[1].text.strip() or 0
		return (own, fam, decl_page_url)
	else:
		return 0, 0, decl_page_url

def decl_out(personal, heritage):
		print "%s (%s)|" % personal, "own: %s, family: %s |src %s" % (heritage)

deps = []
if sys.argv[1:]:
	name = sys.argv[1].decode('utf-8')
	for x in read_deps(full_list_url):
		if x[0].find(name) > -1:
			decl_out(x, read_decl(x[1]))

else:
	print "-- fetching list"
	for x in read_deps(full_list_url):
		got_legacy = read_decl(x[1])
		if got_legacy and filter(bool, got_legacy[:2]):
			decl_out(x, got_legacy)

