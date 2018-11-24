from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^show/$', views.Show.as_view(), name="show"),  # 产品展示
    url(r'^category/(?P<select_cate_id>\d+)/(?P<order_id>\d)/$', views.Category.as_view(), name="category"),  # 产品分类
    url(r'^cate/$', views.Cate.as_view(), name="cate"),  # 产品分类无参数
    url(r'^detail/(?P<id>\d+).html$', views.ProDetail.as_view(), name="detail"),  # 产品详情
]
