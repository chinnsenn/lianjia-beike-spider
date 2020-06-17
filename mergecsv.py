#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import os
 
def merge_csv(src_path,merge_name):
    #修改当前工作目录
    os.chdir(src_path)
    #将该文件夹下的所有文件名存入一个列表
    file_list = os.listdir()
    
    #读取第一个CSV文件并包含表头
    df = pd.read_csv(src_path + os.sep + file_list[0])   #编码默认UTF-8，若乱码自行更改
    #将读取的第一个CSV文件写入合并后的文件保存
    df.to_csv(src_path+ os.sep + merge_name +'.csv',encoding="utf_8_sig",index=False)
    #循环遍历列表中各个CSV文件名，并追加到合并后的文件
    for i in range(1,len(file_list)):
        if file_list[i].endswith(".csv"):
            print(file_list[i])
            df = pd.read_csv(src_path + os.sep + file_list[i])
            df.to_csv(src_path+ os.sep + merge_name +'.csv',encoding="utf_8_sig",index=False, header=False, mode='a+')

if __name__ == "__main__":
    prompt_start = "请拖入需要去重的 csv 文件夹:\n"
    csv_folder = input(prompt_start).replace(' ','')

if not os.path.isdir(csv_folder):
    print("请拖入有效文件夹")
else:
    prompt_start = "请输入合并后的文件名:\n"
    merge_name = input(prompt_start).replace(' ','')
    merge_csv(csv_folder,merge_name)