# -*- coding:utf-8 -*-
__author__ = 'Lin_Tong'

import json
import urllib
import urllib.request
import urllib.parse
from urllib.error import URLError
import urllib3
import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)
class OAuthQQ:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': 'get_user_info',
                  'state': 1}
        url = 'https://graph.qq.com/oauth2.0/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}    # 回调地址
        param = urllib.parse.urlencode(params)
        #url = 'https://graph.qq.com/oauth2.0/token?%s' % urllib.parse.urlencode(params)
        #req=urllib.request.Request(url)
        # 访问该网址，获取access_token
        url = 'https://graph.qq.com/oauth2.0/token?'+param
        req=urllib.request.Request(url)
        #req=urllib.request.(url,param)
        try:
            response = urllib.request.urlopen(req)

        except URLError as e:
            print("出错")
            print('Reason',e.reason)
        else:
            f = response.read()
            f=f.decode('utf-8')

            result = urllib.parse.parse_qs(f, True)
            access_token = str(result['access_token'][0])
            self.access_token = access_token
            return access_token




    def get_open_id(self):
        """获取QQ的OpenID"""
        params = {'access_token': self.access_token}
        url = 'https://graph.qq.com/oauth2.0/me?%s' % urllib.parse.urlencode(params)

        response = urllib.request.urlopen(url).read()
        v_str = str(response)[9:-3]  # 去掉callback的字符
        v_str = v_str[2:-2]
        print(v_str)

        v_json = json.loads(v_str)
        print(v_json)
        openid = v_json["openid"]
        self.openid = openid
        return openid

    def get_qq_info(self):
        """获取QQ用户的资料信息"""
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid}
        url = 'https://graph.qq.com/user/get_user_info?%s' % urllib.parse.urlencode(params)

        response = urllib.request.urlopen(url).read()
        return json.loads(response)
