// 需要先加载 crypto-js
// npm install crypto-js
const path = require('path');
// PyExecJS 运行时 __dirname 可能为当前目录，尝试多种路径解析方式
const possiblePaths = [
    path.join(__dirname, 'node_modules', 'crypto-js'),
    '/Users/apple/Desktop/workspace/kinit_flight/kinit-trip/node_modules/crypto-js',
    'node_modules/crypto-js',
    'crypto-js'
];
let CryptoJS = null;
for (const p of possiblePaths) {
    try {
        CryptoJS = require(p);
        break;
    } catch (e) {
        // 继续尝试下一个路径
    }
}
if (!CryptoJS) {
    throw new Error('Cannot find crypto-js module. Tried: ' + possiblePaths.join(', '));
}
window = globalThis;

var _0x3500 = ["pad", "httperror", "length", "0123456789abcdef", "//ic.ctrip.uat.qa.nt.ctripcorp.com/", "jsonp", "prototype", "mediaStreamTrack", "isPreProduction", "padding", "apply", "removeChild", "iterationCount", "stateChange", "corpid", "_cipher", "DUID", "ver", "getElementsByTagName", "sFP", "_minBufferSize", "encrypt", "PBKDF2", "cfg", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", "browserLanguage", "inter_base", "jigsaw", "ctrip", "=([^&]*)(&|$)", "//ic.ctrip.com/", "risk_info", "UserID", "HmacSHA1", "_oKey", "sigBytes", "false", "Base", "charAt", "checkParas", "extend_param", "ontimeout", "__quote", "undefined", "createEncryptor", "_bfs", "SHA1", "rid", "parentNode", "setAttribute", "Utf8", "cticket", "setRequestHeader", "lib", "push", "addEventListener", "sfp", "compute", "readyState", "ivSize", "_nDataBytes", "string", "navigator", "clear", "(^| )", "timer", "_process", "securefp", "clone", "test", "pro", "msgTips", "//gateway.m.uat.qa.nt.ctripcorp.com/restapi/infosec/", "stack", "_DEC_XFORM_MODE", "hasOwnProperty", "serviceEnv", "icon", "response", "extend", "svid", "\x3c!--[if IE ", "name", "getTimezoneOffset", "hostname", "timeZone", "280px", "VID", "reset", "_getFP", "substr", "$super", "localStorage", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "width", "infoBox", "size", "floor", "(^|&)", "hasIndexedDB", "Linux", "direct", "EvpKDF", "online", "MD5", "risk_inspect", "object", "&business_site=", "httpfail", "parse", "ctripqa.com", "rms", "english", "min", "match", "scrH", "concat", "param", "stringify", "data_js", "Latin1", "ebooking.trip.com", "src", "__getKeys", "guid", "finalize", "JSON", "kdf", "//m.ctrip.com/restapi/infosec/", "AudioContext", "token", "_mode", "Hasher", "_append", "mode", "__CryptoJS", "replace", "_iKey", "substring", "ciphertext", "CipherParams", "fat", "code", "unknown", "&dimensions=", "iterations", "POST", "openDatabase", "jigsawVerificationMain_", "words", "flaState", "//ebooking.trip.com/", "error", ":http error", "CtripUserInfo", "call", "hasher", "_devTrace", "_parse", "Pkcs7", "imei", "keySize", "infosec_openid", "enc", "touchSupport", "tip", "ctrip.com", "status", "//ic.uat.ctripqa.com/", "onerror", "=([^;]*)(;|$)", "indexOf", "__bfi", "getTime", "?callback=", "//m.trip.com/restapi/infosec/", "tid", "slice", "random", "cookieEnabled", "Hex", "lastIndex", "decryptBlock", "withCredentials", "key", "200", "splice", "mixIn", "captcha", "WordArray", "unpad", "ebooking", "ShockwaveFlash.ShockwaveFlash", "//m-ebooking.trip.com/", "serviceerror", "_keySchedule", "_getRmsToken", "clamp", "BlockCipherMode", "post", "_hash", "refresh", "resultHandler", "hasDataBase", "238397", "_prevBlock", "ceil", "meta", "userAgent", "StreamCipher", "_invKeySchedule", "colorDepth", "vid", "cupClass", "_nRounds", "idfa", "screen", "__rmsbfi", "format", "GUID", "Base64", "createElement", "__changeStyle", "_hasher", "HMAC", "_map", "__sJSON", "_iv", "_createHelper", "img_info", "toString", "_xformMode", "iOS", "identify", "$1\n", "keyboardEventExist", "process_type", "language", "process_value", "_getStatus", "height", "data", "cookie", "Decryptor", "_key", "AES", "Encryptor", "_doFinalize", "protocol", "hasLocalStorage", "processBlock", "send", "1.0.3", "sVID", "create", "timeout", "blockSize", "_bfi", "loaded", "scrW", "algo", "join", "constructor", "salt", "OpenSSL", "0000", "split", "data/js/v4", "createDecryptor", "triplinkintl.com", "onreadystatechange", "businessSite", "Cipher", "_createHmacHelper", "_ENC_XFORM_MODE", "hidden", "//ebooking.ctrip.com/", "supportXHR", "_data", "decrypt", "update", "PasswordBasedCipher", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "appId", "uid", "ontouchstart", "getItem", "content", "captcha/v4/", "overtime", "jigsawCaptchaMainModule_", "m-ebooking.trip.com", "&version=", "head", "uat", "toUpperCase", "location", "referrer", "platform", "keywords", "site", "http error", "//ic.trip.com/", "now", "doNotTrack", "http:", "encryptBlock", "https:", "sessionStorage", "&extend_param=", "_doReset", "_doProcessBlock", "webkitAudioContext", "toLowerCase", "_doCryptBlock", "risk_level", "href"];
!function (e, x) {
  !function (x) {
    for (; --x;) e.push(e.shift());
  }(++x);
}(_0x3500, 147);
var _0x596e = function (e, x) {
  return _0x3500[e -= 0];
};

var _0x31271b = _0x596e

window["__sJSON"] = {
    stringify: function (e) {
      var x = _0x31271b,
        t = typeof e;
      if (t != "object" || null === e) return "string" == t && (e = window["__quote"](e)), String(e);
      var r,
        i,
        n = [],
        a = e && e["constructor"] == Array,
        c = window["__sJSON"]["stringify"];
      for (r in e) t = typeof (i = e[r]), e.hasOwnProperty(r) && (t == "string" ? i = window.__quote(i) : t == "object" && null !== i && (i = c(i)), n["push"]((a ? "" : '"' + r + '":') + String(i)));
      return (a ? "[" : "{") + String(n) + (a ? "]" : "}");
    },
    parse: function (_0x26d13d) {
      var _0x33f770 = _0x31271b;
      return window[_0x33f770("0x128")] ? window[_0x33f770("0x128")].parse(_0x26d13d) : eval("(" + _0x26d13d + ")");
    }
  }, window["__quote"] = function (e) {
    var x = _0x31271b,
      t = /[\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
      r = {
        "\b": "\\b",
        "\t": "\\t",
        "\n": "\\n",
        "\f": "\\f",
        "\r": "\\r",
        '"': '\\"',
        "\\": "\\\\"
      };
    return t.lastIndex = 0, t["test"](e) ? '"' + e["replace"](t, function (e) {
      var t = x,
        i = r[e];
      return typeof i === "string" ? i : "\\u" + ("0000" + e.charCodeAt(0)["toString"](16)).slice(-4);
    }) + '"' : '"' + e + '"';
  }, window.__getKeys = function (e) {
    var x = _0x31271b,
      t = [];
    for (var r in e) t["push"](r);
    return t;
  };

const key = CryptoJS.enc.Utf8.parse("YnV0dGVycz3MzRkw");

function encryptBody(plaintext) {
    const text = typeof plaintext === "object" 
        ? JSON.stringify(plaintext) 
        : plaintext;

    const encrypted = CryptoJS.AES.encrypt(
        CryptoJS.enc.Utf8.parse(text),
        key,
        {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }
    );
    return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
}

function decryptBody(ciphertextBase64) {

    const decrypted = CryptoJS.AES.decrypt(
        {
            ciphertext: CryptoJS.enc.Base64.parse(ciphertextBase64)
        },
        key,
        {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }
    );

    return decrypted.toString(CryptoJS.enc.Utf8);
}

obj = {
    "accessCode": "IBUPCAUTEHNTICATE",
    "strategyCode": "PWDLOGIN",
    "authenticateInfo": {
        "loginName": "727735746@qq.com",
        "password": "12345678"
    },
    "frontRiskInfo": {
        "token": "p0791303b93360e8febbcb3504999a3175ce36752b51a!REGION!SIN",
        "sliderVersion": "1.0.3",
        "businessSite": "ibu_login_online_pic",
        "rid": "F9899891A7DB497B8EEB5F360022B6D7"
    },
    "context": {
        "sequenceId": "35ceb7b3-4030-43ce-be65-c9b2d0c6aaa9",
        "needVerifyEmail": "false",
        "needImportOrder": "false"
    },
    "clientInfo": {
        "locale": "zh-HK",
        "clientId": "09034158419539680350",
        "pageId": "10320668088",
        "rmsToken": "fp=BB379A-5EDF21-15AD49&vid=1761882238016.647fHwkeOhM3&pageId=10320668088&r=084171eb1f584bc69bdb0d953e26d8e3&ip=undefined&rg=b4&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36&d=hk.trip.com&v=25&kpg=0_0_0_1_2672_10_0_0_0_0&adblock=F&cck=F&ftoken="
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
        "extension": [{
            "name": "moduleName",
            "value": "PubHeader"
        }, {
            "name": "sdkName",
            "value": "onlinePopup"
        }, {
            "name": "sdkVersion",
            "value": "3.1.40"
        }, {
            "name": "platform",
            "value": "PC"
        }, {
            "name": "sysCode",
            "value": "999"
        }, {
            "name": "fromPageId",
            "value": "10320668088"
        }, {
            "name": "sequence",
            "value": "35ceb7b3-4030-43ce-be65-c9b2d0c6aaa9"
        }],
        "Locale": "zh-HK",
        "Language": "hk",
        "Currency": "CNY",
        "ClientID": ""
    }
}

// res = encryptBody(JSON.stringify(obj));
// console.log(res)

encry_test = "Zmsje75+sMYEQOqoxFML/xUT/WTHEpWvFfJ4DrWg9H5sDDEXCkWSGBLdVw2lzdPf7n93pIIWRo0m75Cm7N2LluCdY4YEtYmTev4QRRiIxpxoEVxf6gL6Jh9t+N0f9aM2dkDPV7Bc0qqOpmQiYtJk+k9UOR6WhEYpeoB/9ld2a6UzQhuIdI0+YTS9/opGGSgANI/qX3KPuhD1kNGOvuXCxqTwpuyNAcrmtoqACwTwVHI95/BKTOE0j7F4uCkCHejPCaKOCcSJdsM3Xux+HsNMfhvBNGDu76sAc2HqzVxNogVGB1yrZSwPzh1eswxYbOCj1ubARj5yoQWAMAGz70AWIe2TL6eaPC6nxQVFGewmGHLPKHx5+AmTwa74+7+ZtF7pJPqIzCvdnX0BYU6ce21yKPztAWeoIs8YPhdyMH3hOFeWSk7mv1Yd5+bq1HNG4dY5n+B9UPbQzGrEBgfVy9YMpKmoWKpSP9sJ88361wKFErsB8vlogSxsd45yPD1OtLcmcomSoDHSU6lQgqmeTOPCM/Er5382JAOXtgmsW1/avuk3ZsuzgfjYuCevWmOBsTEWQqolFjQCpFkrCOS32ki6b4JaUyT+slC1cjF11iazdB02pNYRf/sLFd5Zt1HrBuHTFbXJ8IuyHg8KSOQ9jO4CGQ=="


decry = decryptBody(encry_test);
console.log(decry)
function md5(str) {
    return CryptoJS.MD5(str).toString();
}


class CustomAES {
    constructor(keySize = 128, iterationCount = 1000) {
        this.keySize = keySize / 32;
        this.iterationCount = iterationCount;
        this.key = CryptoJS.lib.WordArray.create([
            -1893508159,
            -893289914,
            1393320303,
            -231424392,
            -351831057
        ], 16);
    }
    encrypt(ivHex, plaintext) {
        const iv = CryptoJS.enc.Hex.parse(ivHex);

        const encrypted = CryptoJS.AES.encrypt(
            CryptoJS.enc.Utf8.parse(plaintext),
            this.key,
            {
                iv: iv,         // CBC 模式下必须
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            }
        );

        return encrypted.ciphertext.toString(CryptoJS.enc.Base64);
    }

    decrypt(ivHex, ciphertextBase64) {
        const iv = CryptoJS.enc.Hex.parse(ivHex);

        const cipherParams = CryptoJS.lib.CipherParams.create({
            ciphertext: CryptoJS.enc.Base64.parse(ciphertextBase64)
        });

        const decrypted = CryptoJS.AES.decrypt(
            cipherParams,
            this.key,
            {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            }
        );
        return decrypted.toString(CryptoJS.enc.Utf8);
    }
}

const ivHex = "69783956775867344e5853626b645431";
obj = {
    "rt": "fp=BB379A-5EDF21-15AD49&vid=1765423717946.8ff9yPtQNDRZ&pageId=10320668055&r=64a654918e6b476793b2275ad57ecf26&ip=undefined&rg=undefined&kpData=0_0_0&kpControl=0_0_0-0_0_0&kpEmp=0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0-0_0_0_0_0_0_0_0_0_0&screen=1920x1080&tz=+8&blang=zh-CN&oslang=zh-CN&ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36&d=hk.trip.com&v=25&kpg=0_1_0_0_58926_26_1_2_0_0&adblock=F&cck=F&ftoken=",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "p": "pc",
    "fp": "BB379A-5EDF21-15AD49",
    "vid": "1765423717946.8ff9yPtQNDRZ",
    "sfp": undefined,
    "identify": "aBB379A-5EDF21-15AD49",
    "svid": undefined,
    "guid": "09034171314349030556",
    "h5_duid": null,
    "pc_duid": null,
    "hb_uid": null,
    "pc_uid": null,
    "h5_uid": null,
    "infosec_openid": null,
    "device_id": "8dd9071a716b799152b40c6618b1ad39",
    "client_id": "d7FcRtOJEen0uliTHQg0Z65nwY3yyfth",
    "pid": "1120620054149430",
    "sid": "ONzmrJfFQPaFxYca",
    "login_uid": "5030570204",
    "client_type": "PC",
    "site": {
        "type": "PC",
        "url": "https://hk.trip.com/account/signin?backUrl=https%3A%2F%2Fhk.trip.com%2Fmembersinfo%2Fprofile%2F%3Flocale%3Dzh-HK%26curr%3DCNY",
        "ref": "https://hk.trip.com/passport/logout?backurl=https%3A%2F%2Fhk.trip.com%2Fmembersinfo%2Fprofile%2F%3Flocale%3Dzh-HK%26curr%3DCNY&locale=zh-HK&curr=CNY",
        "title": "Sign in to Trip.com",
        "keywords": ""
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

const aes = new CustomAES();

// const plaintext = JSON.stringify(obj);
function encBody(plaintext) {
    plaintext = window["__sJSON"].stringify(plaintext)
    return aes.encrypt(ivHex, plaintext);
}

// const encrypted = encBody(obj);
// console.log("ciphertext:", encrypted);
function decBody(ciphertext) {
    return aes.decrypt(ivHex, ciphertext);
}
encrypted = 'YV0zJirkIchRtt6aPaUNZ/IyfvPJyfqK23RUwUzG403pTjWt3pijuH2cg7EKN0po2MOGCVbCzzi/ZIqKQIangLMsA7LnjDZi9oBoavbJub9WZYpwf2EksLY1avUZFh4ZR1mSF9EeGiErx7a7VSwhmMvEB5wWsBCylmTUHY1cyXnes6zYgD/J0635c3s0oYuDMk2PO+RKMKueQCB6v1BrBj/1 ly78DzAADkw+mIBy4BTbD1s2iEWMbHARfhy4v9A2Mk2PO+RKMKueQCB6v1BrBj/1 ly78DzAADkw+mIBy4BSmDlpX8kH+xs3X5gGuYZgpxFRSO4eZ2DoV9wYKwA3bMg329S/sYXBJbCgRFessKMUIQE+AfhfaVM3XHGycN+RxeXjoIrvdS8Gm0owru2pMMxjgHZjOeHq0baprm/zH/V6wq3IdIEQyKnSj7dB0W+4 Tf61N7fpgtFpCrDiSigot1XQh1ZYjCP9zlCpFirzPbyVQFBHiAvFO4sxcsC7Dj9lPGoLzzfvJcwng2HjZMi5Cal35QWU0xVck2AhS8eZV8+LiqltIGpDT6MRXHTYY6TiGVK8c0+9 ThWUxmLfDtRUTR1o8Ml90cNpQq6yzdB0YazrCXU32FxCqnlQwB9zYZwYdg5bVpxNTgJNdLrWw66iB7Q=='
// const decrypted = decBody(encrypted);
// console.log("decrypted:", decrypted);