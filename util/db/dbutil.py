# __author__ = 'pan'
# -*- coding:utf-8 -*-

import pymysql
from util.log.log import Log

class DBUtil(object):
    '''操作数据库'''

    def __init__(self,host,port,user,passwd,dbname,charset):
        self.logger = Log()
        try:
            self.connect = pymysql.Connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = dbname,
                charset = charset
            )
        except Exception as e:
            self.logger.error('Database Initialization Connection Failed 1 : {0}'.format(e))
            raise

    def execute_sql(self,sql):
        '''执行sql语句'''
        self.logger.info('sql:{0}'.format(sql))
        try:
            cur = self.connect.cursor()
            cur.execute(sql)
            cur.close()
            self.connect.commit()
            self.connect.close()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.rollback()
            self.connect.close()
            raise

    def excute_select_one_record(self,query):
        '''执行sql语句：select,返回结果只包含一条数据'''
        self.logger.info('query:{0}'.format(query))
        try:
            cur = self.connect.cursor()
            cur.execute(query)
            return cur.fetchone()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.close()
            raise

    def excute_select_many_record(self,query):
        '''执行sql语句：select，返回结果包含多条数据'''
        self.logger.info('query:{0}'.format(query))
        try:
            cur = self.connect.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.close()
            raise