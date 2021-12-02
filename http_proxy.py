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

        self.app = self.create_app(self.queue_mapper)

    def create_app(self, queue_mapper):
        app = Sanic(__name__)


        @app.route('/')
        def test_query(request):
            data = request.args

            #process group 1
            instance = list(self.queue_mapper.values())[0]

            request_id = instance.put(data)

            data = instance.get(request_id)

            return response.json(data)
        return app

    def close_server(self):
        self.app.stop()
    def run(self):
        self.app.run(host=self.http_ip, port=self.http_port, debug=False)