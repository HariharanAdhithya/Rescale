from Queue import Queue

from concurrent.futures import ThreadPoolExecutor


class ThreadCrawler:

    def __init__(self, input_url, max_threads):
        self.wait_queue = Queue()
        self.initial_url = input_url
        self.max_threads = max_threads
        self.threads = ThreadPoolExecutor(max_workers = self.max_threads)
        self.crawled_pages = set()
        self.enqueue(self.initial_url)

    def enqueue(self, url):
        self.wait_queue.put(url)

    def dequeue(self):
        return self.wait_queue.get()

