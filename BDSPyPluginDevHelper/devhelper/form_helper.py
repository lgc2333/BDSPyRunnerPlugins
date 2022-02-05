"""
FormHelper

帮助开发者更高效地构建GUI窗体

一定程度上借鉴 https://www.minebbs.com/resources/bds-pyrhelper-gui-_-_.3030/
"""
import json
from typing import List, Dict, Any


class Form(list):
    def __init__(self, title: str = None, objects: List[Dict[str, Any]] = None):
        super().__init__()
        self.title = 'Form'
        if title:
            self.title = title
        if objects:
            if isinstance(objects, list):
                self.extend(objects)
            else:
                raise ValueError("'objects' param should be 'dict' (List[Dict[str, Any]])")

    def get_form_json(self):
        """
        将类中控件格式化为json文本

        :return: 窗体json文本
        """
        return json.dumps({"content": self, "type": "custom_form", "title": self.title})

    __str__ = get_form_json

    def add_label(self, text: str, insert_pos: int = None):
        """
        添加一个标签（纯文本）

        :param text: 文本内容
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"type": "label", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)

    def add_input(self, text: str, place_holder: str = '', insert_pos: int = None):
        """
        添加一个输入框

        :param place_holder: 水印文本
        :param text: 显示文本
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"placeholder": place_holder, "default": "", "type": "input", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)

    def add_toggle(self, text: str, state: bool = False, insert_pos: int = None):
        """
        添加一个开关

        :param state: 默认状态
        :param text: 右侧文本
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"default": state, "type": "toggle", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)

    def add_slider(self, text: str, min_pos: int = 0, max_pos: int = 10, step: int = 1, default: int = 0,
                   insert_pos: int = None):
        """
        添加一个滑块

        :param min_pos: 最小位置
        :param max_pos: 最大位置
        :param step: 每格间隔的位置
        :param default: 滑块默认位置
        :param text: 显示文本
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"min": min_pos, "max": max_pos, "step": step, "default": default, "type": "slider", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)

    def add_step_slider(self, text: str, steps: List[str], default: int = 0, insert_pos: int = None):
        """
        添加一个矩阵滑块

        :param default: 初始位置
        :param steps: 每个位置显示的名称
        :param text: 显示文本
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"default": default, "steps": steps, "type": "step_slider", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)

    def add_dropdown(self, text: str, options: List[str], default: int = 0, insert_pos: int = None):
        """
        添加一个下拉框

        :param default: 初始选项
        :param options: 选项内容
        :param text: 显示文本
        :param insert_pos: 如要插入到特定位置请传入要插入的位置
        """
        obj = {"default": default, "options": options, "type": "dropdown", "text": text}
        if insert_pos is None:
            self.append(obj)
        else:
            self.insert(insert_pos, obj)
