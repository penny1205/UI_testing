# __author__ = ‘pan‘
# -*-coding:utf-8-*-

from PIL import Image
import math
import operator
import os
from functools import reduce
from util.config.init.readinit import ReadInit
from util.config.yaml.readyaml import ReadYaml
from util.file.fileutil import FileUtil


def format_photo(photopath):
    # 根据图片路径返回post请求需要的表单格式
    if photopath != '':  # 需传递图片绝对路径
        if os.path.isfile(photopath):
            receipt_name = os.path.basename(photopath)
            with open(photopath, 'rb') as f:
                receipt = (receipt_name, f.read())
        else:
            # 图片路径不正确
            receipt = (None, '')
    else:
        receipt = (None, '')
    return receipt

#截图函数
def insert_img(driver, filename):
    config = ReadYaml(FileUtil.getProjectObsPath() + '/config/config.yaml').getValue()
    file_path = config['screenshot_path'] + '\\' + filename
    driver.take_screenshot(file_path)
    return file_path

#时间区间比较函数,日期大小比较函数
import time
# 这里比较l_time 是否在时间区间[start_t, end_t]中
def time_compare(l_time, start_t, end_t):
    #"2011-11-10 14:56:58"  定义格式串时应该为: "%Y-%m-%d %H:%M:%S"
    s_time = time.mktime(time.strptime(start_t, '%Y%m%d%H%M'))  # get the seconds for specify date
    e_time = time.mktime(time.strptime(end_t, '%Y%m%d%H%M'))
    log_time = time.mktime(time.strptime(l_time, '%Y-%m-%d %H:%M:%S'))
    if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
        return True
    return False

# 图片对比函数
def image_compare(img1,img2):
    image1 = Image.open(img1)
    image2 = Image.open(img2)

    h1 = image1.histogram()
    h2 = image2.histogram()
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return result

#添加token至session storage
def set_session(driver):
    configinit = ReadInit(FileUtil.getProjectObsPath() + '/config/config.init')
    driver.js('sessionStorage.setItem("token","{0}");'.format(configinit.getValue('session','token')))
    driver.js('sessionStorage.setItem("appToken","{0}");'.format(configinit.getValue('session','appToken')))
    driver.js('sessionStorage.setItem("partnerNo","{0}");'.format(configinit.getValue('session','partnerNo')))
    driver.js('sessionStorage.setItem("enterName","{0}");'.format(configinit.getValue('session','enterName')))
    driver.js('sessionStorage.setItem("login","{0}");'.format(configinit.getValue('session','login')))
    driver.js('sessionStorage.setItem("role","{0}");'.format(configinit.getValue('session','role')))
    driver.js('sessionStorage.setItem("carType","{0}");'.format(configinit.getValue('session','carType')))
    driver.js('sessionStorage.setItem("shipperUser",JSON.stringify({0}));'.format(configinit.getValue('session','shipperUser')))
    driver.js('sessionStorage.setItem("mainMenus",JSON.stringify({0}));'.format(configinit.getValue('session','mainMenus')))
    # driver.js('sessionStorage.setItem("navbar",JSON.stringify({0}));'.format(configinit.getValue('session', 'navbar')))
    driver.js('sessionStorage.setItem("username",JSON.stringify({0}));'.format(configinit.getValue('session', 'username')))
    driver.js('sessionStorage.setItem("mobile",JSON.stringify({0}));'.format(configinit.getValue('session', 'mobile')))
    driver.js('sessionStorage.setItem("name",JSON.stringify({0}));'.format(configinit.getValue('session', 'name')))

if __name__ == '__main__':
    configinit = ReadInit(FileUtil.getProjectObsPath() + '/config/config.init')
    print(configinit.getValue('session','enterName'))