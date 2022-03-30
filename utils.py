import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import queue
import threading

import requests
from requests import exceptions
from bs4 import SoupStrainer, BeautifulSoup

import time
from urllib.parse import urlparse
import csv
import logging

class Urls:

    BASE_NAME = None
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
    def refom(self, url, name):
        self.VISITED = []
        self.BASE_URL = url
        self.BASE_NAME = name
    

class Pool:

    def __init__(self, max_workers, task, max_depth, logs) -> None:
        self.workers = max_workers
        self.job = queue.SimpleQueue() # реализована "защита" от гонки потоков
        self.job.put(task)
        self._MAX_DEPTH = max_depth
        self.logs = logs
        self.conf_logs()

    def conf_logs(self):
        if self.logs:
            logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.INFO)

    def _form_new_tasks(self, url_obj):
        """ Формирование заданий для следующей глубины """
        self._send_to_db(url_obj)
        if not url_obj.status:
            self.job.put(url_obj.work_url)
        else:
            for url in url_obj.child_urls:
                task = Urls(url_obj.work_url, url, url_obj.depth + 1)
                self.job.put(task)
        return len


    @staticmethod
    def _send_to_db(url):
        mr = MakeResult()
        mr.send_to_db(url)
        

    def run(self):
        """ Функция создает пул потоков и запускает его, если есть задания и не достигнута макс. глубина """
        start_time = time.time()
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
            
            logging.info('NEXT LEVEL')

        finish_time = time.time()
        MakeResult().make_csv(self.job.get(), finish_time-start_time)
        logging.info('WORKS FINISHED')

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
        logging.info(f'Thread {url}: id = {threading.get_ident()}: name = {threading.current_thread().name}')

        while True:
            response = None
            try:
                response = requests.get(url=url, timeout=10, allow_redirects=True)
            except exceptions.ConnectionError:
                
                logging.info('Thread: {} Невозможно подключиться к {}'.format(threading.get_ident(), url))
                #sleep(15)
                break
            except exceptions.TooManyRedirects:
                print('Thread: {} Слишком много запросов к {}'.format(threading.get_ident(), url))
                #sleep(300)
                break
            except exceptions.Timeout:
                """
                Для некоторых ссылок google кидает постоянный timeout_error , поэтому нет смысла совершать повторный запрос
                А лучше выйти из цикла
                """
                print('Thread: {} превышено время ответа от {}'.format(threading.get_ident(), url))
                break
            except exceptions.MissingSchema:
                url = self.url_obj.BASE_URL + url
                if not self._valid_domain(url, self.url_obj.BASE_NAME):
                    return None 
            except exceptions.InvalidSchema:
                break
            else:
                break
            
        return response 
    
    @staticmethod
    def _valid_domain(url, domain):
        """Проверка, что ссылка относится к нашему сайту"""
        d = urlparse(url).netloc
        return domain in d

    @staticmethod  
    def _valid(link):
        """Проверка, что ссылка имеет смысл"""
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
        """ Парсинг страницы, поиск a href и проверка их корректности"""
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
            logging.info(f'Thread formed next gen {next_gen}: id = {threading.get_ident()}: name = {threading.current_thread().name}')
        self.url_obj.status = True                   
        return self.url_obj


class MakeResult:

    def __init__(self) -> None:
        pass

    def make_csv(self, url, time):
        with open('result.csv', 'a') as csvfile:
            statwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            statwriter.writerow([f'{url.BASE_URL}', f'{time}', f'{len(url.VISITED)}'])


    def send_to_db(self, url):
        data = {
            'base_url': url.parent_url or url.work_url,
            'sub_url': str(url.child_urls),
            'depth': url.depth
        }

        base_url = f'http://127.0.0.1:8000/api/v1/{url.BASE_NAME}/'
        r = requests.post(base_url, data=data, timeout=3)


