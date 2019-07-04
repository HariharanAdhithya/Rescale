import urllib2
import requests
from bs4 import SoupStrainer
from bs4 import BeautifulSoup

# specify the url
base_url = "http://www.rescale.com/"

# base_page = urllib2.urlopen(base_url)

res = requests.get(base_url)

base_page = res.text
only_a_tags = SoupStrainer('a')   # Filter and get only the anchor tags

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(base_page, "html.parser", parse_only=only_a_tags)

# Iterate over the filtered tags (only anchors)
for anchors in soup:
    if anchors.has_attr('href') and anchors['href'].startswith('http'):
        print(anchors['href'])
