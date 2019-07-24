# -*-coding:utf-8-*-

import random
import os
from datetime import date, timedelta
from util.file.fileutil import FileUtil

provinces = ['京', '津', '沪', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁', '新', '苏', '浙', '赣', '鄂', '桂',
             '甘', '晋', '蒙', '陕', '吉', '闽', '贵', '粤', '青', '藏', '川', '宁', '琼']
carLengths = ["4.2", "5.0", "6.2", "6.8", "7.6", "8.6", "9.6", "11.7", "12.5", "13.0", "15.0", "16.0", "17.5", "21.0"]
carTypeInfos = ["GAO_DI_BAN_CHE", "GAO_LAN_CHE", "PING_BAN_CHE", "TE_ZHONG_CHE", "XIANG_SHI_CHE", "GUA_CHE",
                "BAN_GUA_CHE", "LENG_CANG_CHE", "DA_JIAN_CHE", "QI_TA"]


class DataUtil(object):
    def __init__(self):
        self.codelist = []
        self.getdistrictcode()

    # 随机生成手机号
    def createmoble(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "170", "172", "176", "178", "177", "180", "181", "182",
                   "183", "184","185", "186", "187", "188", "189"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    # 随机生成身份证号
    def getdistrictcode(self):
        # 读取地区编码
        self.distfile = FileUtil.getProjectObsPath() + os.path.sep + 'config' + os.path.sep + 'districtcode.txt'
        with open(self.distfile,encoding = "ISO-8859-1") as file:
            data = file.read()
            districtlist = data.split('\n')
        for node in districtlist:
            if node[10:11] != ' ':
                state = node[10:].strip()
            if node[10:11] == ' ' and node[12:13] != ' ':
                city = node[12:].strip()
            if node[10:11] == ' ' and node[12:13] == ' ':
                district = node[14:].strip()
                code = node[0:6]
                self.codelist.append({"state": state, "city": city, "district": district, "code": code})

    def genneratorIdNo(self):
        # 生成符合规则的身份证号
        if not self.codelist:
            self.getdistrictcode()
        id = self.codelist[random.randint(0, len(self.codelist))]['code']  # 地区项
        id = id + str(random.randint(1930, 2013))  # 年份项
        da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))  # ，顺序号简单处理

        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                     '10': '2'}  # 校验码映射
        for i in range(0, len(id)):
            count = count + int(id[i]) * weight[i]
            id = id + checkcode[str(count % 11)]  # 算出校验码
            return id

    # 随机生成车牌号
    def genneratorCarNo(self):
        province = random.sample(provinces, 1)  # 随机省份
        letter = [chr(random.randint(65, 90))]    # 随机大写字母
        code_list = []
        for i in range(10):   # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91):   # A-Z
            if chr(i) == 'O':
                pass
            else:
                code_list.append(chr(i))
        num_1 = random.sample(code_list, 1)      # 五位随机数字字母组合
        num_2 = random.sample(code_list, 1)
        num_3 = [str(random.randint(0, 9))]
        num_4 = [str(random.randint(0, 9))]
        num_5 = [str(random.randint(0, 9))]
        nums = num_1 + num_2 + num_3 + num_4 + num_5
        carNo = ''.join(province + letter + nums)
        return carNo

    # 随机选择车长
    def genneratorCarLength(self):
        carLength = random.sample(carLengths, 1)[0]
        return carLength

    # 随机选择车型
    def genneratorCarTypeInfo(self):
        carTypeInfo = random.sample(carTypeInfos, 1)[0]
        return carTypeInfo

    def genneratorCarInfo(self):
        carLength = random.sample(carLengths, 1)
        carTypeInfo = random.sample(carTypeInfos, 1)
        carInfo = carLength + carTypeInfo
        return carInfo


if __name__ == "__main__":
    id = DataUtil().genneratorCarNo()
    print(id)
