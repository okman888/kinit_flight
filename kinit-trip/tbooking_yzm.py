# -*- coding: utf-8 -*-
# @Time : 2025/6/6 14:39
# @Author: sunwei
# @Instructions: 说明
# @remark: 备注
# @Software: Python 3.7.8
import datetime
import hashlib
import json
import math
import os
import random
import time
import uuid
import numpy as np
import base64
import cv2
import ddddocr
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from loguru import logger
import traceback
from chaojiying_dome import Chaojiying_Client

abs_path = os.path.dirname(os.path.abspath(__file__))


class CtripCaptchaSolver:
    def __init__(self, log, session, appid, business_site, version, type="tbooking", proxies=None):
        self.log = log
        self.session = session
        # self.session = requests.Session()
        try:
            # 使用最新版本 ddddocr API - SlideEngine
            self.ocr = ddddocr.SlideEngine()
        except Exception as e:
            # 如果初始化失败，记录错误
            self.log.error(f"Failed to initialize SlideEngine: {str(e)}")
            # 设置为None，后续代码需要处理这种情况
            self.ocr = None
        self.origin = "https://ic.trip.com"  # 非国内携程
        # self.ip = self.get_proxy()
        self.session.proxies = proxies
        self.vid = self.unique_id()
        self.r = self.match_r()
        self.real_ip = self.match_ip()
        self.appid = appid
        self.business_site = business_site
        self.version = version
        self.imgesPath = f"{os.path.abspath(os.path.dirname(__file__))}/images/"
        self.pingtu_1_path = f"{self.imgesPath}/ctrip_pingtu_1.png"
        self.pingtu_2_path = f"{self.imgesPath}/ctrip_pingtu_2.png"
        self.pingjie_img_path = f"{self.imgesPath}/ctrip_pingjie.png"

    def chaojiying_utils(self, img_path, codetype):
        # chaojiying = Chaojiying_Client('ooshine', 'g24wwyy1', '976339')  # 用户中心>>软件ID 生成一个替换 96001
        chaojiying = Chaojiying_Client('2081540885', 'qwer1234', '9004')	   # 用户中心>>软件ID 生成一个替换 96001
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        json_data = chaojiying.PostPic_base64(b64, codetype)
        pic_str = json_data['pic_str']
        self.log.info(f"当前识别结果:{pic_str}")
        return pic_str

    def get_proxy(self):
        try:
            url = 'https://share.proxy.qg.net/pool?key=768261E0&num=1&area=&isp=0&format=json&distinct=true'
            res = requests.get(url).json()
            data = res.get('data')
            for ip_ in data:
                sometimes = (datetime.datetime.strptime(ip_.get('deadline'),
                                                        "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).seconds
                if sometimes > 100:
                    server = ip_.get('server')
                    ip = {'http': f'http://{server}', 'https': f'http://{server}'}
                    print(f'{ip} 有效时间：{sometimes}')
                    return ip
        except Exception as e:
            self.log.info(f"{str(e)}")

    def match_r(self):
        try:
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": self.origin,
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": self.origin,
                "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "sec-fetch-storage-access": "active",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            }
            url = "https://cdid.c-ctrip.com/chloro-device/v2/d"
            data = {
                "data": "AwdgRgHM3AJgZtATI6AWGmtYkgnMAIzBKFQCG85EUxWhArAwRnAMZj3A3lzlhsyEWGEIBmCGljAxY JHIMIYNCBoBTbFswQ1wNGNBQ0ZPQbJkiVqDe5IYGVleQkudZ XvByl2jGLEcvBerpgAbPBSESDkYXhhbAlhhChiDEjqhvZIEAwgcWHqYWjRICBi9mjqDGj2YuIkmTJg9nkFmWFiBi1GYp21eJWEIKDASUz5DGFIaGBxILXwabJiIBkr0ySSKrloUmhsSIdjifFz6fqTnWFzwYP6fbpIEWGwYelL4rJrTeuNWcAGH1CGFQcNnoMlkDvutZGEZCQkJwSNJgHgoNBFPo9pspgU8pM1tBCHgovFVs94OUXmEFpUpiVJq1sSVWqD4gT3kSXPoIsQCLSrs98mwKoQEPomLsGPBrqcRjLrrL1As1i9Dll1OQ0FKaoq srqXkkPlkgt5qCmLKSnlQCUIPBCDqlHrrVy7WFcrK okQbARkgGOpJLqdVSxrK2CB4vllYrZaDaX08mG5clXgHpiMQJpndKqTa1Krje9FW88Gs1VTA96kn6FQWIoqGbT3iIqlMZdSIOnCzXCtExsbyiN3p1zRXLYr4iq 6PI2aSvFlUhyOo2GhIkw0lTgRmTqWqWC1fEQc9EnkxLAN1ugV3Hr2uf3-VMo0vqfWD1b2ubhxG6xOLzqMQSLBimNQzAsbD6kkFaAt6ICvgkirvqsJQgkUyaGGKZpHBYeCEIcsDqNUCwQaoBxdv UYxkBZYvDa6h4OBtQUdBu6-gOfTxOxv5FqoJYzrSMCcjOKwhNqjxVq87x1F8qzACosYvCKsn6EJFRFOU6S-FsbRCSUVJlBU jVLUMgNH8Yg9PphR9F01n2Go9kDEM2Zfm0UwzHMFaLMsMKZHC2TbGguz7IcxywTcamqGOfS3PglRSZSMkfPUKw-JqWWuEC6bHhCqTQhSgV9NwVRcqo9lmkOdpvFSsQ8XWIm2SVrSxVM8URNwFTYTIsgWdhIzhJ50yzPMGDQUKY2 a0U1QU6sWyrKqkXGgGkZMFi0qeM AMBuTrqGxOqbcpy07ccUyIUkcwYXJsJ-MFQJlAUtI6g IJ9pUhbstcFw5E9XkxE ESJVshjOQivUGIYezHYMgwXas TxK9uU9h9T72MUJ6msaiWBnNBx1EgD1bJuo5TIdUH0kCdSaQCBietJ5ZXbA CyCNkFE5clFdMczombIVmuDk5NDoUbE0yZbFAtzAt06TjNPC8LNTGzBCYEI1wYcUBTob YjkOl5QQBI6WM6sZvmfUTkMgGMhIOl8l4Bl6VAikfUSMUhjTA5PbTLAltPRISCBwYBiy6HXudMmofJJbjumy75SOxjoLPDpSS1iCxz2XeKyuKqcFYz2HHma2lPA8MS5AXUhd4mqIJEohZQoNzA4ps91Y3HHBojtbLuD2izj BW6RsBA66wBAlia2PRyTxAeCaEwq-OOA4DaOglsLDP-L kUsCxPAeCHAw0gt8k8DBGUIBH2MYCGMSYT8GAQA",
                "version": "7",
                "serverName": self.origin
            }
            response = self.session.post(url, headers=headers, data=data)
            text = response.text
            r = text.split("|")[0].replace("-", "")
            return r
        except Exception as e:
            self.log.error(f"获取r参数失败：{str(e)}")

    def match_ip(self):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": self.origin,
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": self.origin,
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-fetch-storage-access": "active",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        url = "https://cdid.c-ctrip.com/model-poc2/h"
        data = {
            "requestId": "3098b088b03c493bbc3cfd6ba0e971f5_21",
            "serverName": self.origin
        }
        response = self.session.post(url, headers=headers, data=data)
        return response.text

    def encrypt_with_fixed_iv(self, plaintext):
        # 固定 IV
        iv_hex = '69783956775867344e5853626b645431'
        iv = binascii.unhexlify(iv_hex)

        # 硬编码的密钥 (对应 words 数组)
        # 原始密钥是 16 字节 (128 位)，由 4 个 32 位整数组成
        key_words = [
            -0x70dca43f,  # 32-bit signed integer
            -0x353e85ba,  # 32-bit signed integer
            0x530c616f,  # 32-bit signed integer
            -0xdcb4188,  # 32-bit signed integer
            -0x14f88411  # 32-bit signed integer
        ]

        # 将每个 32 位整数转换为 4 字节（大端序）
        key_bytes = b''
        for word in key_words:
            # 使用 0xFFFFFFFF 掩码确保 32 位，然后转换为无符号整数
            unsigned_word = word & 0xFFFFFFFF
            key_bytes += unsigned_word.to_bytes(4, 'big')

        # 只取前 16 字节（AES-128）
        key_bytes = key_bytes[:16]

        # AES-CBC 加密
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)

        # 返回 Base64 编码的结果（与 CryptoJS 一致）
        import base64
        return base64.b64encode(ciphertext).decode('utf-8')

    def y_hash(self, e=None):
        if e is None:
            t = ['Netscape',
                 "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                 "zh-cn", "Win32",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                 0, 3000, "24-bit", "", ""]
            t = "".join(map(str, t))
            e = 3
            n = len(t)
            while e > 0:
                t += str(e ^ n)
                e -= 1
                n += 1
            e = t

        i = 1
        if not e:
            return i

        i = 0
        for n in range(len(e) - 1, -1, -1):
            t = ord(e[n])
            i = (i << 6) & 0xFFFFFFF
            i += t + (t << 14)
            mask = 0xFE00000
            t = i & mask
            if t != 0:
                i ^= (t >> 21)
        return i

    def int_to_base36(self, num):
        """将整数转换为 Base36 字符串（模拟 JS 的 toString(36)）"""
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        base36 = []
        if num == 0:
            return "0"
        while num != 0:
            num, rem = divmod(num, 36)
            base36.append(alphabet[rem])
        return ''.join(reversed(base36))

    def unique_id(self):
        rand_str = str(random.random())
        decimal_part = rand_str.split('.')[1]
        if len(decimal_part) < 8:
            decimal_part = decimal_part.ljust(8, '0')
        rand_val = int(decimal_part[-8:])  # 模拟 Y.getRand()
        hash_val = self.y_hash()  # 模拟 Y.CLI.getHash()
        result = rand_val ^ 0x7FFFFFFF & hash_val  # 2147483647 = 0x7FFFFFFF
        return f"{str(int(time.time() * 1000))}.{self.int_to_base36(result)}"  # 转换为 Base36

    def _0x42f251(self, s, e, str):
        _0x15c35d = ['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
                     'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                     '0123456789',
                     '0123456789abcdef']
        _0x1925c8 = _0x15c35d[e]
        _0xd1c1e9 = len(_0x1925c8)
        # 生成随机字符串
        result = ''
        for _ in range(s):
            # 随机选择字符
            random_index = math.floor(random.random() * _0xd1c1e9)
            result += _0x1925c8[random_index]
        return result

    def request_img(self):
        _0x3bbca9 = {
            'rt': f"fp=p51r8v-29do8p-qcu183&vid={self.vid}&pageId=&r={self.r}&ip={self.real_ip}&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36&d={self.origin.replace('https://', '')}&v=25&kpg=0_0_0_0_0_0_0_0_0_0&adblock=F&cck=F",
            'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'p': "pc",
            'fp': 'D5A79A-5EDF21-AE8DF7',
            'vid': self.vid,
            'identify': 'D5A79A-5EDF21-AE8DF7',
            'guid': str(uuid.uuid4()),
            'h5_duid': None,
            'pc_duid': None,
            'hb_uid': None,
            'pc_uid': None,
            'h5_uid': None,
            'infosec_openid': None,
            'device_id': self._0x42f251(0x20, 0x3, '_bfs'),
            'client_id': self._0x42f251(0x20, 0x0, '_bfi'),
            'pid': self._0x42f251(0x10, 0x2, 'corpid'),
            'sid': self._0x42f251(0x10, 0x1, 'SMBID'),
            'login_uid': self._0x42f251(0xa, 0x2, 'login_uid'),
            'client_type': 'PC'
        }
        _0x3bbca9['site'] = {
            "type": "PC",
            "url": f"{self.origin}/#/user/login/CN",
            "ref": "",
            "title": "Partner Portal",
            "keywords": ""
        }
        _0x3bbca9['device'] = {
            "width": 1920,
            "height": 1080,
            "os": "",
            "pixelRatio": 1,
            "did": ""
        }
        _0x3bbca9['user'] = {
            "tid": "",
            "uid": "",
            "vid": ""
        }
        result = self.encrypt_with_fixed_iv(json.dumps(_0x3bbca9, separators=(",", ":")))
        text = f"appid={self.appid}&business_site={self.business_site}&version={self.version}&dimensions={result}&extend_param=ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN00C+H3pGS0QkTS+cybU5kHGoF2BK4PqNKEZeBioYzoyA="
        md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://tbooking.trip.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://tbooking.trip.com/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        }
        url = "https://ic.trip.com/captcha/v4/risk_inspect"
        data = {
            "extend_param": "ak7Oj2doYMHGkXZ9ST5pJogOCCG%2F%2F%2FHWQ%2FKl32rGeNM002Mgcr3MiJwWHR9bljN00C%2BH3pGS0QkTS%2BcybU5kHGoF2BK4PqNKEZeBioYzoyA%3D",
            "appid": self.appid,
            "business_site": self.business_site,
            "version": self.version,
            "dimensions": result,
            "sign": md5_hash,
            "t": int(time.time() * 1000)
        }
        data = json.dumps(data, separators=(',', ':'))
        response = self.session.post(url, headers=headers, data=data)
        json_data = response.json()
        return json_data

    def hand_img(self, json_data):
        if json_data['message'] == 'Success':
            self.log.info("正在处理滑动图片")
            json_result = json_data['result']
            rid = json_result['rid']
            token = json_result['token']
            # 获取三张图片
            risk_info = json_result['risk_info']
            jigsaw_image = risk_info['process_value']['jigsaw_image']
            original_image = risk_info['process_value']['original_image']
            processed_image = risk_info['process_value']['processed_image']
            # 解码 Base64
            jigsaw_image_data = base64.b64decode(jigsaw_image.split(",")[-1] if "," in jigsaw_image else jigsaw_image)
            original_image_data = base64.b64decode(
                original_image.split(",")[-1] if "," in original_image else original_image)
            processed_image_data = base64.b64decode(
                processed_image.split(",")[-1] if "," in processed_image else processed_image)
            # 保存为图片文件
            with open(f"{abs_path}/img/jigsaw.png", "wb") as f:
                f.write(jigsaw_image_data)
            with open(f"{abs_path}/img/original.png", "wb") as f:
                f.write(original_image_data)
            with open(f"{abs_path}/img/processed.png", "wb") as f:
                f.write(processed_image_data)

            # 预处理背景图和滑块图
            bg_processed = self.preprocess_image(f'{abs_path}/img/processed.png')
            slider_processed = self.preprocess_image(f'{abs_path}/img/jigsaw.png')

            # 保存预处理后的图片（可选）
            cv2.imwrite(f'{abs_path}/img/bg_processed.png', bg_processed)
            cv2.imwrite(f'{abs_path}/img/slider_processed.png', slider_processed)

            # 使用 SlideEngine 进行滑块匹配
            det = ddddocr.SlideEngine()
            with open(f"{abs_path}/img/bg_processed.png", 'rb') as f_bg, open(f"{abs_path}/img/slider_processed.png", 'rb') as f_slider:
                bg_bytes = f_bg.read()
                slider_bytes = f_slider.read()
                # 使用 SlideEngine 的 match 方法
                res = det.match(slider_bytes, bg_bytes)
                gap_x = res['target'][0]
                gap_y = 0  # 若需y坐标，需通过其他方式获取
            # 读取滑块图尺寸作为缺口大小
            slider_img = cv2.imread(f"{abs_path}/img/slider_processed.png")
            gap_width, gap_height = slider_img.shape[1], slider_img.shape[0]

            # 标注并保存
            rectangle_x = gap_x
            rectangle_max_x = rectangle_x + gap_width
            bg_img = cv2.imread(f"{abs_path}/img/bg_processed.png")
            cv2.rectangle(
                bg_img,
                (rectangle_x, gap_y),
                (rectangle_max_x, gap_y + gap_height),
                (0, 0, 255), 2
            )
            cv2.imwrite(f"{abs_path}/img/marked.png", bg_img)
            self.log.info(f"缺口位置: x={gap_x}, 尺寸={gap_width}x{gap_height}")

            x_value = int(rectangle_x / 388 * 300) + 54
            # x_value =
            # self.log.info(x_value)
            return x_value, rid, token

    def preprocess_image(self, image_path):
        """预处理验证码图片"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 205, 255, cv2.THRESH_BINARY)
        denoised = cv2.medianBlur(binary, 3)
        return denoised

    def hand_track(self, x_value):
        try:
            x, rid, token = x_value
            img_dict_param = {
                "st": int(time.time() * 1000),
                "slidingTime": 1302,
                "display": "1920x1080",
                "keykoardTrack": [],
                "jigsawKeyboardEventExist": True,
                "jigsawPicWidth": 388,
                "jigsawPicHeight": 194,
                "jigsawViewDuration": 2637817,
                "slidingTrack": [
                    {
                        "x": 795,
                        "y": 146
                    },
                    {
                        "x": 799,
                        "y": 146
                    },
                    {
                        "x": 810,
                        "y": 146
                    },
                    {
                        "x": 829,
                        "y": 147
                    },
                    {
                        "x": 853,
                        "y": 147
                    },
                    {
                        "x": 875,
                        "y": 147
                    },
                    {
                        "x": 895,
                        "y": 147
                    },
                    {
                        "x": 910,
                        "y": 145
                    },
                    {
                        "x": 921,
                        "y": 143
                    },
                    {
                        "x": 929,
                        "y": 141
                    },
                    {
                        "x": 936,
                        "y": 140
                    },
                    {
                        "x": 941,
                        "y": 139
                    },
                    {
                        "x": 943,
                        "y": 138
                    },
                    {
                        "x": 944,
                        "y": 138
                    },
                    {
                        "x": 945,
                        "y": 138
                    },
                    {
                        "x": 946,
                        "y": 137
                    },
                    {
                        "x": 948,
                        "y": 137
                    },
                    {
                        "x": 951,
                        "y": 137
                    },
                    {
                        "x": 955,
                        "y": 137
                    },
                    {
                        "x": 959,
                        "y": 137
                    },
                    {
                        "x": 962,
                        "y": 137
                    },
                    {
                        "x": 965,
                        "y": 137
                    },
                    {
                        "x": 966,
                        "y": 137
                    },
                    {
                        "x": 967,
                        "y": 137
                    },
                    {
                        "x": 968,
                        "y": 136
                    },
                    {
                        "x": 971,
                        "y": 136
                    },
                    {
                        "x": 978,
                        "y": 136
                    },
                    {
                        "x": 988,
                        "y": 137
                    },
                    {
                        "x": 996,
                        "y": 137
                    },
                    {
                        "x": 1004,
                        "y": 137
                    },
                    {
                        "x": 1012,
                        "y": 138
                    },
                    {
                        "x": 1017,
                        "y": 139
                    },
                    {
                        "x": 1020,
                        "y": 139
                    },
                    {
                        "x": 1021,
                        "y": 138
                    },
                    {
                        "x": 1022,
                        "y": 138
                    },
                    {
                        "x": 1024,
                        "y": 138
                    },
                    {
                        "x": 1027,
                        "y": 138
                    },
                    {
                        "x": 1030,
                        "y": 138
                    },
                    {
                        "x": 1033,
                        "y": 138
                    },
                    {
                        "x": 1034,
                        "y": 138
                    },
                    {
                        "x": 1035,
                        "y": 138
                    },
                    {
                        "x": 1036,
                        "y": 138
                    }
                ],
                "timezone": -480,
                "flashState": False,
                "language": "zh-CN",
                "platform": "Win32",
                "hasSessStorage": True,
                "hasLocalStorage": True,
                "hasIndexedDB": True,
                "hasDataBase": False,
                "doNotTrack": False,
                "touchSupport": False,
                "mediaStreamTrack": True,
                "value": x,
                "preJigsawSlidingTrack": [
                    {
                        "x": 607,
                        "y": 164,
                        "t": 1749604458247
                    },
                    {
                        "x": 605,
                        "y": 167,
                        "t": 1749604458256
                    },
                    {
                        "x": 603,
                        "y": 170,
                        "t": 1749604458264
                    },
                    {
                        "x": 599,
                        "y": 174,
                        "t": 1749604458272
                    },
                    {
                        "x": 595,
                        "y": 177,
                        "t": 1749604458281
                    },
                    {
                        "x": 591,
                        "y": 181,
                        "t": 1749604458288
                    },
                    {
                        "x": 585,
                        "y": 185,
                        "t": 1749604458297
                    },
                    {
                        "x": 576,
                        "y": 191,
                        "t": 1749604458304
                    },
                    {
                        "x": 563,
                        "y": 198,
                        "t": 1749604458312
                    },
                    {
                        "x": 548,
                        "y": 204,
                        "t": 1749604458320
                    },
                    {
                        "x": 532,
                        "y": 209,
                        "t": 1749604458328
                    },
                    {
                        "x": 510,
                        "y": 216,
                        "t": 1749604458335
                    },
                    {
                        "x": 480,
                        "y": 225,
                        "t": 1749604458344
                    },
                    {
                        "x": 447,
                        "y": 233,
                        "t": 1749604458351
                    },
                    {
                        "x": 423,
                        "y": 241,
                        "t": 1749604458360
                    },
                    {
                        "x": 403,
                        "y": 248,
                        "t": 1749604458367
                    },
                    {
                        "x": 385,
                        "y": 258,
                        "t": 1749604458376
                    },
                    {
                        "x": 371,
                        "y": 266,
                        "t": 1749604458384
                    },
                    {
                        "x": 363,
                        "y": 272,
                        "t": 1749604458392
                    },
                    {
                        "x": 358,
                        "y": 277,
                        "t": 1749604458400
                    },
                    {
                        "x": 355,
                        "y": 281,
                        "t": 1749604458408
                    },
                    {
                        "x": 353,
                        "y": 285,
                        "t": 1749604458415
                    },
                    {
                        "x": 352,
                        "y": 288,
                        "t": 1749604458423
                    },
                    {
                        "x": 352,
                        "y": 290,
                        "t": 1749604458431
                    },
                    {
                        "x": 350,
                        "y": 292,
                        "t": 1749604458440
                    },
                    {
                        "x": 349,
                        "y": 294,
                        "t": 1749604458448
                    },
                    {
                        "x": 347,
                        "y": 296,
                        "t": 1749604458456
                    },
                    {
                        "x": 346,
                        "y": 298,
                        "t": 1749604458464
                    },
                    {
                        "x": 344,
                        "y": 300,
                        "t": 1749604458472
                    },
                    {
                        "x": 344,
                        "y": 302,
                        "t": 1749604458480
                    },
                    {
                        "x": 343,
                        "y": 304,
                        "t": 1749604458487
                    },
                    {
                        "x": 342,
                        "y": 307,
                        "t": 1749604458495
                    },
                    {
                        "x": 341,
                        "y": 310,
                        "t": 1749604458504
                    },
                    {
                        "x": 340,
                        "y": 313,
                        "t": 1749604458511
                    },
                    {
                        "x": 339,
                        "y": 316,
                        "t": 1749604458519
                    },
                    {
                        "x": 338,
                        "y": 319,
                        "t": 1749604458528
                    },
                    {
                        "x": 337,
                        "y": 323,
                        "t": 1749604458536
                    },
                    {
                        "x": 449,
                        "y": 314,
                        "t": 1749604459312
                    },
                    {
                        "x": 521,
                        "y": 300,
                        "t": 1749604459319
                    },
                    {
                        "x": 596,
                        "y": 282,
                        "t": 1749604459328
                    },
                    {
                        "x": 669,
                        "y": 265,
                        "t": 1749604459335
                    },
                    {
                        "x": 736,
                        "y": 249,
                        "t": 1749604459344
                    },
                    {
                        "x": 795,
                        "y": 232,
                        "t": 1749604459352
                    },
                    {
                        "x": 839,
                        "y": 217,
                        "t": 1749604459360
                    },
                    {
                        "x": 870,
                        "y": 205,
                        "t": 1749604459369
                    },
                    {
                        "x": 890,
                        "y": 196,
                        "t": 1749604459376
                    },
                    {
                        "x": 901,
                        "y": 191,
                        "t": 1749604459384
                    },
                    {
                        "x": 906,
                        "y": 188,
                        "t": 1749604459391
                    },
                    {
                        "x": 907,
                        "y": 187,
                        "t": 1749604459399
                    },
                    {
                        "x": 908,
                        "y": 187,
                        "t": 1749604459448
                    },
                    {
                        "x": 908,
                        "y": 186,
                        "t": 1749604459456
                    },
                    {
                        "x": 908,
                        "y": 183,
                        "t": 1749604459464
                    },
                    {
                        "x": 908,
                        "y": 180,
                        "t": 1749604459472
                    },
                    {
                        "x": 906,
                        "y": 178,
                        "t": 1749604459480
                    },
                    {
                        "x": 905,
                        "y": 176,
                        "t": 1749604459488
                    },
                    {
                        "x": 903,
                        "y": 173,
                        "t": 1749604459498
                    },
                    {
                        "x": 902,
                        "y": 170,
                        "t": 1749604459504
                    },
                    {
                        "x": 900,
                        "y": 169,
                        "t": 1749604459512
                    },
                    {
                        "x": 896,
                        "y": 167,
                        "t": 1749604459520
                    },
                    {
                        "x": 894,
                        "y": 166,
                        "t": 1749604459528
                    },
                    {
                        "x": 893,
                        "y": 165,
                        "t": 1749604459536
                    },
                    {
                        "x": 892,
                        "y": 165,
                        "t": 1749604459568
                    },
                    {
                        "x": 892,
                        "y": 164,
                        "t": 1749604459576
                    },
                    {
                        "x": 890,
                        "y": 163,
                        "t": 1749604459584
                    },
                    {
                        "x": 888,
                        "y": 160,
                        "t": 1749604459592
                    },
                    {
                        "x": 885,
                        "y": 159,
                        "t": 1749604459600
                    },
                    {
                        "x": 880,
                        "y": 157,
                        "t": 1749604459608
                    },
                    {
                        "x": 874,
                        "y": 154,
                        "t": 1749604459616
                    },
                    {
                        "x": 867,
                        "y": 151,
                        "t": 1749604459624
                    },
                    {
                        "x": 859,
                        "y": 149,
                        "t": 1749604459632
                    },
                    {
                        "x": 852,
                        "y": 147,
                        "t": 1749604459640
                    },
                    {
                        "x": 846,
                        "y": 146,
                        "t": 1749604459647
                    },
                    {
                        "x": 841,
                        "y": 146,
                        "t": 1749604459656
                    },
                    {
                        "x": 835,
                        "y": 146,
                        "t": 1749604459664
                    },
                    {
                        "x": 831,
                        "y": 146,
                        "t": 1749604459673
                    },
                    {
                        "x": 828,
                        "y": 146,
                        "t": 1749604459680
                    },
                    {
                        "x": 826,
                        "y": 146,
                        "t": 1749604459688
                    },
                    {
                        "x": 824,
                        "y": 146,
                        "t": 1749604459696
                    },
                    {
                        "x": 822,
                        "y": 146,
                        "t": 1749604459704
                    },
                    {
                        "x": 820,
                        "y": 146,
                        "t": 1749604459712
                    },
                    {
                        "x": 819,
                        "y": 146,
                        "t": 1749604459719
                    },
                    {
                        "x": 818,
                        "y": 146,
                        "t": 1749604459728
                    },
                    {
                        "x": 817,
                        "y": 146,
                        "t": 1749604459737
                    },
                    {
                        "x": 815,
                        "y": 146,
                        "t": 1749604459743
                    },
                    {
                        "x": 814,
                        "y": 146,
                        "t": 1749604459751
                    },
                    {
                        "x": 813,
                        "y": 146,
                        "t": 1749604459760
                    },
                    {
                        "x": 811,
                        "y": 146,
                        "t": 1749604459767
                    },
                    {
                        "x": 810,
                        "y": 146,
                        "t": 1749604459776
                    },
                    {
                        "x": 809,
                        "y": 146,
                        "t": 1749604459784
                    },
                    {
                        "x": 808,
                        "y": 146,
                        "t": 1749604459792
                    },
                    {
                        "x": 806,
                        "y": 146,
                        "t": 1749604459801
                    },
                    {
                        "x": 805,
                        "y": 146,
                        "t": 1749604459807
                    },
                    {
                        "x": 804,
                        "y": 146,
                        "t": 1749604459824
                    },
                    {
                        "x": 802,
                        "y": 146,
                        "t": 1749604459832
                    },
                    {
                        "x": 801,
                        "y": 146,
                        "t": 1749604459848
                    },
                    {
                        "x": 800,
                        "y": 146,
                        "t": 1749604459856
                    },
                    {
                        "x": 799,
                        "y": 146,
                        "t": 1749604459872
                    },
                    {
                        "x": 798,
                        "y": 146,
                        "t": 1749604459880
                    },
                    {
                        "x": 796,
                        "y": 146,
                        "t": 1749604459888
                    },
                    {
                        "x": 795,
                        "y": 146,
                        "t": 1749604459904
                    }
                ],
                "jigsawSlidingTrack": [
                    {
                        "x": 795,
                        "y": 146,
                        "t": 1749604460018
                    },
                    {
                        "x": 799,
                        "y": 146,
                        "t": 1749604460104
                    },
                    {
                        "x": 810,
                        "y": 146,
                        "t": 1749604460111
                    },
                    {
                        "x": 829,
                        "y": 147,
                        "t": 1749604460119
                    },
                    {
                        "x": 853,
                        "y": 147,
                        "t": 1749604460127
                    },
                    {
                        "x": 875,
                        "y": 147,
                        "t": 1749604460136
                    },
                    {
                        "x": 895,
                        "y": 147,
                        "t": 1749604460143
                    },
                    {
                        "x": 910,
                        "y": 145,
                        "t": 1749604460151
                    },
                    {
                        "x": 921,
                        "y": 143,
                        "t": 1749604460159
                    },
                    {
                        "x": 929,
                        "y": 141,
                        "t": 1749604460168
                    },
                    {
                        "x": 936,
                        "y": 140,
                        "t": 1749604460176
                    },
                    {
                        "x": 941,
                        "y": 139,
                        "t": 1749604460184
                    },
                    {
                        "x": 943,
                        "y": 138,
                        "t": 1749604460191
                    },
                    {
                        "x": 944,
                        "y": 138,
                        "t": 1749604460199
                    },
                    {
                        "x": 945,
                        "y": 138,
                        "t": 1749604460207
                    },
                    {
                        "x": 946,
                        "y": 137,
                        "t": 1749604460215
                    },
                    {
                        "x": 948,
                        "y": 137,
                        "t": 1749604460231
                    },
                    {
                        "x": 951,
                        "y": 137,
                        "t": 1749604460239
                    },
                    {
                        "x": 955,
                        "y": 137,
                        "t": 1749604460247
                    },
                    {
                        "x": 959,
                        "y": 137,
                        "t": 1749604460255
                    },
                    {
                        "x": 962,
                        "y": 137,
                        "t": 1749604460264
                    },
                    {
                        "x": 965,
                        "y": 137,
                        "t": 1749604460271
                    },
                    {
                        "x": 966,
                        "y": 137,
                        "t": 1749604460280
                    },
                    {
                        "x": 967,
                        "y": 137,
                        "t": 1749604460287
                    },
                    {
                        "x": 968,
                        "y": 136,
                        "t": 1749604460303
                    },
                    {
                        "x": 971,
                        "y": 136,
                        "t": 1749604460408
                    },
                    {
                        "x": 978,
                        "y": 136,
                        "t": 1749604460415
                    },
                    {
                        "x": 988,
                        "y": 137,
                        "t": 1749604460423
                    },
                    {
                        "x": 996,
                        "y": 137,
                        "t": 1749604460431
                    },
                    {
                        "x": 1004,
                        "y": 137,
                        "t": 1749604460440
                    },
                    {
                        "x": 1012,
                        "y": 138,
                        "t": 1749604460447
                    },
                    {
                        "x": 1017,
                        "y": 139,
                        "t": 1749604460455
                    },
                    {
                        "x": 1020,
                        "y": 139,
                        "t": 1749604460463
                    },
                    {
                        "x": 1021,
                        "y": 138,
                        "t": 1749604460600
                    },
                    {
                        "x": 1022,
                        "y": 138,
                        "t": 1749604460608
                    },
                    {
                        "x": 1024,
                        "y": 138,
                        "t": 1749604460616
                    },
                    {
                        "x": 1027,
                        "y": 138,
                        "t": 1749604460624
                    },
                    {
                        "x": 1030,
                        "y": 138,
                        "t": 1749604460631
                    },
                    {
                        "x": 1033,
                        "y": 138,
                        "t": 1749604460640
                    },
                    {
                        "x": 1034,
                        "y": 138,
                        "t": 1749604460647
                    },
                    {
                        "x": 1035,
                        "y": 138,
                        "t": 1749604460832
                    },
                    {
                        "x": 1036,
                        "y": 138,
                        "t": 1749604460840
                    }
                ]
            }
            second_param = {
                "rt": f"fp=D5A79A-5EDF21-AE8DF7&vid={self.vid}&pageId=10651171056&r={self.r}&ip={self.real_ip}&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36&d={self.origin.replace('https://', '')}&v=25&kpg=0_0_0_0_0_0_0_0_0_0&adblock=F&cck=F",
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                "p": "pc", "fp": "p51r8v-29do8p-qcu183", "vid": self.vid,
                "sfp": "Q1sI%5C-%24%3D%7CyF%2BJE%5E%25r%5DJ0%3DIz%5E%25Mc9%5CN')IE",
                "identify": "aQOxwSkcU3kUqQLqT0uyVCrM00ZniKQQZaPKQyd8w2Ak=",
                "svid": "SO.%3CL%60%24C%7D%24E%2CFD%23%25x%7DIFC1U.'%2B",
                "guid": "6e2b8b33-f65a-451f-a57f-e106b9924934",
                "h5_duid": None, "pc_duid": None, "hb_uid": None, "pc_uid": None, "h5_uid": None,
                "infosec_openid": None,
                "device_id": "1c7bb78a6c483d789c2815470e292ff8", "client_id": "VocHubCNZo4TX2YxIo9KgueeTQxCCXhB",
                "pid": "6902964319144732", "sid": "jmCApXZfEKpQyQtl", "login_uid": "2968015945", "client_type": "PC",
                "site": {"type": "PC", "url": f"{self.origin}/#/user/login/CN", "ref": "",
                         "title": "Partner Portal", "keywords": ""},
                "device": {"width": 1920, "height": 1080, "os": "", "pixelRatio": 1, "did": ""},
                "user": {"tid": "", "uid": "", "vid": ""}}
            second_dimensions = self.encrypt_with_fixed_iv(json.dumps(second_param, separators=(",", ":")))

            img_result = self.encrypt_with_fixed_iv(json.dumps(img_dict_param, separators=(",", ":")))
            img_text = f"appid={self.appid}&business_site={self.business_site}&version={self.version}&verify_msg={img_result}&dimensions={second_dimensions}&extend_param=ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN00C+H3pGS0QkTS+cybU5kHGoF2BK4PqNKEZeBioYzoyA=&token={token}&captcha_type=JIGSAW"
            x_sign = hashlib.md5(img_text.encode('utf-8')).hexdigest()
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/json;charset=UTF-8",
                "origin": self.origin,
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": self.origin,
                "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            }
            url = "https://ic.trip.com/captcha/v4/verify_jigsaw"
            data = {
                "appid": self.appid,
                "business_site": self.business_site,
                "token": token,
                "rid": rid,
                "version": self.version,
                "verify_msg": img_result,
                "dimensions": second_dimensions,
                "extend_param": "ak7Oj2doYMHGkXZ9ST5pJogOCCG%2F%2F%2FHWQ%2FKl32rGeNM002Mgcr3MiJwWHR9bljN00C%2BH3pGS0QkTS%2BcybU5kHGoF2BK4PqNKEZeBioYzoyA%3D",
                "sign": x_sign,
                "t": int(time.time() * 1000)
            }
            data = json.dumps(data, separators=(',', ':'))
            response = requests.post(url, headers=headers, data=data)
            json_data = response.json()
            return json_data
        except Exception as e:
            self.log.error(f"滑动验证请求失败：{str(e)}")

    def hand_click(self, x_value):
        try:
            self.log.info("处理点击验证码")
            x, rid, token = x_value
            img_dict_param = {
                "st": int(time.time() * 1000),
                "display": "1920x1080",
                "keykoardTrack": [],
                "iconKeyboardEventExist": True,
                "iconViewDuration": 29443,
                "timezone": -480,
                "flashState": False,
                "language": "zh-CN",
                "platform": "Win32",
                "hasSessStorage": True,
                "hasLocalStorage": True,
                "hasIndexedDB": True,
                "hasDataBase": False,
                "doNotTrack": False,
                "touchSupport": False,
                "mediaStreamTrack": True,
                "preIconClickTrack": [
                    {
                        "x": 881,
                        "y": 136,
                        "t": 1749635375670
                    },
                    {
                        "x": 878,
                        "y": 136,
                        "t": 1749635375678
                    },
                    {
                        "x": 875,
                        "y": 135,
                        "t": 1749635375688
                    },
                    {
                        "x": 873,
                        "y": 134,
                        "t": 1749635375694
                    },
                    {
                        "x": 870,
                        "y": 133,
                        "t": 1749635375703
                    },
                    {
                        "x": 868,
                        "y": 132,
                        "t": 1749635375710
                    },
                    {
                        "x": 867,
                        "y": 131,
                        "t": 1749635375719
                    },
                    {
                        "x": 865,
                        "y": 131,
                        "t": 1749635375726
                    },
                    {
                        "x": 862,
                        "y": 129,
                        "t": 1749635375734
                    },
                    {
                        "x": 859,
                        "y": 128,
                        "t": 1749635375742
                    },
                    {
                        "x": 855,
                        "y": 127,
                        "t": 1749635375751
                    },
                    {
                        "x": 850,
                        "y": 126,
                        "t": 1749635375758
                    },
                    {
                        "x": 845,
                        "y": 125,
                        "t": 1749635375766
                    },
                    {
                        "x": 839,
                        "y": 124,
                        "t": 1749635375774
                    },
                    {
                        "x": 835,
                        "y": 123,
                        "t": 1749635375782
                    },
                    {
                        "x": 832,
                        "y": 122,
                        "t": 1749635375790
                    },
                    {
                        "x": 829,
                        "y": 121,
                        "t": 1749635375798
                    },
                    {
                        "x": 826,
                        "y": 121,
                        "t": 1749635375806
                    },
                    {
                        "x": 823,
                        "y": 120,
                        "t": 1749635375814
                    },
                    {
                        "x": 823,
                        "y": 119,
                        "t": 1749635375822
                    },
                    {
                        "x": 822,
                        "y": 119,
                        "t": 1749635375830
                    },
                    {
                        "x": 824,
                        "y": 119,
                        "t": 1749635376774
                    },
                    {
                        "x": 826,
                        "y": 119,
                        "t": 1749635376782
                    },
                    {
                        "x": 831,
                        "y": 120,
                        "t": 1749635376790
                    },
                    {
                        "x": 838,
                        "y": 122,
                        "t": 1749635376798
                    },
                    {
                        "x": 845,
                        "y": 123,
                        "t": 1749635376806
                    },
                    {
                        "x": 852,
                        "y": 124,
                        "t": 1749635376814
                    },
                    {
                        "x": 859,
                        "y": 125,
                        "t": 1749635376822
                    },
                    {
                        "x": 866,
                        "y": 127,
                        "t": 1749635376830
                    },
                    {
                        "x": 872,
                        "y": 129,
                        "t": 1749635376838
                    },
                    {
                        "x": 876,
                        "y": 130,
                        "t": 1749635376846
                    },
                    {
                        "x": 880,
                        "y": 131,
                        "t": 1749635376854
                    },
                    {
                        "x": 885,
                        "y": 132,
                        "t": 1749635376862
                    },
                    {
                        "x": 888,
                        "y": 132,
                        "t": 1749635376870
                    },
                    {
                        "x": 891,
                        "y": 133,
                        "t": 1749635376879
                    },
                    {
                        "x": 895,
                        "y": 134,
                        "t": 1749635376886
                    },
                    {
                        "x": 901,
                        "y": 135,
                        "t": 1749635376894
                    },
                    {
                        "x": 906,
                        "y": 136,
                        "t": 1749635376902
                    },
                    {
                        "x": 911,
                        "y": 137,
                        "t": 1749635376910
                    },
                    {
                        "x": 915,
                        "y": 139,
                        "t": 1749635376918
                    },
                    {
                        "x": 921,
                        "y": 140,
                        "t": 1749635376926
                    },
                    {
                        "x": 926,
                        "y": 141,
                        "t": 1749635376934
                    },
                    {
                        "x": 932,
                        "y": 142,
                        "t": 1749635376942
                    },
                    {
                        "x": 937,
                        "y": 143,
                        "t": 1749635376950
                    },
                    {
                        "x": 940,
                        "y": 144,
                        "t": 1749635376958
                    },
                    {
                        "x": 944,
                        "y": 145,
                        "t": 1749635376966
                    },
                    {
                        "x": 947,
                        "y": 146,
                        "t": 1749635376974
                    },
                    {
                        "x": 948,
                        "y": 146,
                        "t": 1749635376982
                    },
                    {
                        "x": 950,
                        "y": 146,
                        "t": 1749635376990
                    },
                    {
                        "x": 951,
                        "y": 146,
                        "t": 1749635376998
                    },
                    {
                        "x": 952,
                        "y": 147,
                        "t": 1749635377006
                    },
                    {
                        "x": 952,
                        "y": 148,
                        "t": 1749635377015
                    },
                    {
                        "x": 953,
                        "y": 148,
                        "t": 1749635377022
                    },
                    {
                        "x": 955,
                        "y": 148,
                        "t": 1749635377030
                    },
                    {
                        "x": 957,
                        "y": 148,
                        "t": 1749635377038
                    },
                    {
                        "x": 959,
                        "y": 148,
                        "t": 1749635377046
                    },
                    {
                        "x": 960,
                        "y": 148,
                        "t": 1749635377054
                    },
                    {
                        "x": 962,
                        "y": 149,
                        "t": 1749635377062
                    },
                    {
                        "x": 963,
                        "y": 149,
                        "t": 1749635377070
                    },
                    {
                        "x": 964,
                        "y": 149,
                        "t": 1749635377079
                    },
                    {
                        "x": 965,
                        "y": 149,
                        "t": 1749635377086
                    },
                    {
                        "x": 965,
                        "y": 148,
                        "t": 1749635377191
                    },
                    {
                        "x": 963,
                        "y": 148,
                        "t": 1749635377198
                    },
                    {
                        "x": 959,
                        "y": 146,
                        "t": 1749635377206
                    },
                    {
                        "x": 954,
                        "y": 145,
                        "t": 1749635377214
                    },
                    {
                        "x": 950,
                        "y": 145,
                        "t": 1749635377222
                    },
                    {
                        "x": 945,
                        "y": 144,
                        "t": 1749635377230
                    },
                    {
                        "x": 940,
                        "y": 143,
                        "t": 1749635377238
                    },
                    {
                        "x": 937,
                        "y": 143,
                        "t": 1749635377246
                    },
                    {
                        "x": 934,
                        "y": 143,
                        "t": 1749635377254
                    },
                    {
                        "x": 932,
                        "y": 142,
                        "t": 1749635377262
                    },
                    {
                        "x": 931,
                        "y": 142,
                        "t": 1749635377270
                    },
                    {
                        "x": 931,
                        "y": 140,
                        "t": 1749635377383
                    },
                    {
                        "x": 932,
                        "y": 140,
                        "t": 1749635377390
                    },
                    {
                        "x": 935,
                        "y": 137,
                        "t": 1749635377398
                    },
                    {
                        "x": 938,
                        "y": 134,
                        "t": 1749635377408
                    },
                    {
                        "x": 940,
                        "y": 132,
                        "t": 1749635377414
                    },
                    {
                        "x": 941,
                        "y": 129,
                        "t": 1749635377422
                    },
                    {
                        "x": 943,
                        "y": 126,
                        "t": 1749635377430
                    },
                    {
                        "x": 945,
                        "y": 124,
                        "t": 1749635377438
                    },
                    {
                        "x": 945,
                        "y": 123,
                        "t": 1749635377446
                    },
                    {
                        "x": 945,
                        "y": 121,
                        "t": 1749635377454
                    },
                    {
                        "x": 946,
                        "y": 120,
                        "t": 1749635377462
                    },
                    {
                        "x": 946,
                        "y": 119,
                        "t": 1749635377470
                    },
                    {
                        "x": 946,
                        "y": 117,
                        "t": 1749635377478
                    },
                    {
                        "x": 946,
                        "y": 116,
                        "t": 1749635377575
                    },
                    {
                        "x": 946,
                        "y": 115,
                        "t": 1749635377583
                    },
                    {
                        "x": 944,
                        "y": 114,
                        "t": 1749635377590
                    },
                    {
                        "x": 943,
                        "y": 113,
                        "t": 1749635377598
                    },
                    {
                        "x": 942,
                        "y": 113,
                        "t": 1749635377606
                    },
                    {
                        "x": 942,
                        "y": 112,
                        "t": 1749635377614
                    },
                    {
                        "x": 941,
                        "y": 112,
                        "t": 1749635377622
                    },
                    {
                        "x": 940,
                        "y": 112,
                        "t": 1749635377630
                    },
                    {
                        "x": 939,
                        "y": 111,
                        "t": 1749635377638
                    },
                    {
                        "x": 939,
                        "y": 110,
                        "t": 1749635377646
                    },
                    {
                        "x": 937,
                        "y": 110,
                        "t": 1749635377662
                    },
                    {
                        "x": 936,
                        "y": 109,
                        "t": 1749635377694
                    },
                    {
                        "x": 935,
                        "y": 109,
                        "t": 1749635377719
                    },
                    {
                        "x": 934,
                        "y": 109,
                        "t": 1749635377726
                    },
                    {
                        "x": 933,
                        "y": 109,
                        "t": 1749635377734
                    }
                ],
                "iconClickTrack": "[{\"x\":951,\"y\":112,\"t\":1749635378102},{\"x\":966,\"y\":113,\"t\":1749635378110},{\"x\":981,\"y\":113,\"t\":1749635378118},{\"x\":991,\"y\":113,\"t\":1749635378126},{\"x\":1001,\"y\":113,\"t\":1749635378134},{\"x\":1009,\"y\":113,\"t\":1749635378142},{\"x\":1014,\"y\":114,\"t\":1749635378150},{\"x\":1019,\"y\":116,\"t\":1749635378158},{\"x\":1022,\"y\":117,\"t\":1749635378166},{\"x\":1025,\"y\":117,\"t\":1749635378174},{\"x\":1028,\"y\":117,\"t\":1749635378182},{\"x\":1030,\"y\":117,\"t\":1749635378191},{\"x\":1031,\"y\":117,\"t\":1749635378198},{\"x\":1032,\"y\":117,\"t\":1749635378206},{\"x\":1034,\"y\":117,\"t\":1749635378222},{\"x\":1035,\"y\":118,\"t\":1749635378238},{\"x\":1036,\"y\":118,\"t\":1749635378246},{\"x\":1037,\"y\":119,\"t\":1749635378254},{\"x\":1041,\"y\":119,\"t\":1749635378262},{\"x\":1044,\"y\":120,\"t\":1749635378270},{\"x\":1046,\"y\":121,\"t\":1749635378278},{\"x\":1050,\"y\":121,\"t\":1749635378286},{\"x\":1055,\"y\":122,\"t\":1749635378294},{\"x\":1060,\"y\":124,\"t\":1749635378302},{\"x\":1064,\"y\":125,\"t\":1749635378311},{\"x\":1068,\"y\":125,\"t\":1749635378318},{\"x\":1071,\"y\":125,\"t\":1749635378326},{\"x\":1075,\"y\":125,\"t\":1749635378334},{\"x\":1079,\"y\":125,\"t\":1749635378342},{\"x\":1083,\"y\":125,\"t\":1749635378350},{\"x\":1086,\"y\":126,\"t\":1749635378358},{\"x\":1088,\"y\":126,\"t\":1749635378366},{\"x\":1089,\"y\":126,\"t\":1749635378374},{\"x\":1090,\"y\":126,\"t\":1749635378382}]",
                "inputStartTs": int(time.time() * 1000),
                "inputEndTs": int(time.time() * 1000),
                "inputTime": 18496,
                "selectMoveTrace": "[{\"x\":951,\"y\":112},{\"x\":966,\"y\":113},{\"x\":981,\"y\":113},{\"x\":991,\"y\":113},{\"x\":1001,\"y\":113},{\"x\":1009,\"y\":113},{\"x\":1014,\"y\":114},{\"x\":1019,\"y\":116},{\"x\":1022,\"y\":117},{\"x\":1025,\"y\":117},{\"x\":1028,\"y\":117},{\"x\":1030,\"y\":117},{\"x\":1031,\"y\":117},{\"x\":1032,\"y\":117},{\"x\":1034,\"y\":117},{\"x\":1035,\"y\":118},{\"x\":1036,\"y\":118},{\"x\":1037,\"y\":119},{\"x\":1041,\"y\":119},{\"x\":1044,\"y\":120},{\"x\":1046,\"y\":121},{\"x\":1050,\"y\":121},{\"x\":1055,\"y\":122},{\"x\":1060,\"y\":124},{\"x\":1064,\"y\":125},{\"x\":1068,\"y\":125},{\"x\":1071,\"y\":125},{\"x\":1075,\"y\":125},{\"x\":1079,\"y\":125},{\"x\":1083,\"y\":125},{\"x\":1086,\"y\":126},{\"x\":1088,\"y\":126},{\"x\":1089,\"y\":126},{\"x\":1090,\"y\":126}]",
                "selectMoveTime": "720",
                "selectCancelCount": 0,
                "selectIsTruncation": True,
                "value": x
            }
            second_param = {
                "rt": f"fp=D5A79A-5EDF21-AE8DF7&vid={self.vid}&pageId=10651171056&r={self.r}&ip={self.real_ip}&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36&d={self.origin.replace('https://', '')}&v=25&kpg=0_0_0_0_0_0_0_0_0_0&adblock=F&cck=F",
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                "p": "pc", "fp": "p51r8v-29do8p-qcu183", "vid": self.vid,
                "sfp": "Qxng%26c%25%40%23%24E*HE%5E%25r%5DJ0%3DIz%5E%25Mc9%5CN')IE",
                "identify": "aQOxwSkcU3kUqQLqT0uyVCrM00ZniKQQZaPKQyd8w2Ak=",
                "svid": "Q'EMd%26%24C%7D%24F*HC%7D!tzJFA%2BGf0%7D", "guid": "f9963043-382d-4d35-87e0-8e416d1db59e",
                "h5_duid": None, "pc_duid": None, "hb_uid": None, "pc_uid": None, "h5_uid": None,
                "infosec_openid": None,
                "device_id": "88b44a45b3d3946f22db34e58dc029fe", "client_id": "6h53EmU9jneFUXRyvhg1cVupddEFmT9b",
                "pid": "1328976876705017", "sid": "qpycHQnELElaQtNn", "login_uid": "5864994155", "client_type": "PC",
                "site": {"type": "PC", "url": f"{self.origin}/#/user/login/CN", "ref": "",
                         "title": "Partner Portal", "keywords": ""},
                "device": {"width": 1920, "height": 1080, "os": "", "pixelRatio": 1, "did": ""},
                "user": {"tid": "", "uid": "", "vid": ""}}
            second_dimensions = self.encrypt_with_fixed_iv(json.dumps(second_param, separators=(",", ":")))
            img_result = self.encrypt_with_fixed_iv(json.dumps(img_dict_param, separators=(",", ":")))
            img_text = f"appid={self.appid}&business_site={self.business_site}&version={self.version}&verify_msg={img_result}&dimensions={second_dimensions}&extend_param=ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN00C+H3pGS0QkTS+cybU5kHGoF2BK4PqNKEZeBioYzoyA=&token={token}&captcha_type=ICON"
            x_sign = hashlib.md5(img_text.encode('utf-8')).hexdigest()
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/json;charset=UTF-8",
                "origin": self.origin,
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": self.origin,
                "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            }
            url = "https://ic.trip.com/captcha/v4/verify_icon"
            data = {
                "appid": self.appid,
                "business_site": self.business_site,
                "token": token,
                "rid": rid,
                "version": self.version,
                "verify_msg": img_result,
                "dimensions": second_dimensions,
                "extend_param": "ak7Oj2doYMHGkXZ9ST5pJogOCCG%2F%2F%2FHWQ%2FKl32rGeNM002Mgcr3MiJwWHR9bljN00C%2BH3pGS0QkTS%2BcybU5kHGoF2BK4PqNKEZeBioYzoyA%3D",
                "sign": x_sign,
                "t": int(time.time() * 1000)
            }
            data = json.dumps(data, separators=(',', ':'))
            response = requests.post(url, headers=headers, data=data)
            json_data = response.json()
            return json_data
        except Exception as e:
            self.log.error(f"点击验证请求失败：{str(e)}")

    def base64_to_photo(self, file_data, img_name):
        """
        file_data: base64数据
        file_name: 文件名称
        """
        if file_data:
            data = base64.b64decode(file_data)
            # imgesPath = "./images/"
            if not os.path.exists(self.imgesPath):
                os.mkdir(self.imgesPath)
            img_path = self.imgesPath + f"{img_name}.jpg"
            with open(img_path, "wb") as f:
                f.write(data)
            return img_path

    def is_success(self, json_data, retry_count=0):
        MAX_RETRIES = 10  # 最大重试次数
        try:
            json_result = json_data['result']
            rid = json_result['rid']
            token = json_result['token']
            # 获取验证信息
            risk_info = json_result['risk_info']
            process_value = risk_info['process_value']
            if process_value:
                # 情况1：需要点选验证（滑动通过但需进一步验证）
                if process_value.get("small_image"):
                    self.log.info("滑动通过验证，需要点选验证")
                    # 处理点选验证
                    jigsaw_image = process_value['small_image']
                    original_image = process_value['big_image']
                    # # Base64 解码
                    # jigsaw_image_data = base64.b64decode(
                    #     jigsaw_image.split(",")[-1] if "," in jigsaw_image else jigsaw_image
                    # )
                    # original_image_data = base64.b64decode(
                    #     original_image.split(",")[-1] if "," in original_image else original_image
                    # )
                    # 合并图片并调用验证码识别服务
                    self.merge_images_from_base64(
                        original_image, jigsaw_image,
                        output_path=f"{abs_path}/img/merged_opencv_v.png"
                    )
                    result = self.chaojiying_utils(f'{abs_path}/img/merged_opencv_v.png', 9103)
                    result = result.replace("|", ",")
                    pic_strs = result.split(",")
                    zuobiao = [pic_str for idx, pic_str in enumerate(pic_strs)]
                    big_img_path = self.base64_to_photo(original_image, "ctrip_big")
                    small_img_path = self.base64_to_photo(jigsaw_image, 'ctrip_small')

                    self.log.info(f"识别结果坐标: {zuobiao}")
                    # 提交点选验证
                    json_result = self.hand_click((zuobiao, rid, token))
                    # 递归继续验证（不增加 retry_count，因为这是正常验证流程）
                    self.log.info(f"当前是第{retry_count}次重试")
                    if retry_count >= MAX_RETRIES:
                        self.log.error(f"已达到最大重试次数({MAX_RETRIES}次)，验证终止")
                        return None
                    return self.is_success(json_result, retry_count + 1)
                # 情况2：滑动未通过验证
                else:
                    self.log.info("当前滑动未通过验证")
                    self.log.info(f"当前是第{retry_count}次重试")
                    if retry_count >= MAX_RETRIES:
                        self.log.error(f"已达到最大重试次数({MAX_RETRIES}次)，验证终止")
                        return None
                    # 处理滑动验证
                    x_value = self.hand_img(json_data)
                    j_data = self.hand_track(x_value)
                    # 递归继续验证（增加 retry_count）
                    return self.is_success(j_data, retry_count + 1)
            # 情况3：验证已通过
            else:
                self.log.info("验证已通过----------")
                return json_result
        except Exception as e:
            self.log.info(traceback.format_exc())
            if retry_count >= MAX_RETRIES:
                self.log.error(f"已达到最大重试次数({MAX_RETRIES}次)，验证终止")
                return None
            self.log.info(f"正在进行第 {retry_count + 1} 次重试...")
            return self.is_success(json_data, retry_count + 1)

    def merge_images_from_base64(self, base64_img1, base64_img2, output_path=None, expand_px=15):
        """
        合并两张Base64编码的图片，自动处理字符串/字节输入

        :param base64_img1: 可以是Base64字符串或字节对象
        :param base64_img2: 可以是Base64字符串或字节对象
        :param output_path: 输出路径（None则返回Base64结果）
        :param expand_px: 短图放大像素数
        :return: 合并后的图片（文件或Base64）
        """

        # 改进的解码函数
        def decode_base64(base64_data):
            # 统一处理字符串或字节输入
            if isinstance(base64_data, str):
                # 去除可能的DataURL前缀
                if ',' in base64_data:
                    base64_data = base64_data.split(',')[-1]
                # 转换为字节对象
                base64_data = base64_data.encode('utf-8')

            img_data = base64.b64decode(base64_data)
            np_img = np.frombuffer(img_data, np.uint8)
            return cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)

        try:
            # 解码图片并确保有Alpha通道
            img1 = decode_base64(base64_img1)
            img2 = decode_base64(base64_img2)

            # 检查是否成功解码
            if img1 is None or img2 is None:
                raise ValueError("Failed to decode one or both images")

            # 确保都是4通道（BGRA）
            if img1.shape[2] == 3:
                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
            if img2.shape[2] == 3:
                img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)

            # 高质量放大较短的图片
            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]

            if h1 < h2:
                scale = (h1 + expand_px) / h1
                img1 = cv2.resize(img1, (int(w1 * scale), h1 + expand_px),
                                  interpolation=cv2.INTER_LANCZOS4)
            elif h2 < h1:
                scale = (h2 + expand_px) / h2
                img2 = cv2.resize(img2, (int(w2 * scale), h2 + expand_px),
                                  interpolation=cv2.INTER_LANCZOS4)

            # 创建透明画布
            max_width = max(img1.shape[1], img2.shape[1])
            merged = np.zeros((img1.shape[0] + img2.shape[0], max_width, 4), dtype=np.uint8)

            # 居中布局
            merged[:img1.shape[0], (max_width - img1.shape[1]) // 2: (max_width + img1.shape[1]) // 2] = img1
            merged[img1.shape[0]:, (max_width - img2.shape[1]) // 2: (max_width + img2.shape[1]) // 2] = img2

            # 结果输出
            if output_path:
                if not output_path.lower().endswith('.png'):
                    output_path += '.png'
                cv2.imwrite(output_path, merged)
                return output_path
            else:
                _, buffer = cv2.imencode('.png', merged)
                return base64.b64encode(buffer).decode('utf-8')

        except Exception as e:
            raise ValueError(f"Image merge failed: {str(e)}")

    def run(self):
        img_data = self.request_img()
        token = img_data.get('result', {}).get("token", None)
        if token.startswith('p0'):
            rid = token = img_data['result']["token"]
            return {"rid": rid, "token": token}
        json_result = self.is_success(img_data)
        if json_result:
            rid = json_result['rid']
            token = json_result['token']
            tt = {"rid": rid, "token": token}
            return tt
        else:
            self.log.error("未成功通过图片验证")
            return None

def get_tt(session, appid, business_site, version):
    trip = CtripCaptchaSolver(logger, session, appid=appid, business_site=business_site, version=version)
    sleep_time = trip.run()
    return sleep_time

# session = requests.session()
# t = get_tt(session=session, appid="100014851", business_site="ibu_airticketsbook_online_pic", version="1.0.13")
# print(t)