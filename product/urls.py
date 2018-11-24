from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^show/$', views.Show.as_view(), name="show"),  # 产品展示
    url(r'^category/(\d*)$', views.Category.as_view(), name="category"),  # 产品分类
    url(r'^detail/(?P<id>\d+).html$', views.ProDetail.as_view(), name="detail"),  # 产品详情
]
