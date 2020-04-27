#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import os


def filereadcsv(originFile_path, toFile_path,duplicate_key):
    if  os.path.exists(toFile_path):
        os.remove(toFile_path)
    df = pd.read_csv(originFile_path,delimiter=',')
    df.drop_duplicates('核验编码').to_csv(toFile_path)
    print("去重成功:" + toFile_path)

if __name__ == "__main__":
    prompt_start = "请拖入需要去重的 csv 文件:\n"
    csv_file = input(prompt_start)
    if not os.path.exists(csv_file):
        print("请拖入有效文件")
    else:
        df = pd.read_csv(csv_file,chunksize=1)
        for index,s in enumerate(df._engine.orig_names):
            print("{0},{1}".format(index,s),end="，")
        prompt_duplicate = "\n请选择根据哪列去重:\n"
        index_key = input(prompt_duplicate)
        filereadcsv(csv_file, os.path.splitext(csv_file)[0] + "_去重.csv",df._engine.orig_names[int(index_key)])