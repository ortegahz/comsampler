import argparse
import logging
import random
import time

import matplotlib.pyplot as plt
import numpy as np

from com_sampler import ComSampler


def plot(db, keys, colors, pause_time_s=1):
    plt.ion()
    # for key in keys:
    for i, key in enumerate(keys):
        time_idxs = range(len(db[key]))
        plt.subplot(len(keys), 1, i + 1)
        plt.plot(np.array(time_idxs), np.array(db[key]).astype(float), label=key, color=colors[i])
        plt.legend()
        plt.grid()
    plt.show()
    plt.pause(pause_time_s)
    plt.clf()


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd_in_a', default=b'\x01\x03\x00\x00\x00\x04\x44\x09')
    parser.add_argument('--db_keys_a', default=['CO'])
    parser.add_argument('--dev_ser_a', default='/dev/ttyUSB0')
    parser.add_argument('--cmd_in_b', default=b'\x11\x02\x01\x00\xEC')
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
    com_sampler_a = ComSampler(args['cmd_in_a'], args['db_keys_a'],
                               args['dev_ser_a'], args['baud_rate'],
                               13, [3], ['01', '03', '08'])
    com_sampler_b = ComSampler(args['cmd_in_b'], args['db_keys_b'],
                               args['dev_ser_b'], args['baud_rate'],
                               20, [7, 9, 15, 17], ['16', '11', '01'])
    while True:
        com_sampler_a.update()
        com_sampler_b.update()
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
