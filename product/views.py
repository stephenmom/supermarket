from django.shortcuts import render, redirect
from django.views import View
from product.models import ProCategory, ProSKU
from product.models import Carousel, Activity, ActivityRegion


class Show(View):
    def get(self, request):
        """首页"""
        # 获取轮播
        carousel = Carousel.objects.filter(carousel_status=False).order_by("-carousel_order")

        # 获取活动
        acts = Activity.objects.all()

        # 获取特色专区
        act_zones = ActivityRegion.objects.filter(region_show=True, region_status=False).order_by("-region_order")

        # 渲染数据
        context = {
            "all_carousel": carousel,
            "acts": acts,
            "act_zones": act_zones,
        }
        print(act_zones[0].region_name)
        return render(request, "shop/index.html", context)

    def post(self, request):
        context = {
        }
        return render(request, "shop/index.html", context)


class Category(View):
    def get(self, request, select_cate_id):
        if not select_cate_id:
            select_cate_id = 1
        all_category = ProCategory.objects.all()
        select_category = ProCategory.objects.filter(pk=select_cate_id).first()
        all_prosku = ProSKU.objects.filter(pro_category_id=select_category)
        context = {
            "all_category": all_category,
            "select_category": select_category,
            "all_prosku": all_prosku
        }
        return render(request, "shop/category.html", context)

    def post(self, request):
        context = {
        }
        return render(request, "shop/category.html", context)


class ProDetail(View):
    def get(self, request, id):
        try:
            goodsSku = ProSKU.objects.get(pk=id, pro_show=1)
        except ProSKU.DoesNotExist:
            # 跳转到首页
            return redirect("product:show")
        context = {
            "goodsSku": goodsSku
        }
        return render(request, "shop/detail.html", context)

    def post(self, request):
        pass
