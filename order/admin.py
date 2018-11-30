from django.contrib import admin

# Register your models here
from order.models import OderInfo, Payment, Transport,OrderGoods

admin.site.register(Payment)
admin.site.register(Transport)
admin.site.register(OrderGoods)


@admin.register(OderInfo)
class OderInfoAdmin(admin.ModelAdmin):
    list_display = ["id",
                    'order_number',
                    'order_money',
                    'user_id',
                    'order_user_name',
                    'order_user_phone',
                    'order_address',
                    'order_status_now',
                    'order_transport',
                    'order_payment',
                    'really_pay_money', ]
    list_display_links = ["id",
                          'order_number',
                          'order_money']
    search_fields = ['order_number', 'order_user_name']
