import random
import requests_go
from requests_go.tls_config import *

def random_chrome_tls_6e():
    tls_list = [okhttp_random_tls, edge_macos_random_tls, edge_windows_random_tls,
                       chrome_ios_random_tls, chrome_android_random_tls, chrome_macos_random_tls, chrome_windows_random_tls
                      ]
    tls_fingerprint = random.choice(tls_list)()
    return tls_fingerprint

def random_chrome_tls():
    chrome_tls_list = [TLS_CHROME_120, TLS_CHROME_122, TLS_CHROME_125, TLS_CHROME_127,
                       TLS_CHROME_128, TLS_CHROME_130, TLS_CHROME_131, TLS_CHROME_132,
                       TLS_CHROME_133, TLS_CHROME_135, TLS_CHROME_138,
                       TLS_CHROME_139, ]
    chrome_tls = random.choice(chrome_tls_list)
    return chrome_tls

def random_chrome_high_tls():
    chrome_tls_list = [TLS_CHROME_120, TLS_CHROME_122, TLS_CHROME_125,
                       TLS_CHROME_127, TLS_CHROME_128, TLS_CHROME_135]
    chrome_tls = random.choice(chrome_tls_list)
    return chrome_tls

def random_edge_tls():
    edge_tls_list = [TLS_EDGE_141, TLS_EDGE_139, TLS_EDGE_131, TLS_EDGE_126,
                     TLS_EDGE_125, TLS_EDGE_122, TLS_EDGE_121
                     ]
    edge_tls = random.choice(edge_tls_list)
    return edge_tls

def random_edge_high_tls():
    edge_tls_list = [TLS_EDGE_131, TLS_EDGE_126,
                     TLS_EDGE_125, TLS_EDGE_122, TLS_EDGE_121
                     ]
    edge_tls = random.choice(edge_tls_list)
    return edge_tls

def random_charles_tls():
    charles_tls_list = [TLS_CHARLES_5_0_3_CHROME_141, TLS_CHARLES_4_6_7_CHROME_141, TLS_CHARLES_4_6_4_CHROME_141,
                        TLS_CHARLES_4_6_2_CHROME_140, TLS_CHARLES_4_6_7_EDGE_141, TLS_CHARLES_4_6_4_EDGE_141,
                        ]
    charles_tls = random.choice(charles_tls_list)
    return charles_tls

def random_firefox_tls():
    firefox_tls_list = [TLS_FIREFOX_144, TLS_FIREFOX_143, TLS_FIREFOX_140,
                        TLS_FIREFOX_144_RV_68_0_ANDROID_16
    ]
    firefox_tls = random.choice(firefox_tls_list)
    return firefox_tls

def shuffle_cipher_suites(ja3: str) -> str:
    """
    接受标准 JA3 字符串，并随机打乱 cipher_suites 的顺序。
    返回新的 JA3 字符串。
    """
    parts = ja3.split(',')
    if len(parts) != 5:
        raise ValueError("Invalid JA3 format")
    cipher_list = parts[1].split('-')
    random.shuffle(cipher_list)
    parts[1] = '-'.join(cipher_list)
    return ','.join(parts)

def ua_to_sec_ch_ua(ua: str) -> str:
    """
    根据 UA 自动生成对应的 sec-ch-ua 字段
    支持 Chrome、Edge
    """
    import re
    # Edge
    if "Edg/" in ua:
        match = re.search(r"Edg/(\d+)", ua)
        if match:
            version = match.group(1)
            return f'"Chromium";v="{version}", "Microsoft Edge";v="{version}", "Not_A Brand";v="99"'
    # Chrome
    match = re.search(r"Chrome/(\d+)", ua)
    if match:
        version = match.group(1)
        return f'"Not)A;Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    # return '"Not_A Brand";v="99", "Chromium";v="99"'

def ua_to_sec_ch_platform(ua: str) -> str:
    """
    根据 UA 自动生成 sec-ch-ua-platform
    能区分 Windows / macOS / Linux / Android / iOS
    """
    ua_lower = ua.lower()
    if "macintosh" in ua_lower:
        return '"macOS"'
    if "windows" in ua_lower:
        return '"Windows"'
    if "linux" in ua_lower and "android" not in ua_lower:
        return '"Linux"'
    if "android" in ua_lower:
        return '"Android"'
    if "iphone" in ua_lower or "ipad" in ua_lower:
        return '"iOS"'