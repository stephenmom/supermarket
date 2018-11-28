from django.contrib import admin

# Register your models here.
from user_info.models import Users, UserAddress

admin.site.register(Users)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["id",
                    'user_id',
                    'goods_user_name',
                    'goods_user_phone',
                    'goods_detail',
                    'default_address',
                    'province_id',
                    'city_id',
                    'district_id',
                    'street_id']
    list_display_links = ["id",
                          'goods_user_name',
                          'goods_user_phone']
    search_fields = ['goods_user_name', 'goods_user_phone']
