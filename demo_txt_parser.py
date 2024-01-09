import argparse
import logging
import time

import xlwt

from utils import set_logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', default='/home/manu/tmp/txt/1.txt')
    parser.add_argument('--path_out', default='/home/manu/tmp/txt/1.xlsx')
    return parser.parse_args()


def run(args):
    logging.info(args)
    with open(args.path_in, 'r') as f:
        lines = f.readlines()
    logging.info(lines)
    sheet_name = 'parser_results'
    obj_xlwt = xlwt.Workbook()
    obj_sheet = obj_xlwt.add_sheet(sheet_name, cell_overwrite_ok=True)
    obj_sheet.write(0, 0, 'time')
    obj_sheet.write(0, 1, 'val')
    for i, line in enumerate(lines):
        logging.info(line)
        str_time, str_val = line.strip().split()
        time_float, val_int = float(str_time), int(str_val, 16)
        time_format = time.asctime(time.localtime(time_float))
        logging.info((time_format, val_int))
        obj_sheet.write(i + 1, 0, str(time_format))
        obj_sheet.write(i + 1, 1, str(val_int))
    obj_xlwt.save(args.path_out)


def main():
    set_logging()
    args = parse_args()
    logging.info(args)
    run(args)


if __name__ == '__main__':
    main()
