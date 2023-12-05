#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: base_db.py
@time: 2023/6/19 21:34
@desc:
"""
import pymysql
import traceback
from sdk.utils.util_decorate import DecorateSingle
from sdk.utils.util_log import LoggingProcess


@DecorateSingle
class BaseDB(object):
    """

    """

    def __init__(self, host: str, port: int,
                 username: str, password: str, db: str):
        # super(BaseDB, self).__init__()
        self.host = host
        self.port = port
        self.user = username
        self.password = password
        self.db = db

        log = LoggingProcess(file="./log/log.log", sign="BaseDB")
        self.logger = log.get_logger()

    def create_cursor(self):
        """

        :param host:
        :param port:
        :param username:
        :param password:
        :param db:
        :return:
        """
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
        )
        self.conn = conn
        self.cur = conn.cursor()
        self.logger.info("数据库链接对象初始化")

    def execute_sql(self, sql: str):
        """

        :param sql:
        :return:
        """
        try:
            update_nums = self.cur.execute(sql)
            if not sql.lower().startswith("select") and not sql.lower().startswith("show"):
                self.conn.commit()
                self.logger.info(
                    "{}\t成功 {} : {}".format(
                        sql, sql.split(" ")[0], update_nums))
                return update_nums
            result = self.get_result()
            self.logger.info("{}\t执行结果:{}".format(sql, result))
            return result
        except BaseException:
            self.logger.error(traceback.print_exc())
            self.conn.rollback()
            self.logger.info("回滚")

    def close(self):
        """

        :return:
        """
        self.cur.close()
        self.conn.close()
        self.logger.info("关闭数据库连接对象")

    def get_result(self):
        """

        :return:
        """
        result = self.cur.fetchall()
        self.logger.info("结果:{}".format(result))
        return result
