# coding: utf-8
import datetime
import json
import logging
import random

import requests
from rest_framework import exceptions

# from Vote.settings import WX_SMART_CONFIG
# from authentication.models import User
# from ticket.functions import TicketAuthorize

logger = logging.getLogger('django')


# class WxInterface:
#     def __init__(self):
#         self.appid = WX_SMART_CONFIG['appid']
#         self.secret = WX_SMART_CONFIG['secret']
#
#     def code_authorize(self, code):
#         logger.info('=========================================================code_authorize')
#         url = "https://api.weixin.qq.com/sns/jscode2session"
#         params = {
#             'appid': self.appid,
#             'secret': self.secret,
#             'js_code': code,
#             'grant_type': 'authorization_code'
#         }
#         response = requests.get(url=url, params=params, verify=False)
#         if response.status_code != 200:
#             logger.info('WxInterface code_authorize response: %s' % response.text)
#             raise exceptions.ValidationError('连接微信服务器异常')
#         res = response.json()
#         if res.get('openid') and res.get('session_key'):
#             logger.info(res)
#             # 首先查询数据库中是否存在该用户信息
#             user = User.objects.filter(open_id=res['openid']).first()
#             if not user:
#                 # 给用户生成活动码
#                 seed = random.random()
#                 code = str(int(seed * 1000000))
#                 # 如果用户不存在，则向数据库插入数据
#                 user = User.objects.create(open_id=res['openid'], last_login=datetime.datetime.now(),
#                                            session_key=res['session_key'], code=code)
#             else:
#                 # 如果用户存在，更新用户信息
#                 user.last_login = datetime.datetime.now()
#                 user.save()
#             ticket = TicketAuthorize.create_ticket(res['openid'])
#             logger.info('=========================================================create ticket')
#             return {'user_id': user.open_id, 'ticket': ticket}
#         else:
#             logger.info('微信认证异常 code_authorize response: %s' % response.text)
#             raise exceptions.ValidationError('微信认证异常： %s' % json.dumps(res))
#
#     # 调用微信接口向用户发送客服文本消息
#     def send_customer_message(self, to_user, text, access_token):
#         url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + access_token
#         params = {
#             "touser": to_user,
#             "msgtype": "text",
#             "text": {
#                 "content": text
#             }
#         }
#         response = requests.post(url=url, params=params, verify=False)
#         if response.status_code != 200:
#             logger.info('WxInterface code_authorize response: %s' % response.text)
#             raise exceptions.ValidationError('连接微信服务器异常')
#         res = response.json()
#         logger.info('8'*70)
#         logger.info(res)
#         logger.info('8' * 70)
#         return
#
#     def get_access_token(self):
#         url = "https://api.weixin.qq.com/cgi-bin/token"
#         params = {
#             'appid': self.appid,
#             'secret': self.secret,
#             'grant_type': 'client_credential'
#         }
#         response = requests.get(url=url, params=params, verify=False)
#         if response.status_code != 200:
#             logger.info('WxInterface code_authorize response: %s' % response.text)
#             raise exceptions.ValidationError('连接微信服务器异常')
#         res = response.json()
#         logger.info('8' * 70)
#         logger.info(res)
#         logger.info('8' * 70)
#         return res['access_token']

# WxInterfaceUtil = WxInterface()
