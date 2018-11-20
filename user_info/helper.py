from django.shortcuts import redirect

from sp2 import settings


def verify_login_required(func):
    def verify(request, *args, **kwargs):
        # 判断session中是否有ID,如果没有说明没有登录，请登录
        if request.session.get("tellphone") is None:
            # 配置文件中获取登录的URL地址
            login_url = settings.LOGIN_URL
            return redirect(login_url)
        else:
            # 返回被调用函数
            return func(request, *args, **kwargs)

    return verify
