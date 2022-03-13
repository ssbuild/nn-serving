# -*- coding: utf-8 -*-
# @Time    : 2021/11/19 12:45
# @Author  : wyw
import json
import os
from sanic import Sanic
from sanic import response
from multiprocessing import Process



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

        self.app = self.create_app()

    def create_app(self):
        app = Sanic(__name__)



        @app.route('/predict')
        def test_query(request):
            try:
                r = request.form if request.form else request.json
                print(r)
                texts = r.get('texts',[])
                param = r.get('param', None)
                if len(texts) == 0 or texts is None:
                    return response.json({'code': -1, "msg": "invalid data"})
                if param is None or param["mode"] is None:
                    return response.json({'code': -1, "msg": "invalid data"})
                mode = param["mode"]
                if mode not in self.queue_mapper:
                    return response.json({'code': -1, "msg": "invalid data"})


                instance = self.queue_mapper["mode"]

                request_id = instance.put(r)

                data = instance.get(request_id)

                return response.json(data)
            except Exception as e:
                raise response.json({'code': -1, "msg": str(e)})
        return app

    def close_server(self):
        self.app.stop()
    def run(self):
        self.app.run(host=self.http_ip, port=self.http_port, debug=False)