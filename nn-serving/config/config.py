# @Time    : 2022/3/13 11:29
# @Author  : tk
# @FileName: config.py

import os
from bert_pretty.cls import load_labels as load_cls_label
from .config_tf import __cls_config__



config = dict(
    cls = dict(
        type="cls",
        vocab_file=os.path.join(os.path.dirname(__cls_config__['model_dir']), 'vocab.txt'),
        max_len=400,
        do_lower_case=True,
        with_decode=True,
        model_config=__cls_config__,
        id2label={},
        label_file=os.path.join(os.path.dirname(__cls_config__['model_dir']), 'labels.txt'),
        parse_label=load_cls_label,
    )
)