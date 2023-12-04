import logging
import datetime
import os
import app
import asyncio


def create_file():
    try:
        fp = open('.\\config\\logs\\jackbox_{}.log'.format(current_date), 'x')
        fp.close()
    except FileExistsError as exist:
        print('Log file is already exist ( {} )'.format(exist))


try:
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    create_file()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler('.\\config\\logs\\jackbox_{}.log'.format(current_date), encoding='UTF-8'),
                  logging.StreamHandler()],
        encoding='UTF-8')
except FileNotFoundError as f:
    cd = datetime.datetime.now().strftime("%Y-%m-%d")
    path = os.path.expanduser('~\\PycharmProjects\\config\\logs\\jackbox_{}.log'.format(cd))
    print(f)
