#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : url
# @Time         : 2023/12/4 17:02
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying


@retrying
@lru_cache(maxsize=1024)
def shorten_url(url, shortener='dagd'):
    """
        https://w3.do/k0xi_szO
        https://clck.ru/36vUv9
        https://da.gd/haFET # 耗时更短
        https://tinyurl.com/ym8xkpyl
    :param url:
    :param shortener:
    :return:
    """
    if shortener.startswith('w3'):
        url = f"https://w3.do/get?url={url}"
        return f"""https://{requests.get(url).json().get("url")}"""

    from pyshorteners import Shortener
    return Shortener().__getattr__(shortener).short(url)


def qrCallback(uuid, status, qrcode):
    # logger.debug("qrCallback: {} {}".format(uuid,status))
    if status == "0":
        try:
            from PIL import Image

            img = Image.open(io.BytesIO(qrcode))
            _thread = threading.Thread(target=img.show, args=("QRCode",))
            _thread.setDaemon(True)
            _thread.start()
        except Exception as e:
            pass

        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)


@retrying
@lru_cache(maxsize=1024)
def to_qrcode(url, qrcode_api="https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}"):
    """
        apis = [
            "https://api.isoyu.com/qr/?m=1&e=L&p=8&url={}",
            "https://api.qrserver.com/v1/create-qr-code/?data={}",
            # "https://api.qrserver.com/v1/create-qr-code/?size=500×500&data={}",
            "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}"
        ]

        for api in apis:
            print(to_qrcode(url, api))

    :param url:
    :param qrcode_api:
    :return: https://api.isoyu.com/qr/?m=1&e=L&p=20&url=https://vip.chatllm.vip/
    """
    return qrcode_api.format(url)


if __name__ == '__main__':
    url = "https://vip.chatllm.vip/"
    # print(shorten_url(url, 'w3'))
    # print(shorten_url(url, 'dagd'))
    # print(shorten_url(url, 'clckru'))
    # print(shorten_url(url, 'tinyurl'))

    apis = [
        "https://api.isoyu.com/qr/?m=1&e=L&p=8&url={}",
        "https://api.qrserver.com/v1/create-qr-code/?data={}",
        # "https://api.qrserver.com/v1/create-qr-code/?size=500×500&data={}",
        "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}"
    ]

    for api in apis:
        print(to_qrcode(url, api))
