#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import datetime
import logging
import os

from flask import Flask, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# const
DEFAULT_LAT = 35.681236
DEFAULT_LNG = 139.767125


def get_rainfall(lat, lng):
    return 0  # TODO


def is_numeric(n):
    try:
        float(n)
    except ValueError:
        return False


@app.route('/nowcast', methods=['GET'])
def get_nowcast():
    lat = request.args.get('lat', DEFAULT_LAT)
    lng = request.args.get('lng', DEFAULT_LNG)

    if False == is_numeric(lat) or False == is_numeric(lng):
        return '', 404

    # TODO
    rainfall = get_rainfall(lat, lng)

    res = 'timestamp={}, RAINFALL={}'.format(
        datetime.datetime.utcnow() + datetime.timedelta(hours=9), rainfall)
    logger.info(res)
    return res, 200


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)
