# -*- coding: utf-8 -*-
# @Time    : 2022/6/8 13:33
# @Author  : tk
import os
import numpy as np
from ipc_worker.ipc_zmq_loader import IPC_zmq,ZMQ_process_worker
from nn_sdk import csdk_wraper
import copy


class My_regression_worker(ZMQ_process_worker):
    def __init__(self,config,device_num,*args,**kwargs):
        super(My_regression_worker,self).__init__(*args,**kwargs)
        #config info , use by yourself
        self._logger.info('Process id {}, group name {} , identity {}'.format(self._idx,self._group_name,self._identity))
        config['model_config']['device_id'] = self._idx % device_num if device_num > 0 else 0
        self._logger.info(config)
        self.config = copy.deepcopy(config)

    #Process begin trigger this func
    def run_begin(self):
        self._logger.info('worker pid {}...'.format(os.getpid()))

        self.sdk = csdk_wraper.csdk_object(self.config['model_config'])
        assert self.sdk.valid()

    # Process end trigger this func
    def run_end(self):
        if self.sdk is not None and self.sdk.valid():
            self.sdk.close()

    #any data put will trigger this func
    def run_once(self,request_data : dict):
        x1 = request_data.get('x1',np.random.rand(1,10))
        x2 = request_data.get('x1',np.random.rand(1,10))
        max_len = self.config.get("max_len",20)

        code,preds = self.sdk.process(0,x1,x2)
        if code != 0:
            return [ -1 * max_len ]
        #第一个输出节点 可以自定义解码
        pred = preds[0]
        return pred