#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import os

def filereadcsv(originFile_path,toFile_path):
    df = pd.read_csv(originFile_path,delimiter='\t')
    df.drop_duplicates('核验编码').to_csv(toFile_path)
    # for chunks in pd.read_csv(originFile_path,chunksize=50000,header=0,delimiter=","):
    #     try:
    #         # print(chunks.info())
    #         chunks.groupby('核验编码').min().to_csv(toFile_path)
    #     except Exception as e:
    #         print(e)
    #         continue

if __name__ == "__main__":
    prompt_start = "请拖入需要去重的 csv 文件:\n"
    csv_file = input(prompt_start)
    if not os.path.exists(csv_file):
        print("请拖入有效文件")
    else:
        filereadcsv(csv_file,os.path.splitext(csv_file)[0] + "_rd.csv")