# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
@代码日期    ：2023/12/5 21:35 
@本段代码的视频说明     ：
'''
from poai.core.AIArt import get_text2image_result


def text2image(id, key, prompt: str, output: str = r'./text2image.jpg'):
    """
    1行代码，生成AI绘画
    :param id:
    :param key:
    :param prompt:
    :param output:
    :return:
    """
    get_text2image_result(id, key, prompt, output)
