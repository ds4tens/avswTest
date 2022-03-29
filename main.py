from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import SoupStrainer, BeautifulSoup
from requests import  exceptions
from time import sleep
import queue


Q = queue.SimpleQueue()

r = requests.get('https://google.com')

only_a_tags = SoupStrainer("a")
soup = BeautifulSoup(r.content, 'lxml')
for a in soup.find_all(only_a_tags, href=True):
    a['href']


class Pool:
    def __init__(self, max_workers, job) -> None:
        self.workers = max_workers
        self.job = job

    def form_new_tasks(self):
        pass
    
    def run(self):
        while

class Parser:

    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url
        return self._parse()
    
    def _connect(self, url: str = None,):
        while True:
            try:
                response = requests.get(url=url, timeout=10, allow_redirects=True)
            except exceptions.ConnectionError:
                print('Ooops... Невозможно подключиться к {}'.format(self.name))
                sleep(15)
            except exceptions.TooManyRedirects:
                print('Ooops... Слишком много запросов от {}'.format(self.name))
                sleep(300)
            except exceptions.Timeout:
                print("Ooops.. превышено время ответа от {}".format(self.name))
                sleep(30)
            else:
                break
        return response 

    def _parse(self):
        response = self._connect(self.url)
        if response.status_code == 200:
            next_gen = []
            only_a_tags = SoupStrainer("a")
            soup = BeautifulSoup(response.content, 'lxml')
            for a in soup.find_all(only_a_tags, href=True):
                link = a['href']
                if link not in Q:
                    Q.put(link)
                    next_gen.append(link)
            return next_gen        

        return ()