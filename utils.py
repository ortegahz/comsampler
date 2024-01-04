import logging
import os
import shutil

import matplotlib.pyplot as plt
import numpy as np


def com_sampler_update_queue(sampler, queue):
    while True:
        sampler.update_db()
        if queue.qsize() < 1:
            queue.put(sampler.db)


def make_dirs(dir_root):
    if os.path.exists(dir_root):
        shutil.rmtree(dir_root)
    if dir_root:
        os.makedirs(os.path.join(dir_root), exist_ok=True)


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def plot_db(db, keys, colors, pause_time_s=1):
    plt.ion()
    # for key in keys:
    for i, key in enumerate(keys):
        # time_idxs = range(len(db[key]))
        plt.subplot(len(keys), 1, i + 1)
        # logging.info((time_idxs, db[key]))
        plt.plot(np.array(range(len(db[key]))), np.array(db[key]).astype(float), label=key, color=colors[i])
        if key == 'temperature':
            plt.ylabel('°c')
        elif key == 'humidity':
            plt.ylabel('%RH')
        elif key == 'TVOC':
            plt.ylabel('ug/m³')
        elif key == 'PM1.0':
            plt.ylabel('ug/m³')
        elif key == 'CO':
            plt.ylabel('PPM')
        plt.legend()
        plt.grid()
    plt.show()
    plt.pause(pause_time_s)
    plt.clf()


def save_db(db, keys, colors, pause_time_s=1):
    plt.ion()
    # for key in keys:
    for i, key in enumerate(keys):
        time_idxs = range(len(db[key]))
        plt.subplot(len(keys), 1, i + 1)
        plt.plot(np.array(time_idxs), np.array(db[key]).astype(float), label=key, color=colors[i])
        if key == 'temperature':
            plt.ylabel('°c')
        elif key == 'humidity':
            plt.ylabel('%RH')
        elif key == 'TVOC':
            plt.ylabel('ug/m³')
        elif key == 'PM1.0':
            plt.ylabel('ug/m³')
        elif key == 'CO':
            plt.ylabel('PPM')
        plt.legend()
        plt.grid()
    plt.show()
    plt.pause(pause_time_s)
    plt.clf()
