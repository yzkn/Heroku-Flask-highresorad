#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import os
import time


# const
NOWCAST_URL = 'http://www.jma.go.jp/jp/highresorad/'
CHROME_PATH = 'C:\\Program Files\\chrome-win\\chrome.exe'
DRIVER_PATH = 'C:\\chromedriver_win32\\chromedriver.exe'


def gen_filename(prefix, suffix):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return prefix + now + suffix


def get_rainfall(lat, lng):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1024,768')

    if 'heroku' == os.environ.get('ENV', 'local'):
        driver = webdriver.Chrome(options=options)
    else:
        options.binary_location = CHROME_PATH
        driver = webdriver.Chrome(
            options=options, executable_path=DRIVER_PATH)
    driver.get(NOWCAST_URL)
    time.sleep(10)

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
    except TimeoutException as e:
        pass

    driver.save_screenshot(gen_filename('ss_', '.png'))

    # TODO
    rainfall = 0

    driver.quit()
    return rainfall
