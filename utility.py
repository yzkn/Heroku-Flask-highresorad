#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from PIL import Image
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


def get_center_pixel(filename, x, y):
    img = Image.open(filename)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    r, g, b = img.getpixel((x, y))
    return (r, g, b)


def get_rainfall(lat, lng):
    options = Options()
    options.add_argument('--disable-geolocation')
    options.add_argument('--headless')
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
        time.sleep(7)
        driver.save_screenshot(gen_filename('ss0_', '.png'))
        # source = driver.page_source
        # print('source1')
        # print(source)
        driver.execute_script(
            "var element = document.getElementsByClassName('ui-widget-overlay ui-front')[0];if (element){element.parentNode.removeChild(element);}")
        time.sleep(3)
        print('driver.execute_script()')
        # source = driver.page_source
        # print('source2')
        # print(source)
        elems = driver.find_elements_by_xpath(
            '//button[contains(.,"閉じる")]')
        for elem in elems:
            try:
                elem.click()
            except:
                pass
    except Exception as e:
        print('e')
        print(e)

    try:
        # time.sleep(6)
        driver.save_screenshot(gen_filename('ss1_', '.png'))

        driver.find_element_by_xpath(
            '//div[contains(@id, "viewbutton_OTHER_jmamesh_highresorad")]').click()

        driver.find_element_by_xpath(
            '//input[contains(@id, "textLat_jmamesh_highresorad")]').clear()
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLat_jmamesh_highresorad")]').send_keys('35.6864604')

        driver.find_element_by_xpath(
            '//input[contains(@id, "textLon_jmamesh_highresorad")]').clear()
        driver.find_element_by_xpath(
            '//input[contains(@id, "textLon_jmamesh_highresorad")]').send_keys('139.7635769')

        driver.find_element_by_xpath(
            '//button[contains(@id, "mvCenter_jmamesh_highresorad")]').click()
        time.sleep(2)

        for i in range(8):
            try:
                driver.find_element_by_xpath(
                    '//span[contains(@class, "ui-icon-plus")]').click()
                time.sleep(1)
            except Exception as e:
                print(e)
        time.sleep(4)

        try:
            # 「このチェックボックスは、地図を拡大したときのみ使用することができます。」
            driver.find_element_by_xpath(
                '//input[contains(@id, "viewMUNICIPALITY_jmamesh_highresorad")]').click()

            target = driver.find_element_by_class_name('jmamesh-contents')
            driver.execute_script('arguments[0].scrollIntoView(true);', target)
            time.sleep(1)
        except Exception as e:
            print(e)

        result_rainfall = {}
        for j in range(12):
            driver.find_element_by_xpath(
                '//input[contains(@id, "viewtime_next_jmamesh_highresorad")]').click()
            time.sleep(1)

            nowcast_datetime_str = driver.find_element_by_xpath(
                '//div[contains(@id, "maptitletxt_jmamesh_highresorad")]').text
            nowcast_datetime = datetime.datetime.strptime(
                nowcast_datetime_str.replace(' (予想)', ''), '%Y年%m月%d日%H時%M分')
            nowcast_datetime_formated = nowcast_datetime.isoformat()

            filename = gen_filename('ss2_', '_' + '{:02}'.format(j) + '.png')
            driver.save_screenshot(filename)
            r, g, b = get_center_pixel(filename, 370, 440)
            nowcast_rainfall = rgb2rainfall(r, g, b)
            print('{:03} {:03} {:03} {:03} {}'.format(
                r, g, b, nowcast_rainfall, nowcast_datetime_formated))
            result_rainfall[nowcast_datetime_formated] = nowcast_rainfall
            time.sleep(1)
    except Exception as e:
        print(e)

    driver.save_screenshot(gen_filename('ss3_', '.png'))

    driver.quit()
    return result_rainfall


def rgb2rainfall(r, g, b):
    if r == 0 and g == 0 and b == 0:  # 境界
        return -1
    if r == 171 and g == 196 and b == 160:  # 陸
        return -1
    if r == 184 and g == 184 and b == 230:  # 海
        return -1
    if r == 242 and g == 242 and b == 255:
        return 0
    if r == 160 and g == 210 and b == 255:
        return 1
    if r == 27 and g == 140 and b == 255:
        return 5
    if r == 0 and g == 53 and b == 255:
        return 10
    if r == 255 and g == 245 and b == 0:
        return 20
    if r == 255 and g == 153 and b == 0:
        return 30
    if r == 255 and g == 32 and b == 0:
        return 50
    if r == 180 and g == 0 and b == 104:
        return 80
    return -1
