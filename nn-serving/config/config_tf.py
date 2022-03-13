# @Time    : 2022/3/13 11:29
# @Author  : tk
# @FileName: config.py

__cls_config__ = {
    "model_dir": '/data/finalmodel/2021/cls/09/model_cls_torch.onnx',
    "aes":{
        "use":False,
        "key":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
        "iv":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
    },
    "log_level": 8,
    'engine':1,
    "device_id":0,
    'onnx':{
        "engine_version": 1,
    },
    "graph": [
        {
            "input": [
                {"node":"input_ids", "dtype":"int64", "shape":[1, 400]},
                {"node":"input_mask", "dtype":"int64", "shape":[1, 400]},
            ],
            "output": [
                {"node":"pred_ids", "dtype":"int64", "shape":[1, 400]},
            ],
        }
    ]
}

config_cls_ = {
    "model_dir": r'/root/model.pb',
    "aes":{
        "use":False,
        "key":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
        "iv":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
    },
    "log_level": 8,# 0 fatal , 2 error , 4 warn, 8 info , 16 debug
    'engine':0, # 0 tensorflow,  1 onnx , 2  tensorrt , 3 fasttext
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
        "model_type": 0,# 0 pb , 1 ckpt
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
    'onnx':{
        "engine_version": 1,# onnxruntime version
    },
    'trt':{
        "engine_version": 8,# tensorrt version
        "enable_graph": 0,
    },
    'fasttext': {
        "engine_version": 0,# fasttext version
        "threshold":0, # 预测k个标签的阈值
        "k":1, # 预测k个标签 score >= threshold
        "dump_label": 1, #输出内部标签，用于上层解码
        "predict_label": 1, #获取预测标签 1  , 获取向量  0
    },
    "graph": [
        {
            # 对于Bert模型 shape [max_batch_size,max_seq_lenth],
            # 其中max_batch_size 用于c++ java开辟输入输出缓存,输入不得超过max_batch_size，对于python没有作用，取决于上层用户真实输入
            # python 限制max_batch_size 在上层用户输入做 , dtype and shape are not necessary for python
            # 对于fasttext node 对应name可以任意写，但不能少
            # dtype must be in [int int32 int64 long longlong uint uint32 uint64 ulong ulonglong float float32 float64 double str]
            "input": [
                {
                    "node":"input_ids:0",
                    "dtype":"int64",
                    #"shape":[1, 256] #Python may be empty, c/c++ java must exist , it will be used to alloc mem
                },
                {
                    "node":"input_mask:0",
                    "dtype":"int64",
                    #"shape":[1, 256] #Python may be empty , c/c++ java must exist , it will be used to alloc mem
                }
            ],
            "output": [
                {
                    "node":"pred_ids:0",
                    "dtype":"int64",
                    #"shape":[1, 256] #Python may be empty , c/c++ java must exist , it will be used to alloc mem
                },
            ],
        }
    ]
}