from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^makeorder/$', views.MaKeOrder.as_view(), name="makeorder"),  # 订单接收处理
    url(r'^submitorder/$', views.SubmitOrder.as_view(), name="submitorder"),  # 订单记录处理
    url(r'^show/$', views.OrderShow.as_view(), name="order_now"),
    url(r'^pay/$', views.OrderPay.as_view(), name="pay"),
]
