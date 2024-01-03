import logging

import matplotlib.pyplot as plt
import numpy as np


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


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
