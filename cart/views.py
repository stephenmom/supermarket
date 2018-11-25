from django.shortcuts import render

# Create your views here.
from django.views import View


class Cart(View):
    def get(self, request):
        context = {

        }
        return render(request, "shop/shopcart.html", context)

    def post(self, request):
        context = {

        }
        return render(request, "shop/shopcart.html", context)
