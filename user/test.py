# # import os,django
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
# # django.setup()
# #
# # from user.models import User
# #
# # mgr = User.objects
# # # print(type(mgr.all), mgr.all)
# # # print(mgr.values())
# # # print(mgr.filter(pk=1).values())
# # print(mgr.count())
# # print(mgr.exist())
#
# import jwt
#
# key = 'secret'
# token = jwt.encode({'payload':'abc123'}, key, 'HS256')
# token = bytes(token, encoding='utf-8')
# print(token, type(token), sep='\n')
#
# print(jwt.decode(token, key, algorithms=['HS256']))
#
# header, payload, signature = token.split(b'.')
# print(header, payload, signature, sep='\n')
#
# import base64
# def addeq(b:bytes):
#     '''为base64编码补齐等号'''
#     rest = 4 - len(b) % 4
#     return b + b'=' * rest
# print('header=', base64.urlsafe_b64decode((addeq(header))))
# print('payload=', base64.urlsafe_b64decode((addeq(payload))))
# print('signature=', base64.urlsafe_b64decode((addeq(signature))))
#
#
#
#
# from jwt import algorithms
#
# # 1 获取算法对象
# alg = algorithms.get_default_algorithms()['HS256']
# newkey = alg.prepare_key(key)
#
# print(newkey)
#
# # 2 获取前两部分 header.payload
# sign_input,_,_ = token.rpartition(b'.')
# print(sign_input)
#
# # 3 使用key 签名
# signature = alg.sign(sign_input, newkey)
# print(signature)
# print(base64.urlsafe_b64encode(signature))
#
# import bcrypt
# import datetime
#
# password = b'123456'
#
# print(bcrypt.gensalt())
# print(bcrypt.gensalt())
#
# # 拿到的盐相同，计算等到的密文相同
# salt = bcrypt.gensalt()
# print('======== same salt ===========')
# x = bcrypt.hashpw(password, salt)
# y = bcrypt.hashpw(password, salt)
# print(x)
# print(y)
#
# print('=========different salt ==========')
# x = bcrypt.hashpw(password, bcrypt.gensalt())
# y = bcrypt.hashpw(password, bcrypt.gensalt())
# print(5, x)
# print(6, y)
#
# print(bcrypt.checkpw(password, x),len(x))
# print(bcrypt.checkpw(password + b' ', x), len(x))
#
#
# # 计算时长
# start = datetime.datetime.now()
# y = bcrypt.hashpw(password, bcrypt.gensalt())
# delta = (datetime.datetime.now() - start).total_seconds()
# print(10, 'duration={}'.format(delta))
#
# # 检验时长
# start = datetime.datetime.now()
# y = bcrypt.checkpw(password, x)
# delta = (datetime.datetime.now() - start).total_seconds()
# print(y)
# print(11, 'duration={}'.format(delta))
#
# start = datetime.datetime.now()
# y = bcrypt.checkpw(b'1', x)
# delta = (datetime.datetime.now() - start).total_seconds()
# print(y)
# print(12, 'duration={}'.format(delta))
#
#

import jwt
import datetime
import threading

event = threading.Event()
key ='magedu'

data = jwt.encode({
    'name':'tom',
    'age':20,
    'exp': int(datetime.datetime.now().timestamp()) + 10,
}, key)
# 不校验签名提取header
print(jwt.get_unverified_header(data))

try:
    while not event.wait(1): #event.wait = false
        print(jwt.decode(data, key, algorithms=['HS256']))
        print(datetime.datetime.now().timestamp())
except jwt.ExpiredSignatureError as e:
    print(e)