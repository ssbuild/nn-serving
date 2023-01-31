# -*- coding: utf-8 -*-
# @Time    : 2021/11/19 12:45
# @Author  : wyw
import json
import os
from sanic import Sanic
from sanic import response
from multiprocessing import Process
from config.config import config as nn_config
import numpy as np


class HTTP_Proxy(Process):
    def __init__(self,
                 queue_mapper : dict,
                 http_ip='0.0.0.0',
                 http_port=8088,
                 cors='*',
                 http_num_workers=1,
    ):
        super().__init__(daemon=True)
        self.cors = cors
        self.http_num_workers = http_num_workers
        self.http_ip = http_ip
        self.http_port = http_port
        self.queue_mapper = queue_mapper

        self.app = None
        # self.app = self.create_app()

    def create_app(self):
        app = Sanic('nn-' + __name__)


        @app.route('/predict', methods=['POST'])
        def test_query(request):
            try:
                r = request.form if request.form else request.json
                print(r)
                texts = r.get('texts',[])
                param = r.get('param', None)
                if len(texts) == 0 or texts is None:
                    return response.json({'code': -1, "msg": "invalid data"})
                if param is None or param["mode"] is None:
                    msg = "param is required"
                    print(msg)
                    return response.json({'code': -1, "msg": msg})
                mode = param["mode"]
                if mode not in nn_config:
                    msg = "mode not in " + ','.join(list(nn_config.keys()))
                    print(msg)
                    return response.json({'code': -1, "msg": msg })


                instance = self.queue_mapper[mode]

                request_id = instance.put(r)

                result = instance.get(request_id)

                if isinstance(result,np.ndarray):
                    result = result.tolist()
                return response.json(result)
            except Exception as e:
                raise response.json({'code': -1, "msg": str(e)})
        return app

    def close_server(self):
        if self.app is not None:
            self.app.stop()
    def run(self):
        self.app = self.create_app()
        self.app.prepare(host=self.http_ip, port=self.http_port, debug=False)
        Sanic.serve_single(primary=self.app)
        # self.app.run(host=self.http_ip, port=self.http_port, debug=False)