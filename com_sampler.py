import logging
import os
import time

import serial


class ComSamplerBase:
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600, dir_save=''):
        self.valid_cnt = 0
        self.db_max_len = 4096
        self.dev_ser = dev_ser
        self.ser = serial.Serial(dev_ser, baud_rate)
        self.ser.flushInput()
        self.db_keys = db_keys
        self.db = dict()
        self.db_raw = list()
        self.dir_save = dir_save
        self.time_s = time.time()
        for key in db_keys:
            self.db[key] = list()

    def save_db_raw(self):
        if not self.dir_save or not os.path.exists(self.dir_save):
            return
        file_name = os.path.basename(self.dev_ser)
        path_save = os.path.join(self.dir_save, file_name + '.txt')
        with open(path_save, 'a') as f:
            for val in self.db_raw:
                f.write(f'{time.time()} {val}\n')
        self.db_raw.clear()


class ComSamplerFS01301(ComSamplerBase):
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600, dir_save=''):
        super().__init__(db_keys, dev_ser, baud_rate, dir_save)

    def update_db(self):
        self.ser.write(b'\x01\x03\x00\x00\x00\x04\x44\x09')
        while self.ser.inWaiting() < 13:
            continue
        buff_lst = list()
        head_0 = self.ser.read(1).hex()
        head_1 = self.ser.read(1).hex()
        head_2 = self.ser.read(1).hex()
        logging.info((head_0, head_1, head_2))
        assert head_0 == '01' and head_1 == '03' and head_2 == '08'
        buff_lst.append(head_0)
        buff_lst.append(head_1)
        buff_lst.append(head_2)
        for _ in range(10):
            buff_lst.append(self.ser.read(1).hex())
        logging.info(buff_lst)
        self.db_raw.extend(buff_lst)
        data = list()
        for data_idx in [3]:
            data.append(int(buff_lst[data_idx] + buff_lst[data_idx + 1], 16))
        for i, key in enumerate(self.db_keys):
            self.db[key].append(data[i])
            self.db[key] = self.db[key][-self.db_max_len:]
        self.save_db_raw()


class ComSamplerFS00801(ComSamplerBase):
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600, dir_save=''):
        super().__init__(db_keys, dev_ser, baud_rate, dir_save)
        self.ser.write(b'\x11\x02\x01\x00\xEC')

    def update_db(self):
        while self.ser.inWaiting() < 1:
            continue
        while True:
            recv = self.ser.read(1).hex()
            self.db_raw.append(recv)
            if recv == '16':
                break
        while self.ser.inWaiting() < 19:
            continue
        buff_lst = list()
        head_0 = '16'
        head_1 = self.ser.read(1).hex()
        head_2 = self.ser.read(1).hex()
        assert head_0 == '16' and head_1 == '11' and head_2 == '01'
        logging.info((head_0, head_1, head_2))
        buff_lst.append(head_0)
        buff_lst.append(head_1)
        buff_lst.append(head_2)
        for _ in range(17):
            buff_lst.append(self.ser.read(1).hex())
        self.db_raw.extend(buff_lst[1:])
        data = list()
        # data.append(int(buff_lst[3] + buff_lst[4], 16))
        # data.append(int(buff_lst[5] + buff_lst[6], 16))
        data.append(int(buff_lst[7] + buff_lst[8], 16) / 10)  # 湿度
        data.append((int(buff_lst[9] + buff_lst[10], 16) - 500) / 10)  # 温度
        # data.append(int(buff_lst[11] + buff_lst[12], 16))
        # data.append(int(buff_lst[13] + buff_lst[14], 16))
        data.append(int(buff_lst[15] + buff_lst[16], 16))  # PM1.0
        data.append(int(buff_lst[17] + buff_lst[18], 16))  # TVOC
        logging.info(buff_lst)
        for i, key in enumerate(self.db_keys):
            self.db[key].append(data[i])
            self.db[key] = self.db[key][-self.db_max_len:]
        self.save_db_raw()


class ComSamplerFW2511(ComSamplerBase):
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600, dir_save=''):
        super().__init__(db_keys, dev_ser, baud_rate, dir_save)

    def update_db(self):
        buff_lst = list()
        while True:
            recv = self.ser.read(1).hex()
            self.db_raw.append(recv)
            buff_lst.append(recv)
            # logging.info(buff_lst)
            if len(buff_lst) >= 6 and buff_lst[-1] == 'fa' and buff_lst[-6] == 'fe':
                buff_lst = buff_lst[-6:]
                break
        self.valid_cnt += 1
        # logging.info(buff_lst)
        # val_forward, val_backward = int(buff_lst[2], 16), int(buff_lst[3], 16)
        data = list()
        for data_idx in [2, 3]:
            data.append(int(buff_lst[data_idx], 16))
        for i, key in enumerate(self.db_keys):
            self.db[key].append(data[i])
            self.db[key] = self.db[key][-self.db_max_len:]
        # self.save_db_raw()
        fps = self.valid_cnt / (time.time() - self.time_s)
        logging.info(('fps --> ', fps))

