from django.conf.urls import url
from cart.views import Cart
urlpatterns = [
    url(r'^cart/$', Cart.as_view(), name="cart"),  # 购物车
]
