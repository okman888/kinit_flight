# -*- coding: utf-8 -*-
# @Time : 2025/12/23 15:28
# @Author: xixi
# @Instructions: 说明
# @remark: 备注
# @Software: Python 3.7.8
#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {'codetype': codetype}
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64': base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {'id': im_id}
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()



if __name__ == '__main__':
    pass
    import base64
    # chaojiying = Chaojiying_Client('2081540885', 'qwer1234', '9004')	   # 用户中心>>软件ID 生成一个替换 96001
    # chaojiying = Chaojiying_Client('ttuser', 'etwin2018', '907333')	   # 用户中心>>软件ID 生成一个替换 96001
    # # img_path = 'D:\\pycharm_obj\\gitlab\\crawler_python\\crawler_captcha\\geetest\\geetest4_click\\img\\new_bg.png'
    # img_path = 'D:\\pycharm_obj\\gitlab\\crawler_python\\crawler_captcha\\geetest\\geetest4_click\\img\\test.png'
    # with open(img_path, 'rb') as f:
    #     base64_data = base64.b64encode(f.read())
    #     b64 = base64_data.decode()
    # print(chaojiying.PostPic_base64(b64, 9004))  # 此处为传入 base64代码


    # from curl_cffi import requests as curl
    # # 获取 提交选择航班验证码 不需要ck
    # headers = {
    #     'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    #     'cache-control': 'no-cache',
    #     'pragma': 'no-cache',
    #     'priority': 'u=2, i',
    #     'referer': 'https://secure2.lionair.co.id/LionAirIBE2/OnlineBooking.aspx',
    #     'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'image',
    #     'sec-fetch-mode': 'no-cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # }
    # resp = curl.get('https://secure2.lionair.co.id/LionAirIBE2/CaptchaGenerator.aspx',
    #                     impersonate='chrome133a',
    #                     headers=headers)
    # with open("./sl.png", 'wb') as fp:
    #     fp.write(resp.content)
    # base64_data = base64.b64encode(resp.content)
    # b64 = base64_data.decode()
    # # print(chaojiying.PostPic_base64(b64, 1006))  # 此处为传入 base64代码
    # print(chaojiying.PostPic(resp.content, 1006))
