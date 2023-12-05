#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_excel.py
@time: 2023/5/27 23:37
@desc:
"""
from typing import List, Dict
import xlsxwriter
import xlrd
from sdk.base.base_temp import Base


class ExcelProcess(Base):
    """
    excel 读写
    """

    def __init__(self):
        super(ExcelProcess, self).__init__()

    def read_yield(self, file: str, headers: list = None,
                   encoding: str = "utf-8", spliter: str = "\t", sheets: list = None, headersline=[0]) -> dict:
        """
        按行读取excel
        :param file:
        :param headers:[[],[]]每个sheet对应一个header
        :param encoding:
        :param spliter:
        :param sheets:
        :return:
        """
        data = xlrd.open_workbook(file)
        if not sheets:
            sheets = data.sheet_names()
        for index, sheet in enumerate(sheets):
            table = data.sheet_by_name(sheet)
            nrows = table.nrows
            # 传headers进来从第1行开始算，不传从第2行开始算
            if not headers:
                header = []
                for id in headersline:
                    _header = table.row_values(id)
                    header.append(_header)
                    start = 1
            else:
                header = headers[index]
                start = 0
            num = 0
            for row in range(start, nrows):
                info = []
                for i in table.row_values(row):
                    if isinstance(i, str):
                        info.append(i)
                    else:
                        if str(i).endswith(".0"):
                            info.append(str(int(i)))
                        else:
                            info.append(str(i))
                num += 1

                yield {
                    "sheet": sheet,
                    "headers": header,
                    "num": num,
                    "line": info,
                }

    @staticmethod
    def write(file: str, data, headers, sheets,
              style_header: Dict = None):
        """
        excel 写入数据
        :param file:
        :param data:[[],[],[]……]
        :param header:["","","",]
        :param style_header:
        :param sheet:
            strings_to_numbers:str 类型数字转换为 int 数字
            strings_to_urls:自动识别超链接
            constant_memory:续内存模式 (True 适用于大数据量输出)
            font_name:字体. 默认值 "Arial"
            font_size:字号. 默认值 11
            text_wrap:单元格内是否自动换行
            bold:字体加粗
            border:单元格边框宽度. 默认值 0
            align:对齐方式
            valign:垂直对齐方式
            text_wrap:单元格内是否自动换行

        :return:
        """
        # 全局样式
        options = {
            'strings_to_numbers': False,
            'strings_to_urls': True,
            'constant_memory': False,
            'default_format_properties': {
                'font_name': '微软雅黑',
                'font_size': 11,
                'bold': False,
                'border': 0,
                'align': 'left',
                'valign': 'vcenter',
                'text_wrap': False,
            },
        }
        workbook = xlsxwriter.Workbook(file, options)
        for index, sheet in enumerate(sheets):
            worksheet = workbook.add_worksheet(sheet)
            # 拼接header 第一行
            data[index].insert(0, headers[index])
            for row, lis in enumerate(data[index]):
                for col, val in enumerate(lis):
                    # header 样式
                    if row == 0:
                        cell_format = workbook.add_format(style_header)
                    else:
                        cell_format = None
                    worksheet.write_string(
                        row=row,
                        col=col,
                        string=str(val),
                        cell_format=cell_format,
                    )
        workbook.close()
