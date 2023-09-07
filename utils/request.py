# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import logging
from configparser import RawConfigParser
from typing import *

import aiohttp

# 不带这堆头部有时候也能成功请求，但是带上后成功的概率更高
BILIBILI_COMMON_HEADERS = {
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/114.0.0.0 Safari/537.36'
}

http_session: Optional[aiohttp.ClientSession] = None

logger = logging.getLogger(__name__)

def init():
    cfg = RawConfigParser()
    cfg.read("./config.ini")
    SESSDATA = dict(cfg.items("cookie"))['cookie']
    cookies = None
    if(len(SESSDATA)<=20):
        logger.warning('cookie值可能有误，未加载')
        logger.warning('无cookie可能无法获取到弹幕等')
        logger.warning('请在config.ini文件中填入自己的SESSDATA值')
    else:
        cookies = http.cookies.SimpleCookie()
        cookies['SESSDATA'] = SESSDATA
        cookies['SESSDATA']['domain'] = 'bilibili.com'
        logger.warning(f'cookie值已加载：{SESSDATA}')

    # ClientSession要在异步函数中创建
    async def do_init():
        global http_session
        http_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        if cookies is not None:
            http_session.cookie_jar.update_cookies(cookies)

    asyncio.get_event_loop().run_until_complete(do_init())
