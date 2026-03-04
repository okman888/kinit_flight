# -*- coding: utf-8 -*-
# @Time : 2026/2/13 10:38
# @Author: sunwei
# @Instructions: 说明
# @remark: 备注
# @Software: Python 3.7.8

import requests_go
import requests
from random_tls import ua_to_sec_ch_ua, ua_to_sec_ch_platform
import time
import json
import re
from datetime import datetime
import random
from loguru import logger
import opencc
from requests_go.tls_config import *
import os
import execjs
import uuid
from tbooking_yzm import get_tt


null = None
false = False
true = True
undefined = None

current_path = os.path.dirname(os.path.abspath(__file__))
# 创建转换器实例
cc = opencc.OpenCC('t2s')  # 繁体转简体

def crypto_js():
    with open(os.path.join(current_path, 'crypto_js.js'), 'r', encoding="utf-8")as f:
        ctx = execjs.compile(f.read())
    return ctx

def random_ee(e=32, t=0):
    charset_list = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "0123456789abcdef"
    ]
    charset = charset_list[t]
    length = e
    result = "".join(random.choice(charset) for _ in range(length))
    return result

# https://hk.trip.com/?locale=zh-HK&curr=CNY



class CrawlerTrip:
    def __init__(self, account=None, password=None, http_proxy=None, https_proxy=None):
        self.session = requests.Session()
        #self.session = requests_go.Session()
        tls_choice = TLS_CHROME_130
        self.random_tls = tls_choice
        self.session.tls_config = self.random_tls
        self.ua = self.random_tls.user_agent
        self.sec_ch_ua = ua_to_sec_ch_ua(self.ua)
        self.sec_ch_ua_platform = ua_to_sec_ch_platform(self.ua)
        self.vid = f"{int(time.time() * 1000)}.{random_ee(12, 0)}"
        self.headers = {
            "accept": "*/*",
            "accept-language": "*/*",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://hk.trip.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://hk.trip.com/",
            "sec-ch-ua": self.sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": self.sec_ch_ua_platform,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.ua,
            "x-ctx-country": "HK",
            "x-ctx-currency": "CNY",
            "x-ctx-locale": "zh-HK",
            "x-ctx-ubt-vid": self.vid,
            # "x-ctx-wclient-req": "655b2cb36e63fbd59f645ccac05db2bc"
        }
        if not self.sec_ch_ua:
            del self.headers['sec-ch-ua']
        self.cookies = {}

        self.proxies = None
        if http_proxy or https_proxy:
            self.proxies = {}
            if http_proxy:
                self.proxies['http'] = http_proxy
            if https_proxy:
                self.proxies['https'] = https_proxy
        # self.proxies = {
        #     'https': 'http://B_62149_HK_3865_66511_5_crawler1:123456@gate2.ipweb.cc:7778',
        #     'http': 'http://B_62149_HK_3865_66511_5_crawler1:123456@gate2.ipweb.cc:7778',
        # }

        self.username = account
        self.password = password
        self.timeout = 60

    def get_risk_token(self, appId, version, business_site):
        Plaint_data = {
            "rt": "fp=BB379A-5EDF21-15AD49&vid=1765423717946.8ff9yPtQNDRZ&pageId=10320668055&r=64a654918e6b476793b2275ad57ecf26&ip=undefined&rg=undefined&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36&d=hk.trip.com&v=25&kpg=0_1_0_0_58926_26_1_2_0_0&adblock=F&cck=F&ftoken=",
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "p": "pc",
            "fp": "BB379A-5EDF21-15AD49",
            "vid": self.vid,
            "sfp": None,
            "identify": "aBB379A-5EDF21-15AD49",
            "svid": undefined,
            "guid": "09034171314349030556",
            "h5_duid": null,
            "pc_duid": null,
            "hb_uid": null,
            "pc_uid": null,
            "h5_uid": null,
            "infosec_openid": null,
            "device_id": random_ee(32, 3),  ##
            "client_id": random_ee(32, 0),  ##
            "pid": random_ee(16, 2),  ##
            "sid": random_ee(16, 1),  ##
            "login_uid": random_ee(10, 2),  ##
            "client_type": "PC",
            "site": {
                "type": "PC",
                "url": "https://hk.trip.com/?locale=zh-HK&curr=CNY",
                "ref": "",
                "title": "Trip.com官方網站：全球機票、酒店，高鐵網上預訂",
                "keywords": "酒店,機票,自由行套票,酒店預訂,訂房,機票預訂,機票查詢,火車票,中國旅遊,旅遊,旅遊網, Trip.com"
            },
            "device": {
                "width": 1920,
                "height": 1080,
                "os": "",
                "pixelRatio": 1,
                "did": ""
            },
            "user": {
                "tid": "",
                "uid": "",
                "vid": ""
            }
        }
        dimensions = crypto_js().call("encBody", Plaint_data)
        md5_text = f'appid={appId}&business_site={business_site}&version={version}&dimensions={dimensions}&extend_param=ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN0AgsRxljIDHaPz8drzUPu5bpQteKLCckGxztUEuzE6pE='
        sign = crypto_js().call("md5", md5_text)
        data = {
            "extend_param": "ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN0AgsRxljIDHaPz8drzUPu5bpQteKLCckGxztUEuzE6pE=",
            "appid": int(appId),
            "business_site": business_site,
            "version": str(version),
            "dimensions": dimensions,
            "sign": sign,
            "t": int(time.time() * 1000)
        }
        data = json.dumps(data, separators=(',', ':'))
        url = "https://ic.trip.com/captcha/v4/risk_inspect"
        res = self.session.post(url, headers=self.headers, data=data, proxies=self.proxies, timeout=self.timeout)
        if res.status_code != 200:
            logger.error(f"获取登录token失败: {res.status_code}")
            return {"code": 400, "msg": "获取登录token失败", "data": None}
        if res.json().get("code") != 0:
            logger.error(f"获取登录token失败: {res.json()}")
            return {"code": 400, "msg": "获取登录token失败", "data": None}
        if res.json().get("result").get("risk_info").get("process_value"):
            logger.info(f"触发验证码, 当前验证码类型为: {res.json().get('result').get('risk_info').get('process_type')}")
            logger.info(f"当前风险等级: {res.json().get('result').get('risk_info').get('risk_level')}")
            # return self.slider_verify(res.json())
            return {"code": 400, "msg": "触发验证码", "data": res.json()}
        return {"code": 200, "msg": "获取登录token成功", "data": res.json()}

    def login(self):
        appId = 100032497
        version = "1.0.3"
        business_site = "ibu_login_online_pic"
        login_token = self.get_risk_token(appId, version, business_site)
        if login_token.get("code") != 200:
            return login_token
        token_info = login_token.get("data")
        url = "https://hk.trip.com/restapi/soa2/27024/pwdLogin"
        sequenceId = str(uuid.uuid4())
        plaint_data = {
            "accessCode": "IBUPCAUTEHNTICATE",
            "strategyCode": "PWDLOGIN",
            "authenticateInfo": {
                "loginName": self.username,
                "password": self.password
            },
            "frontRiskInfo": {
                "token": token_info['result']['token'],
                "sliderVersion": "1.0.5",
                "businessSite": "ibu_login_online_pic",
                "rid": token_info['result']['rid']
            },
            "context": {
                "sequenceId": sequenceId,
                "needVerifyEmail": "false",
                "needImportOrder": "false"
            },
            "clientInfo": {
                "locale": "zh-HK",
                "clientId": "09034016214753366907",
                "pageId": "10320667454",
                "rmsToken": f"fp=BB379A-5EDF21-15AD49&vid={self.vid}&pageId=10320667454&r=96cc3bbf13414a8999fc6f524dae3c23&ip=14.220.241.8&rg=fin&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36&d=hk.trip.com&v=25&kpg=0_0_0_0_6342_10_2_0_0_0&adblock=F&cck=F&ftoken="
            },
            "head": {
                "cid": "",
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "syscode": "09",
                "auth": "",
                "xsid": "",
                "extension": [
                    {
                        "name": "moduleName",
                        "value": "accountSignin"
                    },
                    {
                        "name": "sdkName",
                        "value": "onlinePopup"
                    },
                    {
                        "name": "sdkVersion",
                        "value": "3.1.40"
                    },
                    {
                        "name": "platform",
                        "value": "PC"
                    },
                    {
                        "name": "sysCode",
                        "value": "999"
                    },
                    {
                        "name": "fromPageId",
                        "value": "10320667454"
                    },
                    {
                        "name": "sequence",
                        "value": sequenceId
                    }
                ],
                "Locale": "zh-HK",
                "Language": "hk",
                "Currency": "CNY",
                "ClientID": ""
            }
        }
        headers = {
            "Host": "hk.trip.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": self.sec_ch_ua,
            "x-ctx-ubt-pvid": "6",
            "cookieorigin": "https://hk.trip.com",
            "x-origin-ct": "application/json",
            "sec-ch-ua-platform": self.sec_ch_ua_platform,
            "x-ctx-locale": "zh-HK",
            "currency": "CNY",
            "x-ctx-ubt-sid": "4",
            "x-ctx-country": "HK",
            "x-payload-encoding": "camev1",
            "locale": "zh-HK",
            "sec-ch-ua-mobile": "?0",
            "user-agent": self.ua,
            "content-type": "text/plain",
            "x-payload-accept": "camev1",
            "x-ctx-ubt-vid": self.vid,
            "x-ctx-currency": "CNY",
            "x-ctx-ubt-pageid": "10320668088",
            "accept": "*/*",
            "origin": "https://hk.trip.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://hk.trip.com/?locale=zh-HK&curr=CNY",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=1, i"
        }
        data = crypto_js().call("encryptBody", plaint_data)
        res = self.session.post(url, headers=headers, data=data, proxies=self.proxies, timeout=self.timeout)
        if res.status_code != 200:
            logger.error(f"登录失败: {res.status_code}")
            return {"code": 400, "msg": "登录失败", "data": None}
        decry_text = json.loads(crypto_js().call("decryptBody", res.text))
        if decry_text.get("returnCode") != 0:
            logger.error(f"账号: {self.username}登录失败: {decry_text.get('message')}")
            return {"code": 400, "msg": decry_text.get('message'), "data": None}
        logger.info(f"账号: {self.username}登录成功")
        self.save_account_info(decry_text, res.cookies.get_dict())
        return {"code": 200, "msg": "登录成功", "data": decry_text}

    def save_account_info(self, login_data, login_cookies):
        """
        保存账户信息和cookies到文件
        """
        accounts_dir = os.path.join(current_path, "accounts")
        if not os.path.exists(accounts_dir):
            os.makedirs(accounts_dir)
        # 使用账号名称作为文件名（去除邮箱中的@和.字符）
        safe_username = self.username.replace("@", "_").replace(".", "_")
        account_info = {
            "username": self.username,
            "login_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "response_data": login_data,
            "cookies": login_cookies
        }
        info_file_path = os.path.join(accounts_dir, f"{safe_username}_info.json")
        with open(info_file_path, "w", encoding="utf-8") as f:
            json.dump(account_info, f, ensure_ascii=False, indent=4)
        cookies_file_path = os.path.join(accounts_dir, f"{safe_username}_cookies.json")
        with open(cookies_file_path, "w", encoding="utf-8") as f:
            json.dump(login_cookies, f, ensure_ascii=False, indent=4)
        logger.info(f"账户信息已保存至: {info_file_path}")
        logger.info(f"Cookies已保存至: {cookies_file_path}")

    def is_expired(self, expire_time_str):
        """检查expireTime是否已过期"""
        match = re.search(r'/Date\((\d+)', expire_time_str)
        if match:
            timestamp = int(match.group(1))
            expire_time = timestamp / 1000
            current_time = time.time()
            return current_time > expire_time
        return True

    def load_saved_cookies(self):
        """加载已保存的cookies"""
        safe_username = self.username.replace("@", "_").replace(".", "_")
        cookies_file_path = os.path.join(current_path, "accounts", f"{safe_username}_cookies.json")
        if os.path.exists(cookies_file_path):
            try:
                with open(cookies_file_path, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                    # 设置session的cookies
                    for key, value in cookies.items():
                        self.session.cookies.set(key, value)
                        self.cookies[key] = value
                return True
            except Exception as e:
                logger.error(f"账号: {self.username}加载cookies失败: {e}")
        return False

    def check_and_login(self):
        """检查过期时间并决定是否需要重新登录"""
        safe_username = self.username.replace("@", "_").replace(".", "_")
        info_file_path = os.path.join(current_path, "accounts", f"{safe_username}_info.json")
        if os.path.exists(info_file_path):
            try:
                with open(info_file_path, "r", encoding="utf-8") as f:
                    account_info = json.load(f)
                expire_time = account_info.get("response_data", {}).get("expireTime")
                if expire_time and not self.is_expired(expire_time):
                    if self.load_saved_cookies():
                        logger.info(f"使用已保存的有效会话: {self.username}")
                        return {"code": 200, "msg": "使用缓存登录", "data": account_info}
                    else:
                        logger.warning("Cookies加载失败，重新登录")
                else:
                    logger.info(f"账号: {self.username}会话已过期，重新登录")
            except Exception as e:
                logger.error(f"账号: {self.username}检查过期时间失败: {e}")
        return self.login()

    def queryFlight(self, param, fno=None):
        if param.get("platformType").upper() == "B2B":
            # logger.info(f"使用B2B登录")
            login_result = self.check_and_login()
            if login_result.get("code") != 200:
                return login_result
        url = "https://hk.trip.com/restapi/soa2/27015/FlightListSearch"
        dept = param['dept'].lower()
        arrs = param['arr'].lower()
        timestamp = datetime.now()
        data = {
            "mode": 0,
            "searchCriteria": {
                "grade": 3,
                "realGrade": 1,
                "tripType": 1,
                "journeyNo": 1,
                "passengerInfoType": {
                    "adultCount": param.get("adtnum", 1),
                    "childCount": param.get("chdnum", 0),
                    "infantCount": param.get("infnum", 0)
                },
                "journeyInfoTypes": [
                    {
                        "journeyNo": 1,
                        "departDate": param['fromdate'],
                        "departCode": param['dept'],
                        "arriveCode": param['arr'],
                        "departAirport": "",
                        "arriveAirport": ""
                    }
                ],
                "policyId": None
            },
            "sortInfoType": {
                "direction": True,
                "orderBy": "Direct",
                "topList": []
            },
            "tagList": [],
            "flagList": [
                "NEED_RESET_SORT"
            ],
            "filterType": {
                "filterFlagTypes": [],
                "queryItemSettings": [],
                "studentsSelectedStatus": True
            },
            "abtList": [
                {
                    "abCode": "250811_IBU_wjrankol",
                    "abVersion": "E"
                },
                {
                    "abCode": "250806_IBU_FiltersOpt",
                    "abVersion": "A"
                },
                {
                    "abCode": "250812_IBU_FiltersOp2",
                    "abVersion": "A"
                },
                {
                    "abCode": "251023_IBU_pricetool",
                    "abVersion": "B"
                }
            ],
            "head": {
                "cid": "09034150414450274844",
                "ctok": "",
                "cver": "3",
                "lang": "01",
                "sid": "8888",
                "syscode": "40",
                "auth": "",
                "xsid": "",
                "extension": [
                    {
                        "name": "abTesting",
                        "value": "M:98,250626_IBU_refresh:A;M:32,240912_IBU_jpwjo:A;M:68,241224_IBU_TOLNG:B;M:30,250109_IBU_OLFBO:B;M:64,250207_IBU_FLTOLM:C;M:91,250403_IBU_PDOOL:A;M:60,250427_IBU_TCBOL:E;M:79,250630_IBU_fill:E;M:96,250710_IBU_meta:A;M:42,250710_IBU_automore:B;M:60,250710_IBU_stgp:C;M:81,250630_IBU_omp3:A;M:81,250716_IBU_Flightcard:A;M:81,250716_IBU_FCredesg:E;M:99,250630_IBU_BSOOL:D;M:37,250724_IBU_TooltipInt:E;M:92,250730_IBU_Load15:A;M:16,250807_IBU_sea:A;M:36,250811_IBU_wjrankol:E;M:11,250811_IBU_law:B;M:17,250806_IBU_Off2Scroll:B;M:48,250806_IBU_FiltersOpt:A;M:85,250730_IBU_OLNOHIDFE:A;M:39,250812_IBU_SDoubleCTA:A;M:43,250812_IBU_FiltersOp2:A;M:40,250924_IBU_OLYPGZ:B;M:16,251022_IBU_HoverRed:B;M:76,251031_IBU_lppg:A;M:5,251023_IBU_pricetool:B;M:11,251110_IBU_TVCOL:A;M:6,251010_IBU_mfm:A;M:-1,251119_IBU_MCSearch:A;M:-1,251118_IBU_XResultOpt:A;M:-1,251119_IBU_MCSegDisp:A;M:78,251128_IBU_fic:D;M:36,251112_IBU_pxjygxtol:A;M:93,251124_IBU_lfp4:D;M:91,251029_IBU_GATETECH:A;"
                    },
                    {
                        "name": "source",
                        "value": "ONLINE"
                    },
                    {
                        "name": "sotpGroup",
                        "value": "Trip"
                    },
                    {
                        "name": "sotpLocale",
                        "value": "zh-HK"
                    },
                    {
                        "name": "sotpCurrency",
                        "value": param.get("currency")
                    },
                    {
                        "name": "allianceID",
                        "value": "0"
                    },
                    {
                        "name": "sid",
                        "value": "0"
                    },
                    {
                        "name": "ouid",
                        "value": ""
                    },
                    {
                        "name": "uuid"
                    },
                    {
                        "name": "useDistributionType",
                        "value": "1"
                    },
                    {
                        "name": "flt_app_session_transactionId",
                        "value": f"1-mf-{timestamp.strftime('%Y%m%d%H%M%S') + str(timestamp.microsecond)[:3]}-WEB"
                    },
                    {
                        "name": "vid",
                        "value": self.vid
                    },
                    {
                        "name": "pvid",
                        "value": "1"
                    },
                    {
                        "name": "Flt_SessionId",
                        "value": "3"
                    },
                    {
                        "name": "channel"
                    },
                    {
                        "name": "x-ua",
                        "value": "v=3_os=ONLINE_osv=10"
                    },
                    {
                        "name": "PageId",
                        "value": "10320667452"
                    },
                    {
                        "name": "clientTime",
                        "value": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime())
                    },
                    {
                        "name": "Member",
                        "value": "1"
                    },
                    {
                        "name": "LowPriceSource",
                        "value": "searchForm"
                    },
                    {
                        "name": "Flt_BatchId",
                        "value": str(uuid.uuid4())
                    },
                    {
                        "name": "BlockTokenTimeout",
                        "value": "0"
                    },
                    {
                        "name": "full_link_time_scene",
                        "value": "pure_list_page"
                    },
                    {
                        "name": "xproduct",
                        "value": "baggage"
                    },
                    {
                        "name": "units",
                        "value": "METRIC"
                    },
                    {
                        "name": "sotpUnit",
                        "value": "METRIC"
                    }
                ],
                "Locale": "zh-HK",
                "Language": "hk",
                "Currency": param['currency'],
                "ClientID": "",
                "appid": "700020"
            }
        }
        data = json.dumps(data, separators=(',', ':'))
        self.headers['referer'] = f"https://hk.trip.com/chinaflights/showfarefirst?pagesource=list&triptype=OW&class=Y" \
                                  f"&quantity=1&childqty=0&babyqty=0&jumptype=Timeout&dcity=sha&acity=bjs&dairpor" \
                                  f"t={param['dept'].lower()}&aairport={param['arr'].lower()}&ddate={param['fromdate']}&airline=&lo" \
                                  f"cale=zh-HK&curr={param['currency']}"
        if param.get('iata') == "int":
            url = "https://hk.trip.com/restapi/soa2/27015/FlightListSearchSSE"
            self.headers['referer'] = f"https://hk.trip.com/flights/showfarefirst?dcity={dept}&acity={arrs}&ddat" \
                                      f"e={param['fromdate']}&rdate=2026-03-03&triptype=ow&class=y&lowpricesource=" \
                                      f"searchform&quantity=1&searchboxarg=t&nonstoponly=off&loc" \
                                      f"ale=zh-HK&curr={param['currency']}"
        res = self.session.post(url, headers=self.headers, data=data, proxies=self.proxies, timeout=self.timeout)
        if res.status_code != 200:
            logger.error(f"{param['dept']} - {param['arr']} 请求失败: {res.status_code}")
            return {"code": 400, "msg": f"{param['dept']} - {param['arr']} 请求失败: {res.status_code}"}
        match_flight = re.findall('data:(.*?)\n', res.text)
        if len(match_flight) != 2:
            logger.error(f"{param['dept']} - {param['arr']} 触发验证码")
            t = get_tt(session=self.session, appid="100014851", business_site="ibu_airticketsbook_online_pic",
                       version="1.0.14")
            if t is None:
                return {"code": 400, "message": "验证码未通过校验"}
            self.updateToWhite(t['rid'], t['token'], "flightListSearch")
            return {"code": 400, "msg": f"{param['dept']} - {param['arr']} 触发验证码"}
        flight_data = {}
        if param['iata'] == "ca":
            flight_data = res.json()
        elif param['iata'] == "int":
            match_flight = re.findall('data:(.*?)\n', res.text)
            if len(match_flight) != 2:
                logger.error(f"{param['dept']} - {param['arr']} 触发验证码")
                return {"code": 400, "msg": f"{param['dept']} - {param['arr']} 触发验证码"}
            flight_data = json.loads(match_flight[1])
        if not flight_data.get("itineraryList"):
            logger.error(f"{param['dept']} - {param['arr']} 航班数据为空")
            return {"code": 400, "msg": f"{param['dept']} - {param['arr']} 航班数据为空"}
        if flight_data.get("ResponseStatus", None) is None:
            logger.error(f"{param['dept']} - {param['arr']} 航班数据异常或可能触发验证码")
            t = get_tt(session=self.session, appid="100014851", business_site="ibu_airticketsbook_online_pic", version="1.0.14")
            if t is None:
                return {"code": 400, "message": "验证码未通过校验"}
            self.updateToWhite(t['rid'], t['token'], "flightListSearch")
            return {"code": 401, "msg": f"{param['dept']} - {param['arr']} 航班数据异常或可能触发验证码"}
        logger.info(f"{param['dept']} - {param['arr']} 航班数据获取成功")
        return {"code": 200, "msg": "success", "data": flight_data}

    def parseFlight(self, flight_data):
        results = []
        re_flight_list = []
        basicInfo = flight_data.get("basicInfo", {})
        currency = basicInfo.get("currency")
        productId = basicInfo.get("productId")
        for itinerary in flight_data["itineraryList"]:
            ex = []
            ex.append(productId)
            journey = itinerary["journeyList"][0]
            segments = journey.get("transSectionList", [])
            policies = itinerary.get("policies", [])[0]
            for segment in segments:
                depart_point = segment.get("departPoint", {})
                arrive_point = segment.get("arrivePoint", {})
                flight_info = segment.get("flightInfo", {})
                craft_info = flight_info.get("craftInfo", {})
                segs = []
                segs.append({
                    "aircraftCode": craft_info.get("shortName", ""),
                    "dept": depart_point.get("airportCode", ""),
                    "depttime": segment.get("departDateTime", ""),
                    "depttrmn": depart_point.get("terminal", ""),
                    "arr": arrive_point.get("airportCode", ""),
                    "arrtime": segment.get("arriveDateTime", ""),
                    "arrtrmn": arrive_point.get("terminal", ""),
                    # "chdbag": "1,20,KG",  # 默认儿童行李信息
                    # "chdfarebasis": "",  # 儿童票价基础代码
                    # "bag": "1,20,KG",  # 默认行李信息，可根据实际数据调整
                    "cabinclass": policies['gradeInfoList'][0]['subClass'],
                    "cabinName": policies['gradeInfoList'][0]['gradeMultilingual'],
                    "flightno": flight_info.get("flightNo", ""),
                    "flighttime": segment.get("duration", 0),
                    "fareFamily": "",  # 票价家族
                    "farebasis": "",  # 票价基础代码
                    "group": 0,
                    # "seat": "R",  # 座位等级
                    "meal": None,
                    "oprcarrier": flight_info.get("airlineCode", ""),
                    "oprflightno": flight_info.get("flightNo", ""),
                })
                price = policies.get("price")
                policyId = policies.get("policyId")
                ex.append(policyId)
                adult_price = price.get("adult", {}).get("totalPrice", 0) if price.get("adult") else 0
                adult_piaojia = price.get("adult", {}).get("salePrice", 0) if price.get("adult") else 0
                adult_tax = price.get("adult", {}).get("tax", 0) if price.get("adult") else 0
                child_price = price.get("child", {}).get("totalPrice", 0) if price.get("child") else 0
                child_piaojia = price.get("child", {}).get("salePrice", 0) if price.get("child") else 0
                child_tax = price.get("adult", {}).get("tax", 0) if price.get("child") else 0
                infant_price = price.get("infant", {}).get("totalPrice", 0) if price.get("infant") else 0
                infant_piaojia = price.get("child", {}).get("salePrice", 0) if price.get("infant") else 0
                infant_tax = price.get("adult", {}).get("tax", 0) if price.get("infant") else 0
                totalMoney = adult_price + child_price + infant_price
                totalTax = price.get("totalTax", 0)
                result_item = {
                    "carrier": flight_info.get("airlineCode", ""),
                    "fromsegs": segs,
                    "ex": ("|").join(ex),
                    "adult_price": adult_price,
                    "adult_piaojia": adult_piaojia,
                    "adult_tax": adult_tax,
                    "child_price": child_price,
                    "child_piaojia": child_piaojia,
                    "child_tax": child_tax,
                    "infant_price": infant_price,
                    "infant_piaojia": infant_piaojia,
                    "infant_tax": infant_tax,
                    "totalMoney": totalMoney,
                    "totalTax": totalTax,
                    "currency": currency,
                    "seatcount": policies.get("seatCount"),  # 座位数量
                    "stopcity": None
                }
                results.append(result_item)
        return results

    def updateToWhite(self, rid, token, sourceApi):
        # 提交校验验证码
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://hk.trip.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://hk.trip.com/flights/showfarefirst?pagesource=list&lowpricesource=lowPriceCalendar&triptype=OW&class=Y&quantity=1&childqty=0&babyqty=0&dcity=tyo&acity=tpe&ddate=2026-03-01&dcityName=Tokyo&acityName=Taipei&airline=&locale=zh-HK&curr=HKD",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        url = "https://hk.trip.com/flightapi/updateToWhite"
        data = {
            "rid": rid,
            "token": token,
            "checkState": "success",
            "version": "1.0.14",
            "sourceApi": sourceApi,
            "Head": {"ExtendFields": {"flightRegion": "I"}}
        }
        data = json.dumps(data, separators=(',', ':'))
        response = self.session.post(url, headers=headers, data=data, timeout=self.timeout)
        print(response.text)
        print(response)

def search(param):
    account = '727735746@qq.com'
    pwd = 'Hjj07270318'
    dept, arr, fromdate, retdate = param.get('dept'), param.get('arr'), param.get('fromdate'), param.get('retdate', '')
    trip = CrawlerTrip(account=account, password=pwd)
    query_result = trip.queryFlight(query_data)
    if query_result.get('code') != 200:
        return query_result
    flight_result = trip.parseFlight(query_result.get('data'))
    return {"code": 200, "message": f"成功返回{dept}-{arr} {fromdate} {retdate}的航班数据", "result": flight_result}


if __name__ == '__main__':
    #2293851393@qq.com
    #@hw520888
    account = '727735746@qq.com'
    pwd = 'Hjj07270318'
    query_data = {
        "dept": "TYO",
        "arr": "TPE",
        # "arr": "SZX",
        # "arr": "BKK",
        "fromdate": "2026-03-19",
        "currency": "CNY",
        "triptype": 1,  ## 1:单程，2:往返
        "platformType": "B2B",
        "adtnum": 1,
        "chdnum": 0,
        "infnum": 0,
        "iata": "int" ## ca为国内航班, int为国际航班
    }
    res = search(query_data)
    print(res)
    # while True:
    #     res = search(query_data)
    #     print(res)
