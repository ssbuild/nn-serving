# -*- coding: utf-8 -*-
import random

import numpy as np
from nn_sdk import csdk_object





'''
    前言: 
        当前支持开发语言c/c++,python,java
        当前支持推理引擎tensorflow(v1,v2) onnxruntime
        当前支持多子图,支持图多输入多输出，支持tensorflow 1 pb , tensorflow 2 pb , tensorflow ckpt
        当前支持tensorflow 1.x pb模型和onnx模型 aes加密 , 模型加密参考test_aes.py
        推荐环境ubuntu16 ubuntu18  ubuntu20 centos7 centos8 windows系列
        python (test_py.py) , c包 (test.c) , java包 (nn_sdk.java)
        qq group: 759163831
'''
'''
    python 推理demo
    config 字段介绍:
        aes: 模型加密配置，目前支持tensorflow 1 pb 模型
        engine: 推理引擎 0: tensorflow , 1: onnx
        log_level: 日志类型 0 fatal , 2 error , 4 info , 8 debug
        model_type: tensorflow时有效, 0 pb format   if 1 ckpt format
        ConfigProto: tensorflow时有效
        graph_inf_version: tensorflow version [0,1] or onnxruntime 1
        graph: 多子图配置 
            node: 例子: tensorflow 1 input_ids:0 ,  tensorflow 2: input_ids , onnx: input_ids
            data_type: 节点的类型根据模型配置，支持 int int64 long longlong float double 
            shape: 节点尺寸
            java 和 c 包不可缺少 data_type,shape字段

'''
config = {
    "model_dir": r'./model.ckpt',
    "aes": {
        "use": False,
        "key": bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
        "iv": bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    },
    "log_level": 8,
    'engine': 0,
    "device_id": 0,
     'tf':{
        "ConfigProto": {
            "log_device_placement": False,
            "allow_soft_placement": True,
            "gpu_options": {
                "allow_growth": True
            },
            "graph_options":{
                "optimizer_options":{
                    "global_jit_level": 1
                }
            },
        },
        "engine_version": 1, # tensorflow majar version , must be correct.
        "model_type": 1,# 0 pb , 1 ckpt
        #配置pb模型
        "saved_model":{
            # model_type为 1 pb , 模型有效,
            # 模型是否是是否启用saved_model冻结 , 如果是,则 use=True并且配置tags
            # 普通 freeze pb , use = False
            'use': False, # 是否启用saved_model
            'tags': ['serve'],
            'signature_key': 'serving_default',
        },
        "fastertransformer":{
            "use": False,
            "cuda_version":"11.3", #pip install tf2pb ,支持10.2 11.3 ,
        }
    },
    'onnx': {
        "engine_version": 1,
    },
    'trt': {
        'enable_graph': 0,
        "engine_version": 8,
    },
    "graph": [
        {
            "input": [
                {"node": "x1:0", "dtype": "float32"},
                {"node": "x2:0", "dtype": "float32"},
            ],
            "output": [
                {"node": "pred_ids:0", "dtype": "float32"},
            ],
        }
    ]
}

batch_size = 1
seq_length = 10
x1 = np.random.randint(1,10,size=(batch_size,seq_length))
x2 = np.random.randint(1,10,size=(batch_size,seq_length))

inputs = (x1,x2)

sdk_inf = csdk_object(config)
if sdk_inf.valid():
    net_stage = 0
    ret, out = sdk_inf.process(net_stage, *inputs)

    print(x1)
    print(x2)
    print(ret)
    print(out)
    sdk_inf.close()