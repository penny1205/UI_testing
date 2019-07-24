# __author__ = ‘pan‘
# -*-coding:utf-8-*-
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

class HeplerWaybill(object):
    '''运单管理'''

    def open_menu(self,driver,menu_ele):
        '''打开菜单'''
        driver.element_is_not_visible('class->loading-bar-background')
        driver.move_to_click(menu_ele)
        driver.element_is_not_visible('class->loading-bar-background')

    def set_value_select_input(self,driver,input_ele,content):
        '''选择输入框'''
        driver.type(input_ele, content)
        time.sleep(2)
        driver.get_element(input_ele).send_keys(Keys.ENTER)
        driver.element_is_not_visible('class->modal-open')

    def set_value_address(self,driver,input_ele,province_ele,city_ele,district_ele):
        '''地址输入框'''
        driver.click(input_ele)
        driver.click(province_ele)
        driver.click(city_ele)
        driver.click(district_ele)

    def set_value_cargo(self,driver,cargoName,cargoWeight,cargoVolume,cargoCount,unit,cargoNo,cargoWorth,insuranceCosts):
        '''货物明细'''
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[2]/input",cargoName)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[3]/input", cargoWeight)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[4]/input", cargoVolume)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[5]/input", cargoCount)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[6]/input", unit)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[7]/input", cargoNo)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[8]/input", cargoWorth)
        driver.type("xpath->//*[@id='addWayBillDiv']/div/form/div[2]/div[2]/div/div[3]/ul/li[9]/input", insuranceCosts)

    def fuzzy_query(self,driver,type_ele,query_ele,content):
        '''模糊查询 '''
        #输入内容
        driver.type(type_ele, content)
        #点击查询按钮
        driver.retry_find_click(query_ele)
        driver.element_is_not_visible('class->loading-bar-background')

    def date_query(self,driver,start_time_ele='',ending_time_ele='',select_ele='',index='0'):
        '''按照日期查询'''
        if select_ele != None:
            Select(driver.get_element(select_ele)).select_by_index(index)
        else:
            driver.click(start_time_ele)
            driver.click(ending_time_ele)

    def input_query(self,driver,input_ele,content,query_ele):
        '''单个输入框查询'''
        driver.type(input_ele, content)
        driver.retry_find_click(query_ele)
        driver.element_is_not_visible('class->loading-bar-background')
        time.sleep(2)

    def select_query(self,driver,select_ele,index='0'):
        '''选择框查询'''
        Select(driver.get_element(select_ele)).select_by_index(index)

    def address_query(self,departure_ele,destination_ele):
        '''地址输入框查询'''

