from django.conf.urls import url
from user_info import views

urlpatterns = [
    url(r'^login/$', views.user_login, name="login"),  # 用户登录
    url(r'^register/$', views.register, name="register"),  # 用户登录
]
