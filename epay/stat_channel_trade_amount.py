# -*- coding:utf-8 -*-

if __name__ == '__main__':

    with open('32_320100GD001_020_20170801.txt', 'r') as f:
        header = f.readline()
        for line in f:
            items = line.split('\t')
            print items[20]