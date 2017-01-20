# -*- coding: utf-8 -*-

import base64
import urllib
import urllib2
import requests
import re
import json
import rsa
import binascii

# encode username
def get_username(user_id):
    user_id_ = urllib.quote(user_id)
    su = base64.encodestring(user_id_)
    return su

#encode password
def get_password_rsa(USER_PSWD, PUBKEY, servertime, nonce):
    rsa_pubkey = int(PUBKEY, 16)
    key_1 = int('10001', 16)
    key = rsa.PublicKey(rsa_pubkey, key_1)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(USER_PSWD)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)  # to 16
    return passwd

def get_parameter():
    username = '18952517912'   #set by your own
    password = 'python'             #set by your own
    su = get_username(username)
    url = 'https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack&su=' + su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
    r = requests.get(url)
    p = re.compile('\((.*)\)')
    json_data = p.search(r.text).group(1)
    data = json.loads(json_data)
    PUBKEY = data['pubkey']
    servertime = str(data['servertime'])
    nonce = data['nonce']
    rsakv = str(data['rsakv'])
    sp = get_password_rsa(password, PUBKEY, servertime, nonce)
    return servertime, nonce, rsakv, sp, su

def get_ticket():
    servertime, nonce, rsakv, sp, su = get_parameter()
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A//api.weibo.com/oauth2/default.html&response_type=code&client_id=3828611682',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    content = {
        'entry': 'openapi',
        'gateway': '1',
        'from': '',
        'savestate': '0',
        'useticket': '1',
        'pagerefer': '',
        'ct': '1800',
        's': '1',
        'vsnf': '1',
        'vsnval': '',
        'door': '',
        'appkey': 'z2ANX',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': sp,
        'sr': '1280*1024',
        'encoding': 'UTF-8',
        'cdult': '2',
        'domain': 'weibo.com',
        'prelt': '633',
        'returntype': 'TEXT'
    }
    url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    r = requests.post(url=url, headers=header, data=content)
    json_data = r.text
    data = json.loads(json_data)
    ti = data['ticket']
    return ti

def get_code():
    ticket = get_ticket()
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A//api.weibo.com/oauth2/default.html&response_type=code&client_id=3828611682',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    content = {
        'action':'login',
        'display':'default',
        'withOfficalFlag':'0',
        'quick_auth':'false',
        'withOfficalAccount':'',
        'scope':'',
        'ticket':ticket,
        'isLoginSina':'',
        'response_type':'code',
        'regCallback':'https%3A%2F%2Fapi.weibo.com%2F2%2Foauth2%2Fauthorize%3Fclient_id%3D350618137%26response_type%3Dcode%26display%3Ddefault%26redirect_uri%3Dhttps%253A%252F%252Fapi.weibo.com%252Foauth2%252Fdefault.html%26from%3D%26with_cookie%3D',
        'redirect_uri':'https://api.weibo.com/oauth2/default.html',
        'client_id':'3828611682',
        'appkey62':'z2ANX',
        'state':'',
        'verifyToken':'null',
        'from':'',
        'switchLogin':'0',
        'userId':'',
        'passwd':''
    }
    login_url = 'https://api.weibo.com/oauth2/authorize'
    r = requests.post(login_url, data=content, headers=header)
    code = re.split('=',r.url)[1]
    return code

if __name__ == '__main__':
    print get_ticket()
    print get_code()
    3828611682