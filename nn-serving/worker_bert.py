# -*- coding: utf-8 -*-
# @Time    : 2022/6/8 13:34
# @Author  : tk
import os
import numpy as np
from ipc_worker.ipc_zmq_loader import IPC_zmq,ZMQ_process_worker
from nn_sdk import csdk_wraper
import copy

# bert model worker
class My_worker_bert(ZMQ_process_worker):
    def __init__(self,config,device_num,*args,**kwargs):
        super(My_worker_bert,self).__init__(*args,**kwargs)
        #config info , use by yourself
        self._logger.info('Process id {}, group name {} , identity {}'.format(self._idx,self._group_name,self._identity))
        config['model_config']['device_id'] = self._idx % device_num if device_num > 0 else 0
        self._logger.info(config)
        self.config = copy.deepcopy(config)

    #Process begin trigger this func
    def run_begin(self):
        self._logger.info('worker pid {}...'.format(os.getpid()))
        from bert_pretty import FullTokenizer
        from bert_pretty import text_feature_char_level_input_ids_mask
        self.tokenizer = FullTokenizer(self.config['vocab_file'],do_lower_case=True)
        self.sdk = csdk_wraper.csdk_object(self.config['model_config'])
        assert self.sdk.valid()

        self.text_feature = text_feature_char_level_input_ids_mask

    # Process end trigger this func
    def run_end(self):
        if self.sdk is not None and self.sdk.valid():
            self.sdk.close()

    #any data put will trigger this func
    def run_once(self,request_data : dict):
        texts = request_data.get('texts',[])
        param = request_data.get('param',{})
        max_len = self.config['max_len']
        input_ids,input_mask = self.text_feature(self.tokenizer,texts,max_len=max_len,with_padding=False)
        code,preds = self.sdk.process(0,input_ids,input_mask)
        if code != 0:
            return [ -1 * len(texts) ]
        #第一个输出节点 可以自定义解码
        pred = preds[0]
        return pred