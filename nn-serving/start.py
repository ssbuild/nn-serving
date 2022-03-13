# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 10:07
# @Author  : wyw
import copy
import sys
sys.path.append('.')

import multiprocessing
import os
from ipc_worker.ipc_zmq_loader import IPC_zmq,ZMQ_process_worker
from  http_proxy import HTTP_Proxy

from nn_sdk import csdk_wraper
from bert_pretty import FullTokenizer
from bert_pretty import text_feature_char_level_input_ids_mask
from config.config import config as nn_config



tmp_dir = './tmp'
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

os.environ['ZEROMQ_SOCK_TMP_DIR'] = tmp_dir

class My_worker(ZMQ_process_worker):
    def __init__(self,config,device_num,*args,**kwargs):
        super(My_worker,self).__init__(*args,**kwargs)
        #config info , use by yourself
        self._logger.info('Process id {}, group name {} , identity {}'.format(self._idx,self._group_name,self._identity))

        config['model_config']['device_id'] = self._idx % device_num if device_num > 0 else 0
        self._logger.info(config)



        self.config = copy.deepcopy(config)

    #Process begin trigger this func
    def run_begin(self):
        self._logger.info('worker pid {}...'.format(os.getpid()))

        self.tokenizer = FullTokenizer(self.config['vocab_file'],do_lower_case=True)
        self.sdk = csdk_wraper.csdk_object(self.config['model_config'])
        assert self.sdk.valid()

    # Process end trigger this func
    def run_end(self):
        if self.sdk is not None and self.sdk.valid():
            self.sdk.close()

    #any data put will trigger this func
    def run_once(self,request_data : dict):
        texts = request_data.get('texts',[])
        param = request_data.get('param',{})
        max_len = self.config['max_len']
        input_ids,input_mask = text_feature_char_level_input_ids_mask(self.tokenizer,texts,max_len=max_len,with_padding=False)
        code,preds = self.sdk.process(0,input_ids,input_mask)
        if code != 0:
            return [ -1 * len(texts) ]
        #第一个输出节点 可以自定义解码
        pred = preds[0]
        return pred

if __name__ == '__main__':
    evt_quit = multiprocessing.Manager().Event()
    queue_mapper = {}
    process_list = []

    #gpu 数量
    device_num = 1
    for k,config in nn_config.items():
        group_name = 'serving_group_{}_1'.format(k)
        # group_name
        # manager is an agent  and act as a load balancing
        # worker is real doing your work
        instance = IPC_zmq(
            CLS_worker=My_worker,
            worker_args=(config,device_num),  # must be tuple
            worker_num=device_num * 2,  # number of worker Process
            group_name=group_name,  # share memory name
            evt_quit=evt_quit,
            queue_size=20,  # recv queue size
            is_log_time=True,  # whether log compute time
        )
        process_list.append(instance)
        queue_mapper[group_name] = instance
        instance.start()

    http_ = HTTP_Proxy(queue_mapper,
                 http_ip='0.0.0.0',
                 http_port=8081,)
    http_.start()
    process_list.append(http_)

    try:
        for p in process_list:
            p.join()
    except Exception as e:
        evt_quit.set()
        for p in process_list:
            p.terminate()
    del evt_quit