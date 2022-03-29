from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import queue
import threading
import requests
from bs4 import SoupStrainer, BeautifulSoup
from requests import  exceptions
from time import sleep

# TODO перекинуть общий список и base url в классы
Q = []
BASE_URL = 'https://google.com'


class Urls:
    def __init__(self, parent_url, work_url, depth) -> None:
        self.parent_url = parent_url
        self.work_url = work_url
        self.depth = depth
        self.child_urls = []
        self.status = False

class Pool:

    MAX_DEPTH = 2

    def __init__(self, max_workers, URL) -> None:
        self.workers = max_workers
        self.job = queue.SimpleQueue()
        self.job.put(URL)

    def _form_new_tasks(self, url_obj):
        if not url_obj.status:
            self.job.put(url_obj.work_url)
        else:
            for url in url_obj.child_urls:
                self.job.put(Urls(url_obj.work_url, url, url_obj.depth + 1))
                
    
    def run(self):
        for _ in range(self.MAX_DEPTH):     
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = []
                sentinel = object()
                for task in iter(self.job.get, sentinel):
                    
                    parser = Parser(task)
                    futures.append(executor.submit(parser.parse))
                    
                    if self.job.qsize() == 0:
                        break
                
                for future in concurrent.futures.as_completed(futures):
                    self._form_new_tasks(future.result())
                sleep(1)
            print('NEXT LEVEL')
        

        print(self.job.qsize())

class Parser:

    def __init__(self, url: object, name='thr') -> None:
        self.name = name
        self.url = url.work_url
        self.url_obj = url
        

    @staticmethod
    def _connect(url):
        print(url)
        while True:
            response = None
            try:
                response = requests.get(url=url, timeout=10, allow_redirects=True)
            except exceptions.ConnectionError:
                print('Ooops... Невозможно подключиться к {}'.format(url))
                sleep(15)
            except exceptions.TooManyRedirects:
                print('Ooops... Слишком много запросов от {}'.format(url))
                sleep(300)
            except exceptions.Timeout:
                print("Ooops.. превышено время ответа от {}".format(url))
                break
            except exceptions.MissingSchema:
                url = BASE_URL + url
            else:
                break
            
        return response 
        

    def parse(self):
        response = self._connect(self.url)
        if response is not None and response.status_code == 200:
            next_gen = []
            only_a_tags = SoupStrainer("a")
            soup = BeautifulSoup(response.content, 'lxml')
            for a in soup.find_all(only_a_tags, href=True):
                try:
                    link = a['href']
                except KeyError:
                    next

                lock = threading.Lock()
                lock.acquire()
                if link not in Q:
                    Q.append(link)
                    next_gen.append(link)
                lock.release()
            self.url_obj.child_urls = next_gen

        self.url_obj.status = True                   
        return self.url_obj


lst = Urls(None ,'https://www.google.ru/imghp?hl=ru&tab=wi', 0)
pool = Pool(2, lst)
pool.run()
print(Q)