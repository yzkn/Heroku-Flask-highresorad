#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import datetime
import logging
import os

from flask import Flask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/nowcast', methods=['GET'])
def get():
    #TODO
    rainfall = 0

    res = 'timestamp={}, RAINFALL={}'.format(
        datetime.datetime.utcnow() + datetime.timedelta(hours=9), rainfall)
    logger.info(res)
    return res, 200


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)
