import argparse
import logging
import random
import time

from com_sampler import ComSamplerFS01301, ComSamplerFS00801
from utils import set_logging, plot


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_keys_a', default=['CO'])
    parser.add_argument('--dev_ser_a', default='/dev/ttyUSB0')
    parser.add_argument('--db_keys_b', default=['humidity', 'temperature', 'PM1.0', 'TVOC'])
    parser.add_argument('--dev_ser_b', default='/dev/ttyUSB1')
    parser.add_argument('--baud_rate', default=9600)
    parser.add_argument('--interval', default=1)  # second
    return parser.parse_args()


def run(**args):
    db_keys = args['db_keys_a'] + args['db_keys_b']
    colors = list()
    for i in range(len(db_keys)):
        colors.append([random.random(), random.random(), random.random()])
    com_sampler_a = ComSamplerFS01301(args['db_keys_a'], args['dev_ser_a'], args['baud_rate'])
    com_sampler_b = ComSamplerFS00801(args['db_keys_b'], args['dev_ser_b'], args['baud_rate'])
    while True:
        com_sampler_a.update_db()
        com_sampler_b.update_db()
        db = {**com_sampler_a.db, **com_sampler_b.db}

        plot(db, db_keys, colors)
        time.sleep(args['interval'])


def main():
    set_logging()
    args = parse_args()
    logging.info(args)
    run(**vars(args))


if __name__ == '__main__':
    main()
