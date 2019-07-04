import threading
from Queue import Queue

import requests
from bs4 import SoupStrainer, BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class ThreadCrawler:

    def __init__(self, input_url, max_threads):
        self.wait_queue = Queue()
        self.initial_url = input_url
        self.max_threads = max_threads
        self.thread_executor = ThreadPoolExecutor(max_workers = self.max_threads)
        self.crawled_pages = set()
        self.enqueue(self.initial_url)
        self.print_lock = threading.Lock()

    def enqueue(self, url):
        self.wait_queue.put(url)

    def dequeue(self):
        return self.wait_queue.get()

    def scrap(self, url):
        res = requests.get(url)

        base_page = res.text
        only_a_tags = SoupStrainer('a')  # Filter and get only the anchor tags

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(base_page, "html.parser", parse_only=only_a_tags)

        temp_set = set()

        # Iterate over the filtered tags (only anchors)
        for anchors in soup:
            if anchors.has_attr('href') and anchors['href'].startswith('http'):
                if anchors['href'] not in temp_set:
                    temp_set.add(anchors['href'])
                    self.enqueue(anchors['href'])
        print(url)

        for i in temp_set:
            print('\t' + i)


    def crawl(self):
        cur_url = self.dequeue()
        if cur_url not in self.crawled_pages:
            self.crawled_pages.add(cur_url)
            task = self.thread_executor.submit(self.scrap(cur_url))
            