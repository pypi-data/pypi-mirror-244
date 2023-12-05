# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :
    Json TextGrid 互转
"""
import json
import os
from sdk.utils.util_file import FileProcess


class Tran():
    """

    """

    def __init__(self):
        self.file = FileProcess()
        self.fill_single = True

    def get_column(self, args: dict, key_lis: list) -> dict:
        """

        :param args:
        :param key_lis:
        :return:
        """
        headers = args["headers"]
        data = args["line"]
        res = {}
        for key in key_lis:
            res[key] = data[headers.index(key)]
        return res

    def save_result(self, file, data):
        """

        :param file:
        :param data:
        :return:
        """
        with open(file, "w", encoding="utf-8")as fp:
            fp.write(data)

    def get_answer(self, args: dict, answer_list: list = [
                   "验收答案", "拟合答案", "质检答案"]):
        """
        取答案
        :param args:FileProcess返回的dict
        :param answer_list:取答案顺序
        :return:
        """
        un_condition = ["-", "是", ""]
        for key in answer_list:
            answer = args["data"][args["headers"].index(key)]
            if answer not in un_condition:
                return answer
        num = args["num"]
        return "第 {} 行 答案为:{}".format(num, answer)

    def jsontrantext(self, file, save_path, answer_list=["最终答案"]):
        """

        :param file:
        :param save_path:
        :return:
        """
        os.makedirs(save_path, exist_ok=True)
        error_log_lis = []

        def _get_main(audioDuration, size, name):
            return """File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\nxmax = {}\ntiers? <exists>\nsize = 1\nitem []:\n\titem [1]:\n\t\tclass = "IntervalTier"\n \t\tname = "{}"\n \t\txmin = 0\n \t\txmax = {}\n\t\tintervals: size = {}\n""".format(
                audioDuration, name, audioDuration, size)

        def _get_items(num, xmin, xmax, text):
            return """\t\tintervals [{}]:\n\t\t\txmin = {}\n\t\t\txmax = {}\n\t\t\ttext = \"{}\"""".format(
                num, xmin, xmax, text)

        # data_json = self.file.read_json(file)
        for args in self.file.read_yield(file):
            answer = self.get_answer(args, answer_list)
            # data_map = self.get_col(args,["拟合答案"])
            # answer = data_map["拟合答案"]
            if not answer.startswith("第"):
                data_json = json.loads(answer)
                name = data_json["audioFileName"].split("/")[-1]
                audioDuration = data_json["audioDuration"]
                records = data_json["records"]
                item_lis = []
                history_head = [0, 0]
                num = 0
                for args in records:
                    _time = args["time"]
                    xmin = _time["begin"]
                    xmax = _time["end"]
                    # 补充开头空白和中间空白
                    if self.fill_single:
                        if xmin != history_head[-1]:
                            num += 1
                            _item = _get_items(num, history_head[-1], xmin, "")
                            item_lis.append(_item)
                            history_head = [history_head[-1], xmin]
                            del _item

                    num += 1
                    text = args["content"]
                    _item = _get_items(num, xmin, xmax, text)
                    history_head = [xmin, xmax]
                    item_lis.append(_item)
                    del _item

                # 补充结尾空白
                if self.fill_single:
                    if history_head[-1] < audioDuration:
                        num += 1
                        _item = _get_items(
                            num, history_head[-1], audioDuration, "")
                        item_lis.append(_item)
                        del _item

                size = len(item_lis)
                main_args = _get_main(audioDuration, size, name)
                main_args += "\n".join(item_lis)
                _save_path = os.path.join(save_path, "data")
                os.makedirs(_save_path, exist_ok=True)
                save_file = os.path.join(
                    _save_path, "{}.TxtGrid".format(name))
                self.save_result(save_file, main_args)
                del main_args
                print("成功保存:{}".format(save_file))
            else:
                error_msg = "文件:{} {}".format(file, answer)
                print("[答案存在错误]:", error_msg)
                error_log_lis.append(error_msg)

        if error_log_lis:
            print("")
            print("|---------------------------------------------|")
            print("| >>>----请检查 error.txt 文件中的错误内容----<<< |")
            print("|---------------------------------------------|")
            print("")
            self.save_result("error.txt", "\n".join(error_log_lis))


if __name__ == '__main__':
    t = Tran()
    t.jsontrantext(
        R"D:\Desktop\1\平台导出8504912.txt",
        R"D:\Desktop\2")
