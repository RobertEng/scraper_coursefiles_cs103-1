#------------------------------------------------------------
# Scraper for CS 103 course files
#------------------------------------------------------------
# Grabs *.pdf files from the url specified by HOME_URL and
# puts them in the same directory that this file occupies.
# Preserves the original folder hierarchy by creating new
# directories as required.
#------------------------------------------------------------

import urllib2
import cookielib
import os
from bs4 import BeautifulSoup

# Website to scrape
HOME_URL = 'http://www.stanford.edu/class/cs103/'

# File extension to scrape
FILE_EXT = '.pdf'

# Request page content
home_req = urllib2.Request(HOME_URL)
home_content = urllib2.urlopen(home_req)

# Construct BeautifulSoup object of page content
soup = BeautifulSoup(home_content)


for link in soup.find_all('a'):
	candidate = str(link.get('href'))
	print candidate
	if (candidate[-len(FILE_EXT):] == FILE_EXT):
		file_url = HOME_URL + candidate
		file_url = file_url.replace(" ", "%20")
		# note above: can use urlencode to remove dangerous characters such as spaces
		
		# k = index of last "/" of the candidate => ...path/filename.pdf
		k = candidate.rfind("/")
		pathname = candidate[:k]
		filename = candidate[k+1:]

		# Open and save content of the file in pdf_read
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		pdf_req = urllib2.Request(file_url)
		pdf_content = opener.open(pdf_req)
		pdf_read = pdf_content.read()
		pdf_content.close()
		opener.close()

		# Create the path if not defined
		if not os.path.exists(pathname):
			os.makedirs(pathname)		
		
		# Write content of the file to the path
		pdf_write = open(candidate, 'wb')
		pdf_write.write(pdf_read)
		pdf_write.close()