"""sp2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
                  url(r'^admin/', admin.site.urls, name="admin"),
                  url(r'^user/', include("user_info.urls", namespace="user_info")),
                  url(r'^product/', include("product.urls", namespace="product")),
                  url(r'^order/', include("order.urls", namespace="order")),
                  url(r'^cart/', include("cart.urls", namespace="cart")),
                  url(r'^ckeditor/', include("ckeditor_uploader.urls")),
                  url(r'^search/', include('haystack.urls')),
                  # 添加自己的应用的子路由
                  url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
