# coding: utf-8


# coding: utf-8

from Vote.settings import WX_SMART_CONFIG
import requests
import logging
from rest_framework import exceptions

logger = logging.getLogger('django')


class WxInterface:
    def __init__(self):
        self.appid = WX_SMART_CONFIG['appid']
        self.secret = WX_SMART_CONFIG['secret']

    def get_access_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'grant_type': 'client_credential'
        }
        response = requests.get(url=url, params=params, verify=False)
        if response.status_code != 200:
            logger.info('WxInterface code_authorize response: %s' % response.text)
            raise exceptions.ValidationError('连接微信服务器异常')
        res = response.json()
        logger.info('8' * 70)
        logger.info(res)
        logger.info('8' * 70)
        return res['access_token']

    def state(self, openid):
        access_token = WxInterfaceUtil.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
            access_token, openid)
        params = {
            'appid': WX_SMART_CONFIG['APP_ID'],
            'secret': WX_SMART_CONFIG['APP_SECRET'],
            'grant_type': 'client_credential'

        }
        response = requests.get(url=url, params=params, verify=False)
        if response.status_code != 200:
            raise exceptions.ValidationError('连接微信服务器异常')
        res = response.json()
        return res['subscribe']


WxInterfaceUtil = WxInterface()
