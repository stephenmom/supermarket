from django.conf.urls import url
from cart.views import CartAdd, Cart, CartInfo, CartChange

urlpatterns = [
    url(r'^add/$', CartAdd.as_view(), name="add"),  # 购物车添加
    url(r'^cart/$', Cart.as_view(), name="cart"),  # 购物车添加
    url(r'^cartchange/$', CartChange.as_view(), name="cartchange"),  # 购物车修改
    url(r'^cart_info/$', CartInfo.as_view(), name="cart_info"),  # 购物车显示
]
