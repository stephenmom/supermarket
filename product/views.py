from django.shortcuts import render, redirect, reverse
from django.views import View
from product.models import ProCategory, ProSKU
from product.models import Carousel, Activity, ActivityRegion


class Show(View):
    def get(self, request):
        """
        显示首页,需要获取
        :param request:
        :return:
        """
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
        return render(request, "shop/index.html", context)

    def post(self, request):
        context = {
        }
        return render(request, "shop/index.html", context)


class Category(View):
    def get(self, request, select_cate_id, order_id):
        """
        :param request: request
        :param select_cate_id: 当前选中的分类id
        :param order_id: 用于排序的order_id
        :return: 返回分类页面
        """
        # 获取到所有的分类 ,用于展示分类
        all_category = ProCategory.objects.all()
        # 获取用户当前选中的分类,便于判断
        select_category = ProCategory.objects.filter(pk=select_cate_id).first()
        # 获取当前分类的中所有的sku信息,用于展示
        prosku_ob = ProSKU.objects.filter(pro_category_id=select_category, pro_status=False, pro_show=1)
        # 排序规则的列表
        order_rule = ["id", "pro_sales_volume", "-pro_price", "pro_price", "-pro_add_time"]
        # 将排序id强制类型转换为 int类型
        int_order = 0
        # 如果字符串id不为int类型,那么就直接赋值为 0
        if order_id.isdecimal():
            int_order = int(order_id)
            if int_order > order_rule.__len__() - 1:
                int_order = 0
        # 对sku进行排序
        all_prosku = prosku_ob.order_by(order_rule[int_order])
        context = {
            "all_category": all_category,
            "select_category": select_category,
            "all_prosku": all_prosku,
            "order_id": order_id
        }
        return render(request, "shop/category.html", context)

    def post(self, request):
        context = {
        }
        return render(request, "shop/category.html", context)


class Cate(View):
    def get(self, request):
        """
        分类无参数url路由,提供无参数的Category连接
        :param request:
        :return:
        """
        cate = ProCategory.objects.all().first()
        ki = {"select_cate_id": ProCategory.objects.all().first().pk, "order_id": 0}
        return redirect("product:category", **ki)

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
        return redirect("product:detail", args=1)
