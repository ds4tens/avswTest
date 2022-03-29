from concurrent.futures import ThreadPoolExecutor
import threading
import requests
from bs4 import SoupStrainer, BeautifulSoup
from requests import  exceptions
from time import sleep
from itertools import repeat

Q = []
BASE_URL = 'https://google.com'
r = requests.get('https://google.com')

only_a_tags = SoupStrainer("a")
soup = BeautifulSoup(r.content, 'lxml')
for a in soup.find_all(only_a_tags, href=True):
    a['href']


class Pool:
    def __init__(self, max_workers, job) -> None:
        self.workers = max_workers
        self.job = job

    def form_new_tasks(self, links):
        for link in links:
            self.job.append(link)
    
    def run(self):
        flag = 2
        
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            gen = executor.map(Parser.parse, repeat(a),  self.job)
        for g in gen:
            self.form_new_tasks(g)

class Parser:

    def __init__(self, url, name='thr') -> None:
        self.name = name
        self.url = url
    
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
        

    def parse(self, url):
        response = Parser('')._connect(url)
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
            return next_gen        

        return ()


lst = ['https://www.google.ru/imghp?hl=ru&tab=wi', 'https://maps.google.ru/maps?hl=ru&tab=wl', 'https://play.google.com/?hl=ru&tab=w8', 'https://www.youtube.com/?gl=RU&tab=w1', 'https://news.google.com/?tab=wn', 'https://mail.google.com/mail/?tab=wm', 'https://drive.google.com/?tab=wo', 'https://www.google.ru/intl/ru/about/products?tab=wh', 'http://www.google.ru/history/optout?hl=ru', '/preferences?hl=ru', 'https://accounts.google.com/ServiceLogin?hl=ru&passive=true&continue=https://www.google.com/&ec=GAZAAQ', '/advanced_search?hl=ru&authuser=0', 'http://www.google.ru/intl/ru/services/', '/intl/ru/about.html', 'https://www.google.com/setprefdomain?prefdom=RU&prev=https://www.google.ru/&sig=K_-a8iAohFX3vwfmAvR4WW_aSAQ18%3D', '/intl/ru/policies/privacy/', '/intl/ru/policies/terms/']

pool = Pool(2, lst)
pool.run()
print(Q)
'''parser = Parser('edu', 'https://google.com/')
print(parser.parse())
print()'''