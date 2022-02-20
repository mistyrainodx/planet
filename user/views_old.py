from django.http import HttpRequest, JsonResponse, HttpResponse
import simplejson
from django.views.decorators.http import require_http_methods

from .models import User
import jwt
import bcrypt
import datetime
from django.conf import settings

AUTH_EXPIRE = 8 * 60 * 60 # 8小时过期
AUTH_HEADER = "HTTP_JWT" # 浏览器端是jwt，服务器端被改为全大写并加HTTP_前缀

def gen_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp())  + AUTH_HEADER
    }, settings.SECRET_KEY)

def authenticate(viewfunc):
    def wrapper(request:HttpRequest):
        jwtheader = request.META.get(AUTH_HEADER, '')
        if not jwtheader:
            return HttpResponse(status=401)
        print(jwtheader)
        try:
            payload = jwt.decode(jwtheader, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload) # {'user_id': 106, 'timestamp': 1563181151}
        except Exception as e:
            return HttpResponse(status=401)
        print('-'*30)
        try:
            user_id = payload.get('user_id',0)
            if user_id == 0:
                return HttpResponse(status=401)
            user = User.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            return HttpResponse(status=4-1)

        response = viewfunc(request)
        return response
    return wrapper


#用户注册功能
@require_http_methods(['POST'])
def reg(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        query = User.objects.filter(email=email)
        print(query.query)
        if query.first():
            return  JsonResponse({'error': '用户已存在'})
        name = payload['name']
        password = payload['password'].encode()
        print(email, name, password)

        password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User()
        user.email = email
        user.name = name
        user.password = password.decode()
        user.save()
        return JsonResponse({'token':gen_token(user.id)},status=201)
    except Exception as e:
        return JsonResponse({'error':'用户名或密码错误'},status=400)


def jsonify(instance, allow=None, exclude=[]):
    modelcls = type(instance)
    # 筛选字段
    if allow:
        fn = (lambda x: x.name in allow)
    # 代码分解
    # for x.name in allow:
    #    return x（传入的字段field）
    else:
        fn = (lambda x: x.name not in exclude)
    # for x.name not in exclude:
    # return x(传入的字段field)

    return {k.name:getattr(instance, k.name) for k in filter(fn, modelcls._meta.fields)}
    #代码分解
    # for k in filter(fn, modelcls._meta.fields):
    #     return k.name:getattr(instance, k.name)
    # 判断查询字段是否在白名单列表中
    # modelcls._meta.fields(x变量) -->  fn

def login(request):
    try:
        payload = simplejson.loads(request.body)
        print(payload)
        email = payload['email']
        password = payload['password'].encode()
        print(email,password)

        user = User.objects.get(email=email)

        print(user.password)
        if bcrypt.checkpw(password, user.password.encode()):
            # 验证成功
            token = gen_token(user.id)

            res = JsonResponse({
                'user': jsonify(user, exclude=['password']),
                'token': token
            })
            res.set_cookie('jwt', token)
            return res
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'error': '用户名或密码错误'}, status=400)

@authenticate
def test(request):
    print(request.user)
    return JsonResponse({}, status=200)
# test = authenticate(test) --> return wrapper
# test(request) = authenticate(test)(request) = wrapper(request)
# return reponse = return viewfunc(request+user) = test(request+user)

# 如果认证成功，则将查询到的user对象添加到请求对象中传入登陆函数

