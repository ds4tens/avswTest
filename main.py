from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import queue
import threading
import requests
from bs4 import SoupStrainer, BeautifulSoup
from requests import  exceptions
from time import sleep

# TODO перекинуть общий список и base url в классы



class Urls:

    BASE_URL = None
    VISITED = []

    """ Класс представляет из себя подобие дерева, где хранятся потомоки и наследники"""
    def __init__(self, parent_url, work_url, depth) -> None:
        self.parent_url = parent_url
        self.work_url = work_url
        self.depth = depth
        self.child_urls = []
        self.status = False
    
    @classmethod
    def set_base_url(self, url):
        self.BASE_URL = url
    

class Pool:

    def __init__(self, max_workers, task, max_depth) -> None:
        self.workers = max_workers
        self.job = queue.SimpleQueue() # реализована "защита" от гонки потоков
        self.job.put(task)
        self._MAX_DEPTH = max_depth

    def _form_new_tasks(self, url_obj):
        """ Формирование заданий для следующей глубины """
        if not url_obj.status:
            self.job.put(url_obj.work_url)
        else:
            for url in url_obj.child_urls:
                self.job.put(Urls(url_obj.work_url, url, url_obj.depth + 1))
                
    
    def run(self):
        """ Функция создает пул потоков и запускает его, если есть задания и не достигнута макс. глубина """
        for _ in range(self._MAX_DEPTH):     
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
    """ Класс парсинга сайта"""
    def __init__(self, url: object, name='thr') -> None:
        self.name = name
        self.url = url.work_url
        self.url_obj = url

    def _connect(self, url):
        """ 
        Функция обрабатывает запросы 
        И возвращает ответ
        """
        # logging нужен

        while True:
            response = None
            try:
                response = requests.get(url=url, timeout=10, allow_redirects=True)
            except exceptions.ConnectionError:
                print('Ooops... Невозможно подключиться к {}'.format(url))
                sleep(15)
            except exceptions.TooManyRedirects:
                print('Ooops... Слишком много запросов к {}'.format(url))
                sleep(300)
            except exceptions.Timeout:
                """
                Для некоторых ссылок google кидает постоянный timeout_error , поэтому нет смысла совершать повторный запрос
                А лучше выйти из цикла
                """
                print("Ooops.. превышено время ответа от {}".format(url))
                break
            except exceptions.MissingSchema:
                #print(f'url={url} base_url={self.url_obj.BASE_URL}')
                url = self.url_obj.BASE_URL + url
                #print(f'end = {url}')
            except exceptions.InvalidSchema:
                break
            else:
                break
            
        return response 
    @staticmethod  
    def _valid(link):
        if len(link) < 1:
            return False
        if link[0] == '#':
            return False
        while link[0] == '.':
            link = link[1:]
        if link[0] not in('.', '/', '#', 'h'):
            link = '/'+link
        return link

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
                    continue

                link = self._valid(link)
                if not link:
                    continue

                lock = threading.Lock()
                lock.acquire()
                if link not in self.url_obj.VISITED:
                    self.url_obj.VISITED.append(link)
                    next_gen.append(link)
                lock.release()

            self.url_obj.child_urls = next_gen

        self.url_obj.status = True                   
        return self.url_obj


class MakeResult:

    def __init__(self) -> None:
        pass

    def make_csv(self, url, time, url_counter):
        pass
    
    def send_to_db():
        pass

u = Urls(None, 'https://google.com/', 0)
u.set_base_url('https://google.com')
pool = Pool(10, u, 3)
pool.run()