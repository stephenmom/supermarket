from product.models import ProCategory, ProSKU, PhotoAlbum, ProSPU
from django.contrib import admin


class ProCategoryInline(admin.StackedInline):
    model = ProSKU  # 该处配置多端表
    extra = 1


@admin.register(ProSKU)
class ProCategoryAdmin(admin.ModelAdmin):
    # 配置项
    #  每页显示多少项
    list_per_page = 5

    # 设置显示字段
    list_display = ['pro_name',
                    'pro_introduce',
                    'pro_price',
                    'pro_unit',
                    'pro_inventory',
                    'pro_sales_volume',
                    'pro_logo',
                    'pro_show',
                    'pro_status']  # 更改名字默认值.verbose_name='上级区域'

    # 在字段上添加一个连接, 能点进去编辑
    list_display_links = ['pro_introduce', 'pro_name']

    # 过滤器
    list_filter = ['pro_name']

    # 添加搜索框
    search_fields = ['pro_name']

    # 编辑或者添加的字段
    # fields = ['class_name', 'class_intro']

    # 将多端配置添加到管理界面
    # inlines = [
    #     ProCategoryInline
    # ]


admin.site.register(ProCategory)
admin.site.register(ProSPU)
admin.site.register(PhotoAlbum)
