import urllib2
from bs4 import SoupStrainer
from bs4 import BeautifulSoup

# specify the url
base_url = "http://www.rescale.com/"

base_page = urllib2.urlopen(base_url)


only_a_tags = SoupStrainer('a')   # Filter and get only the anchor tags

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(base_page, "html.parser", parse_only=only_a_tags)

# Iterate over the filtered tags (only anchors)
for anchors in soup:
    if anchors.has_attr('href'):
        print(anchors['href'])
