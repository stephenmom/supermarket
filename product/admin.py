from product.models import ProCategory, ProSKU, PhotoAlbum, ProSPU, Carousel, ProductUnit, Activity, ActivityRegion,ActivityRegionProduct
from django.contrib import admin

"""
注册方式:
admin.site.register(模型类)

装饰器形式注册
@admin.register(模型类)
class XxxAdmin(admin.ModelAdmin):
    # 自定义后显示的类
"""


# admin.site.register(Category)
@admin.register(ProCategory)
class CategoryAdmin(admin.ModelAdmin):
    # 自定义后台
    list_display = ['id', 'category_name', 'category_introduce', 'category_add_time', 'category_status']
    list_display_links = ['id', 'category_name', 'category_introduce']


admin.site.register(ProductUnit)

admin.site.register(ProSPU)


# 商品sku
class GalleryInline(admin.TabularInline):
    model = PhotoAlbum
    extra = 1


@admin.register(ProSKU)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ["id", 'pro_name', 'pro_price', 'pro_unit', 'pro_inventory', 'pro_sales_volume', 'show_logo',
                    'pro_show', 'pro_category_id']
    list_display_links = ["id", 'pro_name', 'pro_price']

    search_fields = ['pro_name', 'pro_price']
    inlines = [
        GalleryInline,
    ]


# 首页管理
admin.site.register(Carousel)
admin.site.register(Activity)


class ActivityZoneGoodsInline(admin.TabularInline):
    model = ActivityRegionProduct
    extra = 2


@admin.register(ActivityRegion)
class ActivityZoneAdmin(admin.ModelAdmin):
    inlines = [
        ActivityZoneGoodsInline
    ]
