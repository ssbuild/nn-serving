# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 10:07
# @Author  : wyw
import copy
import os
import multiprocessing
from config.config import config as nn_config
from  http_proxy import HTTP_Proxy
from ipc_worker.ipc_zmq_loader import IPC_zmq,ZMQ_process_worker
# from worker_regression import My_regression_worker
# from worker_bert import My_worker_bert
import worker_none

tmp_dir = './tmp'
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

os.environ['ZEROMQ_SOCK_TMP_DIR'] = tmp_dir



if __name__ == '__main__':
    evt_quit = multiprocessing.Manager().Event()
    queue_mapper = {}
    process_list = []

    #gpu 数量
    device_num = 1
    for mode,config in nn_config.items():
        group_name = 'serving_group_{}_1'.format(mode)
        # group_name
        # manager is an agent  and act as a load balancing
        # worker is real doing your work
        instance = IPC_zmq(
            CLS_worker=worker_none.My_worker,
            worker_args=(config,device_num),  # must be tuple
            worker_num=device_num * 2,  # number of worker Process
            group_name=group_name,  # share memory name
            evt_quit=evt_quit,
            queue_size=20,  # recv queue size
            is_log_time=True,  # whether log compute time
        )
        process_list.append(instance)
        queue_mapper[mode] = instance
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