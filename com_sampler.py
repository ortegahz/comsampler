import logging

import serial


class ComSampler:
    def __init__(self, cmd_req, db_keys, dev_ser, baud_rate, valid_recv_len, data_idxes, heads):
        self.heads = heads
        self.data_idxes = data_idxes
        self.valid_recv_len = valid_recv_len
        self.cmd_req = cmd_req
        self.db_keys = db_keys
        self.ser = serial.Serial(dev_ser, baud_rate)
        self.ser.flushInput()
        self.db = dict()
        for key in db_keys:
            self.db[key] = list()

    def update(self):
        self.ser.write(self.cmd_req)
        while self.ser.inWaiting() < self.valid_recv_len:
            continue
        buff_lst = list()
        head_0 = self.ser.read(1).hex()
        head_1 = self.ser.read(1).hex()
        head_2 = self.ser.read(1).hex()
        logging.info((head_0, head_1, head_2))
        flag_valid = head_0 == self.heads[0] and head_1 == self.heads[1] and head_2 == self.heads[2]
        if not flag_valid:
            return
        buff_lst.append(head_0)
        buff_lst.append(head_1)
        buff_lst.append(head_2)

        for _ in range(self.valid_recv_len - 3):
            buff_lst.append(self.ser.read(1).hex())
        logging.info(buff_lst)
        data = list()
        for data_idx in self.data_idxes:
            data.append(int(buff_lst[data_idx] + buff_lst[data_idx + 1], 16))
        for i, key in enumerate(self.db_keys):
            if key == 'humidity':
                self.db[key].append(data[i] / 10.)
            elif key == 'temperature':
                self.db[key].append((data[i] - 500) / 10)
            else:
                self.db[key].append(data[i])
            # logging.info(db[key][-1])
