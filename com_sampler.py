import logging

import serial


class ComSamplerBase:
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600):
        self.ser = serial.Serial(dev_ser, baud_rate)
        self.ser.flushInput()
        self.db_keys = db_keys
        self.db = dict()
        for key in db_keys:
            self.db[key] = list()

    def update_db(self):
        pass


class ComSamplerFS01301(ComSamplerBase):
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600):
        super().__init__(db_keys, dev_ser, baud_rate)

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
        data = list()
        for data_idx in [3]:
            data.append(int(buff_lst[data_idx] + buff_lst[data_idx + 1], 16))
        for i, key in enumerate(self.db_keys):
            self.db[key].append(data[i])


class ComSamplerFS00801(ComSamplerBase):
    def __init__(self, db_keys, dev_ser='/dev/ttyUSB0', baud_rate=9600):
        super().__init__(db_keys, dev_ser, baud_rate)
        self.ser.write(b'\x11\x02\x01\x00\xEC')

    def update_db(self):
        while self.ser.inWaiting() < 1 or not self.ser.read(1).hex() == '16':
            continue
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
