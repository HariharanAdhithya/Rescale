from Queue import Queue, Empty
import threading
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class ThreadCrawler:

    def __init__(self, input_url, max_threads):
        self.wait_queue = Queue()
        self.initial_url = input_url
        self.thread_executor = ThreadPoolExecutor(max_workers = max_threads)
        self.crawled_pages = set()
        self.wait_queue.put(self.initial_url)
        self.check_lock = threading.Lock()


    def scrape_info(self, url):
        res = requests.get(url, timeout=(3, 30))
        html = res.text

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html, "html.parser")
        href_links = soup.find_all('a', href=True)
        # Iterate over the filtered tags (only anchors)

        self.check_lock.acquire()
        print (url)
        for anchors in href_links:
            if anchors['href'].startswith('http') and anchors['href'] not in self.crawled_pages:
                    self.wait_queue.put(anchors['href'])
                    self.crawled_pages.add(anchors['href'])
                    print('\t' + anchors['href'])
        self.check_lock.release()

        while not self.wait_queue.empty():
            cur_url = self.wait_queue.get()
            self.thread_executor.submit(self.scrape_info, cur_url)


    def crawl(self):
        try:
            cur_url = self.wait_queue.get()
            self.crawled_pages.add(cur_url)
            self.thread_executor.submit(self.scrape_info, cur_url)
        except Empty:
            return
        except Exception as e:
            print(e)
