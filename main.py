from ThreadCrawler import ThreadCrawler


# base_url = "http://triplebyte.github.io/web-crawler-test-site/already-passing-tests/"
base_url = "http://www.rescale.com/"

job = ThreadCrawler(base_url, 100)

job.crawl()