from django.shortcuts import render
from django.views import View

# Create your views here.
from product.models import ProCategory, ProSKU


class Show(View):
    def get(self, request):
        context = {
        }
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
