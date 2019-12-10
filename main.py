#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

# $py -m venv herokuenv
# $.\herokuenv\Scripts\activate
# $py -m pip install -r requirements.txt

# 環境変数を設定しておく
# $heroku config:set ENV=heroku

import datetime
import glob
import logging
import os

from flask import Flask, request

from utility import get_rainfall

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# const
DEFAULT_LAT = 35.681236
DEFAULT_LNG = 139.767125


def is_numeric(n):
    try:
        float(n)
    except ValueError:
        return False


def remove_glob(pathname, recursive=False):
    # remove_glob('./*.png')
    for p in glob.glob(pathname, recursive=recursive):
        if os.path.isfile(p):
            os.remove(p)


@app.route('/nowcast', methods=['GET'])
def get_nowcast():
    remove_glob('./*.png')

    lat = request.args.get('lat', DEFAULT_LAT)
    lng = request.args.get('lng', DEFAULT_LNG)

    if False == is_numeric(lat) or False == is_numeric(lng):
        return '', 404

    result_rainfall = get_rainfall(lat, lng)
    logger.info(result_rainfall)
    return result_rainfall, 200


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)
