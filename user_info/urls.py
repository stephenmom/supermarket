from django.conf.urls import url
from user_info import views

urlpatterns = [
    url(r'^login/$', views.UserLogin.as_view(), name="login"),  # 用户登录
    url(r'^register/$', views.Register.as_view(), name="register"),  # 用户注册
    url(r'^forget/$', views.Forget.as_view(), name="forget"),  # 用户注册
    url(r'^member/$', views.Member.as_view(), name="member"),  # 用户中心
    url(r'^logout/$', views.Logout.as_view(), name="logout"),  # 注销
    url(r'^info/$', views.Info.as_view(), name="info"),  # 个人资料
    url(r'^address/$', views.Address.as_view(), name="address"),  # 收货地址
    url(r'^deladdress/$', views.DelAddress.as_view(), name="deladdress"),  # 收货地址
    url(r'^addressedit/(?P<addpk>\d+)$', views.AddressEdit.as_view(), name="addressedit"),  # 修改地址
    url(r'^changedefaultaddress/$', views.ChangeDefaultAddress.as_view(), name="changedefaultaddress"),  # 修改默认收货地址
    url(r'^addressadd/$', views.AddressAdd.as_view(), name="addressadd"),  # 收货地址
    url(r'^send_msg_phone/$', views.send_msg_phone, name="send_msg_phone"),  # 个人资料
]
