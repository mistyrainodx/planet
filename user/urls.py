from django.conf.urls import url
from .views import reg,login

urlpatterns = [
    url(r'^reg$', reg), # /users
    url(r'^login$', login), # /users
]