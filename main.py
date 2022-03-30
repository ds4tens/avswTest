import logging
from utils import Pool, Urls
import sys



if __name__ == '__main__':


    workers = int(sys.argv[1])
    logging = bool(int(sys.argv[2]))
    
    lst = [
        ('https://vk.com', 'vk', 3),
        ('http://crawler-test.com', 'crawler-test', 3),
        ('https://yandex.ru', 'yandex', 2),
        ('http://google.com', 'google', 3),
        ('https://stackoverflow.com', 'stackoverflow', 2)
    ]

    for url, name, depth in lst:
        
        u = Urls(None, url, 0)
        u.refom(url, name)

        p = Pool(workers, u, depth, logging)
        p.run()