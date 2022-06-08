# @Time    : 2022/3/13 11:29
# @Author  : tk
# @FileName: config.py

import os

base_path =  os.path.join(os.path.dirname(__file__),'../..')

regression_conf = {
    "model_dir": os.path.join(base_path,'train/model.ckpt'),
    "aes": {
        "use": False,
        "key": bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
        "iv": bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    },
    "log_level": 8,
    'engine': 0,
    "device_id": -1,
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

config = dict(
    cls=dict(
        type="cls",
        vocab_file=os.path.join(os.path.dirname(regression_conf['model_dir']), 'vocab.txt'),
        max_len=400,
        do_lower_case=True,
        with_decode=True,
        model_config=regression_conf,
        id2label={},
        #label_file=os.path.join(os.path.dirname(regression_conf['model_dir']), 'labels.txt'),
    )
)