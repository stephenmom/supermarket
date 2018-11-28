from django.conf.urls import url
from order import views
urlpatterns = [
    url(r'^makeorder/$', views.MaKeOrder.as_view(), name="makeorder"),  # 用户注册
]
