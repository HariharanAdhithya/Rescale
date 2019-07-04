from ThreadCrawler import ThreadCrawler

base_url = "http://www.rescale.com/"

job = ThreadCrawler(base_url, 100)

job.crawl()