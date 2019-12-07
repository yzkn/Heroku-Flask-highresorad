#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import os
import time


# const
NOWCAST_URL = 'https://www.jma.go.jp/jp/highresorad/'
CHROME_PATH = 'C:\\Program Files\\chrome-win\\chrome.exe'
DRIVER_PATH = 'C:\\chromedriver_win32\\chromedriver.exe'


def gen_filename(prefix, suffix):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return prefix + now + suffix


def get_rainfall(lat, lng):
    options = Options()
    options.add_argument('--disable-geolocation')
    # options.add_argument('--headless')
    options.add_argument('--window-size=1024,1024')

    driver = None
    if 'heroku' == os.environ.get('ENV', 'local'):
        driver = webdriver.Chrome(options=options)
    else:
        options.binary_location = CHROME_PATH
        driver = webdriver.Chrome(
            options=options, executable_path=DRIVER_PATH)
    driver.get(NOWCAST_URL)

    # 位置情報を取得できませんでした。
    try:
        time.sleep(5)
        driver.save_screenshot(gen_filename('ss1_', '.png'))

        driver.find_element_by_xpath(
            '//div[contains(@id, "viewbutton_OTHER_jmamesh_highresorad")]').click()
        time.sleep(1)
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLat_jmamesh_highresorad")]').clear()
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLat_jmamesh_highresorad")]').send_keys('35.6864604')
        time.sleep(1)
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLon_jmamesh_highresorad")]').clear()
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLon_jmamesh_highresorad")]').send_keys('139.7635769')
        time.sleep(1)
        driver.find_element_by_xpath(
            '//button[contains(@id, "mvCenter_jmamesh_highresorad")]').click()
        time.sleep(2)

        for i in range(8):
            try:
                driver.find_element_by_xpath(
                    '//span[contains(@class, "ui-icon-plus")]').click()
                time.sleep(2)
            except Exception as e:
                print(e)

        try:
            target = driver.find_element_by_class_name('jmamesh-contents')
            driver.execute_script('arguments[0].scrollIntoView(true);', target)
            time.sleep(2)
        except Exception as e:
            print(e)

        for j in range(12):
            driver.find_element_by_xpath(
                '//input[contains(@id, "viewtime_next_jmamesh_highresorad")]').click()
            time.sleep(1)
            driver.save_screenshot(gen_filename(
                'ss2_', '_' + '{:02}'.format(j) + '.png'))
            time.sleep(2)
    except Exception as e:
        print(e)

    driver.save_screenshot(gen_filename('ss3_', '.png'))

    # TODO
    rainfall = 0

    driver.quit()
    return rainfall
