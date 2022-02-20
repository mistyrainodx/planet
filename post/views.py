

from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views import View
import simplejson
import datetime
from post.models import Post,Content
from user.models import User
from user.views import authenticate

from utils import jsonify
from django.db import transaction


class PostView(View):
    # 发起GET请求，通过查询字符串 http://url/posts/?page=2
    # 查询第二页数据
    def get(self, request:HttpRequest):
        print('get ~~~~~~~~~')

        '''
        GET /posts/?page=3&size=20
        文章列表页，视图类PostView
        '''
        try: #页码
            page = int(request.GET.get('page', 1))
            page = page if page > 0 else 1
        except:
            page = 1

        try: #每页文章数量
            size = int(request.GET.get('size', 20))
            size = size if size > 0 and size < 101 else 20
        except:
            size = 20


        try: #查询数据库定位文章
            start = (page-1) * size
            posts = Post.objects.order_by('-pk')[start: start+size]

        try:
            posts = Post.objects.order_by('-pk')
            print(posts.query)

            return JsonResponse({
                'posts': [
                    jsonify(post, allow=['id', 'title']) for post in posts
                ]
            })
        except Exception as e:
            return HttpResponse(status=400)

    @authenticate
    def post(self, request:HttpRequest):
        print('post +++++')
        post = Post()
        content = Content()

        try:
            payload = simplejson.loads(request.body)
            post.title = payload['title']
            post.author = User(id=request.user.id)
            post.postdate = datetime.datetime.now(
                datetime.timezone(datetime.timezone(datetime.timedelta(hours=8)))
            )

            with transaction.atomic():
                post.save()

                content.post = post
                content.content = payload['content']
                content.save()
            return JsonResponse({
                'post': jsonify(post, allow=['id', 'title'])
            })
        except Exception as e:
            print(e)
            return HttpResponse(status=400)


@require_GET
def getpost(request:HttpRequest, id):
    # 发起GET请求，通过查询字符串
    # http://url/posts/2
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        return JsonResponse({
            'post': {
                'id': post.id,
                'title': post.title,
                'author': post.author_id,
                'postdate': post.postdate.timestamp(),
                'content': post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponse(status=404)