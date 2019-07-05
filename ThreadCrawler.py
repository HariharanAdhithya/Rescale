import threading
from Queue import Empty
from multiprocessing import Queue

import requests
from bs4 import SoupStrainer, BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED


class ThreadCrawler:

    def __init__(self, input_url, max_threads):
        self.wait_queue = []
        self.initial_url = input_url
        self.max_threads = max_threads
        self.thread_executor = ThreadPoolExecutor(max_workers = 20)
        self.crawled_pages = set()
        self.wait_queue.append(self.initial_url)
        self.print_lock = threading.Lock()


    def scrape_info(self, url):
        res = requests.get(url, timeout=(3, 30))
        html = res.text

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html, "html.parser")
        href_links = soup.find_all('a', href=True)
        temp_set = set()
        # Iterate over the filtered tags (only anchors)
        for anchors in href_links:
            if anchors['href'].startswith('http') and anchors['href'] not in self.crawled_pages:
                    temp_set.add(anchors['href'])
                    self.wait_queue.append(anchors['href'])

        self.print_lock.acquire()
        print (url)
        for i in temp_set:
            print('\t' + i)
        self.print_lock.release()

        if len(self.wait_queue) != 0:
            while self.wait_queue:
                cur_url = self.wait_queue.pop(0)
                if cur_url not in self.crawled_pages:
                    self.crawled_pages.add(cur_url)
                    self.thread_executor.submit(self.scrape_info, cur_url)


    def crawl(self):
        try:
            cur_url = self.wait_queue.pop(0)
            if cur_url not in self.crawled_pages:
                self.crawled_pages.add(cur_url)
                self.thread_executor.submit(self.scrape_info, cur_url)
        except Empty:
            return
        except Exception as e:
            print(e)
