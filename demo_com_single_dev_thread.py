import argparse
import logging
import random
import time
from queue import Queue
from threading import Thread

from com_sampler import ComSamplerFS01301, ComSamplerFS00801, ComSamplerFW2511
from utils import set_logging, plot_db, make_dirs, com_sampler_update_queue


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_keys', nargs='+', default=['forward', 'backward'])
    parser.add_argument('--dev_ser', default='/dev/ttyUSB0')
    parser.add_argument('--baud_rate', default=6250)
    parser.add_argument('--interval', default=1)  # second
    parser.add_argument('--dir_save', default='')
    parser.add_argument('--type_sensor', default='FW2511', help='FW2511 or FS01301 or FS00801')
    return parser.parse_args()


def run(**args):
    make_dirs(args['dir_save'])
    db_keys = args['db_keys']
    colors = list()
    for i in range(len(db_keys)):
        colors.append([random.random(), random.random(), random.random()])
    if args['type_sensor'] == 'FW2511':
        com_sampler = ComSamplerFW2511(args['db_keys'], args['dev_ser'], args['baud_rate'], args['dir_save'])
    elif args['type_sensor'] == 'FS01301':
        com_sampler = ComSamplerFS01301(args['db_keys'], args['dev_ser'], args['baud_rate'], args['dir_save'])
    elif args['type_sensor'] == 'FS00801':
        com_sampler = ComSamplerFS00801(args['db_keys'], args['dev_ser'], args['baud_rate'], args['dir_save'])
    else:
        com_sampler = ComSamplerFW2511(args['db_keys'], args['dev_ser'], args['baud_rate'], args['dir_save'])

    q_sampler = Queue()
    p_sampler = Thread(target=com_sampler_update_queue, args=(com_sampler, q_sampler), daemon=True)
    p_sampler.start()

    while True:
        if q_sampler.qsize() > 0:
            db = {**q_sampler.get()}
            plot_db(db, db_keys, colors)
        time.sleep(args['interval'])


def main():
    set_logging()
    args = parse_args()
    logging.info(args)
    run(**vars(args))


if __name__ == '__main__':
    main()
