from Queue import Queue, Empty
import threading
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class ThreadCrawler:

    def __init__(self, max_threads):
        self.wait_queue = Queue()
        self.thread_executor = ThreadPoolExecutor(max_workers = max_threads)
        self.crawled_pages = set()
        self.check_lock = threading.Lock()

    def scrape_links(self, url, html):
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html, "html.parser")
        href_links = soup.find_all('a', href=True)

        with self.check_lock:
            print (url)
            for anchors in href_links:
                if anchors['href'].startswith('http'):
                    if anchors['href'] not in self.crawled_pages:
                        self.wait_queue.put(anchors['href'])
                        self.crawled_pages.add(anchors['href'])
                    print('\t' + anchors['href'])


        while not self.wait_queue.empty():
            cur_url = self.wait_queue.get()
            self.thread_executor.submit(self.get_page, cur_url)

    def get_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 30))
        except requests.RequestException as e:
            print(e)
            return

        if res and res.status_code == 200:
            self.scrape_links(url, res.text)



    def crawl(self, initial_url):
        try:
            self.crawled_pages.add(initial_url)
            self.thread_executor.submit(self.get_page, initial_url)
        except Empty:
            print('Queue is empty')
            return
        except Exception as e:
            print(e)
