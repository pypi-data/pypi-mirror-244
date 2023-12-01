#!/usr/bin/python
# coding: utf-8

"""
调用各类predictor的predictor_files实现对文件的多进程处理
注：将会在当前路径下创建一个临时文件，结束后会删除

Examples:

    >>> import os
    >>> from paraller_preidctor import Pall_process
    
    >>> def pred(x):

        >>> input_file, output_path, indice, sep, device = x
        >>> sepindex=1 if sep=='\t' else 2
        >>> pred_shell = 'prediceot_shell.py'
        >>> os.system('python %s %s %s %s %s '%(pred_shell,input_file, output_path+'xx.csv', pred_name, skip_head)\
        '['+str(indice[0])+','+str(indice[1])+'] '+str(sepindex)) + ' '+ device
        
    >>> if __name__ == '__main__':
        >>> indice = [0,1]
        >>> sep=','
        >>> device='-1'
        >>> input_file='tmp/test.csv'
        >>> output_file='tmp/test_pred.csv'

        >>> Pall_process(pred, 5).run(input_file, output_file, indice, sep, device)
    

Author:  wanggj --<guijiang.wang@neoantigen.cn>
Created: 20/11/23
"""

import os
import sys
import time
import math
import random
import numpy as np
import pandas as pd
import multiprocessing as mp


class Pall_process():
    def __init__(self, funx, process):
        """
        Args:
            funx:需要执行的预测脚本函数名
            process:本次启动的进程数
        Example:
            def funx(x):
                input_file, output_path, indice, sep, device = x
                sepindex=1 if sep !=',' else 2
                pred_shell = 'prediceot_shell.py'
                os.system('python %s %s %s %s %s '%(pred_shell,input_file, output_path+'xx.csv', pred_name, skip_head)\
                '['+str(indice[0])+','+str(indice[1])+'] '+str(sepindex))
                
            Pall_process(funx, 5).run(input_file, output_file, indice, sep, device)
        """
        self.funx = funx
        self.process = process
        self.file_split_path = os.getcwd()+'/tmps/'
        self.random_num = self.random_name(8)
        self.tmp_save = self.file_split_path+self.random_num+'/'
        self.tmp_save_res = self.tmp_save+'res/'

        self.check_path(self.file_split_path)
        self.check_path(self.tmp_save)
        self.check_path(self.tmp_save_res)
        
    def check_path(self, path_):
        if not os.path.exists(path_):
            os.mkdir(path_)
        
    def random_name(self, n=8):
        ret = ""
        for i in range(n):
            num = chr(random.randint(48,57))#ASCII表示数字
            letter = chr(random.randint(97, 122))  # 取小写字母
            Letter = chr(random.randint(65, 90))  # 取大写字母
            s = str(random.choice([num, letter, Letter]))
            ret += s
        return ret
    
    def split_file(self, input_file, tmp_save, sep, processes):
        """
        将单个文件按照进程数进行分割,返回按照顺序分割的文件列表
        1） 获取文件数量
        2） 按照进程数将文件进行划分，并按照顺序保存
        3） 对划分后的文件按照idx进行排序
        4） 返回排序后的文件列表
        Args:
            input_file:原始的预测文件
            tmp_save:文件分割后的存放地址
            sep: sep
            processes:进程数
        return:
            分割生成的文件列表
        """
        print("正在执行{}的文件划分".format(input_file))
        file_name = input_file.split('/')[-1]
        os.system('wc -l '+ input_file + '> '+tmp_save+file_name+'_total_len') # 获取文件的数量
        len_input = int(open(tmp_save+file_name+'_total_len').readline().split(' ')[0])
        os.system('rm -rf '+tmp_save+file_name+'_total_len')
        
        chunk_size = (len_input-1)//processes
        
        print("划分后的文件将存放在{},将会划分为{}个文件".format(tmp_save, math.ceil((len_input-1)/chunk_size)))
        df=pd.read_csv(input_file, sep=sep, chunksize=chunk_size) # 按照进程数将文件进行分割


        for idx, chunk in enumerate(df):
            chunk.to_csv(tmp_save+'/'+file_name[:-4]+'~'+str(idx)+'~'+file_name[-4:], sep=sep, index=False)

        time.sleep(1)
        file_list = [tmp_save+x for x in os.listdir(tmp_save) if '.csv' in x]
        file_list.sort(key=lambda x: int(x.split('~')[1]))
        return file_list
    
    def concat_res(self, tmp_save_res, output_file, sep):
        """
        拼接各个进程的结果
        1） 获取结果的list
        2） 对结果的list按照其idx进行排序
        3） 对list的结果进行合并
        4） 按照要求将结果进行输出
        """
        res_list = [tmp_save_res + x for x in os.listdir(tmp_save_res) if '.ipy' not in x]
        res_list.sort(key=lambda x: int(x.split('~')[1]))
        res = pd.DataFrame()
        for f in res_list:
            r = pd.read_csv(f, sep=sep)
            res = pd.concat([res, r], axis=0)
        res.to_csv(output_file, sep=sep, index=False)
        
    def _pool(self, funx, iters, processes):
        """
        并行进程，可使用pkill test.py全部杀死终结进程
        """
        pool=mp.Pool(processes=processes)
        pool.map(funx, iters)
        pool.close()
        pool.join()
        
    def run(self, input_file, output_file, indice, sep, device):
        """
        执行主函数
        Args:
            input_file:需要预测的文件
            output_file:预测结果输出文件
            indice:需要预测的列id，如[0,1]
            sep:文件分隔符
            device:使用gpu或者cpu('-1')
        Example:
            Pall_process(funx, 5).run(input_file, output_file, indice, sep, device)
            
        kill进程：
            pkill test.py
        查看进程:
            ps aux | grep "test.py"
            
        """
        file_list = self.split_file(input_file, self.tmp_save, sep, self.process)
        
        file_list = [(x, self.tmp_save_res, indice, sep, device) for x in file_list]
    
        self._pool(self.funx, file_list, self.process)
    
        self.concat_res(self.tmp_save_res, output_file, sep)
        
        os.system('rm -rf '+ self.tmp_save)
        
        
if __name__ == '__main__':
    pass