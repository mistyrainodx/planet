from django.conf.urls import url
from .views import PostView, getpost
from user.views import authenticate

urlpatterns = [
    # 路径/posts/
    # View类调用as_view()之后类等价一个视图函数，可以被装饰
    # 装饰器函数返回新函数
    url(r'^$', PostView.as_view()), #匹配路径/posts/
    url(r'^(\d+)$', getpost), #匹配路径/posts/(\d+)
]

# as_view()方法就是返回一个内建的 view(request, *args, **kwargs) 函数，本质上其实还是url映射到了函数上
# 只不过view函数内部会调用 dispatch(request, *args, **kwargs) 分发函数
# dispatch函数中使用request对象的请求方法小写和http_method_names中允许的HTTP方法匹配
# 匹配说明是正确的HTTP请求方法，然后尝试在View子类中找该方法，调用后返回结果。
# 找不到该名称方法，就执行http_method_not_allowed方法返回405状态码
# 看到了getattr等反射函数，说明基于反射实现的


