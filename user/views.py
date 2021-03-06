from django.http import HttpRequest, JsonResponse, HttpResponse
import simplejson
from django.views.decorators.http import require_http_methods, require_POST

from utils import jsonify
from .models import User
import jwt
import bcrypt
import datetime
from django.conf import settings

AUTH_EXPIRE = 8 * 60 * 60 # 8小时过期
AUTH_HEADER = "HTTP_JWT" # 浏览器端是jwt，服务器端被改为全大写并加HTTP_前缀

def authenticate(viewfunc):
    def wrapper(*args):

        *s, request = args
        print(s)
        print(request)

        jwtheader = request.META.get(AUTH_HEADER,'')
        if not jwtheader:
            return HttpResponse(staus=401)
        print(jwtheader)
        try:
            payload = jwt.decode(
                jwtheader,
                settings.SECRET_KEY,
                algorithms=['HS256'],
                options={'verify_signature': True}
            )
        except Exception as e:
            return HttpResponse(status=401)

        try:
            user_id = payload.get('user_id', 0)
            if user_id == 0:
                return HttpResponse(status=401)
            user = User.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            return HttpResponse(status=401)
        response = viewfunc(*args)
        return response
    return wrapper

def gen_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp())  + AUTH_HEADER
    }, settings.SECRET_KEY)



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


@require_POST
def login(request):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password'].encode()

        user = User.objects.get(email=email)

        if bcrypt.checkpw(password, user.password.encode()):
            token = gen_token(user.id)
            res = JsonResponse({
                'user':jsonify(user, exclude=['password']),
                'token': token
            })
            res.set_cookie('jwt', token)
            return res

        else:
            return JsonResponse({'error':'用户名或密码错误'}, status=400)
    except Exception as e:
        return JsonResponse({'error':'用户名或密码错误'}, status=400)



@require_POST
@authenticate
def test(request):
    print(request.user)
    return JsonResponse({}, status=200)
# test = authenticate(test) --> return wrapper
# test(request) = authenticate(test)(request) = wrapper(request)
# return reponse = return viewfunc(request+user) = test(request+user)

# 如果认证成功，则将查询到的user对象添加到请求对象中传入登陆函数

