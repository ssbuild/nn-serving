# 简介
   nn-serving 是一个神经网络推理服务，推理冻结的模型并提供restful接口.
   
实例demo提供一个回顾预测 y = 1 *x1 + 2 * x2
# 推荐环境
   linux python >=3.8
   因对进程的管理和共享内存机制，暂时不支持windows
    

# 安装模块
pip install -r nn-serving/requirements.txt


## 启动

```
cd script
bash start.sh
```

## 客户端测试
`
curl http://192.168.16.157:8081/predict -H "Content-Type: application/json" -X POST -d '{"param":{"mode":"cls"},"texts":["111"]}
`

`
返回
[
    [
        1.1050461530685425,
        1.8959273099899292,
        1.5472604036331177,
        1.8059791326522827,
        1.0221816301345825,
        0.8907957077026367,
        2.3363492488861084,
        1.1122045516967773,
        1.6358901262283325,
        1.4435145854949951
    ]
]
`

