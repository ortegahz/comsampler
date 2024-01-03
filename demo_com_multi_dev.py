import argparse
import logging
import random
import time

from com_sampler import ComSamplerFS01301, ComSamplerFS00801, ComSamplerFW2511
from utils import set_logging, plot_db, make_dirs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_keys_a', default=['CO'])
    parser.add_argument('--dev_ser_a', default='/dev/ttyUSB0')
    parser.add_argument('--db_keys_b', default=['humidity', 'temperature', 'PM1.0', 'TVOC'])
    parser.add_argument('--dev_ser_b', default='/dev/ttyUSB1')
    parser.add_argument('--db_keys_c', default=['forward', 'backward'])
    parser.add_argument('--dev_ser_c', default='/dev/ttyUSB2')
    parser.add_argument('--db_keys_choose', default=['forward', 'backward'])
    parser.add_argument('--baud_rate', default=9600)
    parser.add_argument('--interval', default=1)  # second
    parser.add_argument('--dir_save', default='/home/manu/tmp/sampler_results')
    return parser.parse_args()


def run(**args):
    make_dirs(args['dir_save'])
    db_keys = args['db_keys_a'] + args['db_keys_b'] + args['db_keys_c']
    # db_keys = args['db_keys_choose']
    colors = list()
    for i in range(len(db_keys)):
        colors.append([random.random(), random.random(), random.random()])
    com_sampler_a = ComSamplerFS01301(args['db_keys_a'], args['dev_ser_a'], args['baud_rate'], args['dir_save'])
    com_sampler_b = ComSamplerFS00801(args['db_keys_b'], args['dev_ser_b'], args['baud_rate'], args['dir_save'])
    com_sampler_c = ComSamplerFW2511(args['db_keys_c'], args['dev_ser_c'], 6250, args['dir_save'])
    while True:
        com_sampler_a.update_db()
        com_sampler_b.update_db()
        com_sampler_c.update_db()
        db = {**com_sampler_a.db, **com_sampler_b.db, **com_sampler_c.db}
        plot_db(db, db_keys, colors)
        time.sleep(args['interval'])


def main():
    set_logging()
    args = parse_args()
    logging.info(args)
    run(**vars(args))


if __name__ == '__main__':
    main()
