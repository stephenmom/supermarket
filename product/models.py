from django.db import models


# Create your models here.


class ProCategory(models.Model):
    """
    商品分类
    ID
    分类名
    分类简介
    添加时间
    修改时间
    是否删除
    """
    category_name = models.CharField(max_length=32, verbose_name='分类名')
    category_introduce = models.CharField(max_length=50, verbose_name='分类简介', null=True, blank=True)
    category_add_time = models.DateTimeField(auto_now_add=True, verbose_name="分类添加时间")
    category_edit_time = models.DateTimeField(auto_now=True, verbose_name="分类修改时间")
    category_status = models.BooleanField(default=False, verbose_name="删除状态")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "分类管理"
        verbose_name_plural = verbose_name


class ProSKU(models.Model):
    """
        商品SKU表
        ID
        商品名
        简介
        价格
        单位
        库存
        销量
        LOGO地址
        是否上架
        商品分类ID
        商品spu_id
        添加时间
        修改时间
        是否删除
    """
    SHOW_STATUS_CHOICES = (
        (1, '上架'),
        (2, '下架'),
    )
    pro_name = models.CharField(max_length=32, verbose_name='商品名')
    pro_introduce = models.CharField(max_length=50, verbose_name='商品简介', null=True, blank=True)
    pro_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="商品价格")
    pro_unit = models.CharField(max_length=10, verbose_name='商品单位', default="个")
    pro_inventory = models.IntegerField(verbose_name='商品库存', default=0)
    pro_sales_volume = models.IntegerField(verbose_name='商品销量', null=True, blank=True)
    pro_logo = models.ImageField(upload_to='pro', verbose_name='商品LOGO地址', null=True, blank=True, max_length=500)
    pro_show = models.IntegerField(choices=SHOW_STATUS_CHOICES, verbose_name='上架状态', default=1)
    pro_category_id = models.ForeignKey(to='ProCategory', on_delete=models.CASCADE, verbose_name="商品分类id")
    pro_spu_id = models.ForeignKey(to='ProSPU', on_delete=models.CASCADE, verbose_name="商品spuid")
    pro_add_time = models.DateTimeField(auto_now_add=True, verbose_name="商品添加时间")
    pro_edit_time = models.DateTimeField(auto_now=True, verbose_name="商品修改时间")
    pro_status = models.BooleanField(default=False, verbose_name="商品删除状态")

    def __str__(self):
        return self.pro_name

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = verbose_name


class ProSPU(models.Model):
    """
        商品SPU表
        ID
        名称
        详情
    """
    spu_name = models.CharField(max_length=32, verbose_name='商品spu名')
    spu_introduce = models.CharField(max_length=50, verbose_name='商品spu详情', null=True, blank=True)
    spu_add_time = models.DateTimeField(auto_now_add=True, verbose_name="商品spu添加时间")
    spu_edit_time = models.DateTimeField(auto_now=True, verbose_name="商品spu修改时间")
    spu_status = models.BooleanField(default=False, verbose_name="商品spu删除状态")

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name


class PhotoAlbum(models.Model):
    """
        商品相册
        ID
        图片地址
        商品SKUID
        添加时间
        修改时间
        是否删除
    """
    photo_url = models.ImageField(upload_to='photo', verbose_name='图片地址', null=True, blank=True, max_length=500)
    photo_sku_id = models.ForeignKey(to='ProSKU', on_delete=models.CASCADE, verbose_name="图片sku_id")
    photo_add_time = models.DateTimeField(auto_now_add=True, verbose_name="图片添加时间")
    photo_edit_time = models.DateTimeField(auto_now=True, verbose_name="图片修改时间")
    photo_status = models.BooleanField(default=False, verbose_name="图片删除状态")

    def __str__(self):
        return self.photo_url

    class Meta:
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name


class PhotoUnit(models.Model):
    """
        商品单位表
        ID
        单位名（斤，箱）
        添加时间
        修改时间
        是否删除
    """
    unit_name = models.CharField(max_length=10, verbose_name="单位添加时间", default="个")
    unit_add_time = models.DateTimeField(auto_now_add=True, verbose_name="单位添加时间")
    unit_edit_time = models.DateTimeField(auto_now=True, verbose_name="单位修改时间")
    unit_status = models.BooleanField(default=False, verbose_name="单位删除状态")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "商品单位管理"
        verbose_name_plural = verbose_name


class Carousel(models.Model):
    """
    首页轮播商品
    ID
    名称
    商品SKUID
    图片地址
    排序（order）
    添加时间
    修改时间
    是否删除
    """
    carousel_name = models.CharField(max_length=32, verbose_name="轮播图名字")
    carousel_sku_id = models.ForeignKey(to='ProSKU', on_delete=models.CASCADE, verbose_name="轮播sku_id")
    carousel_url = models.ImageField(upload_to='carousel', verbose_name='轮播图片地址', null=True, blank=True, max_length=500)
    carousel_order = models.IntegerField(null=True, blank=True, verbose_name="排序")
    carousel_add_time = models.DateTimeField(auto_now_add=True, verbose_name="轮播添加时间")
    carousel_edit_time = models.DateTimeField(auto_now=True, verbose_name="轮播修改时间")
    carousel_status = models.BooleanField(default=False, verbose_name="轮播删除状态")

    def __str__(self):
        return self.carousel_name

    class Meta:
        verbose_name = "轮播图管理"
        verbose_name_plural = verbose_name


class Activity(models.Model):
    """
        首页活动表
        ID
        名称
        图片地址
        url地址 www.jd.com
    """
    activity_name = models.CharField(max_length=22, verbose_name="活动名字")
    activity_photo = models.ImageField(upload_to='activity', verbose_name='活动图片地址', null=True, blank=True,
                                       max_length=500)
    activity_address = models.CharField(max_length=50, verbose_name="活动链接地址")

    def __str__(self):
        return self.activity_name

    class Meta:
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name


class ActivityRegion(models.Model):
    """
        首页活动专区
        ID
        名称
        描述
        排序
        是否上架
        添加时间
        修改时间
        是否删除
    """
    SHOW_STATUS_CHOICES = (
        (1, '上架'),
        (2, '下架'),
    )
    region_name = models.CharField(max_length=22, verbose_name="专区名字")
    region_introduce = models.CharField(max_length=50, verbose_name="专区描述")
    region_order = models.IntegerField(verbose_name="专区排序")
    region_show = models.IntegerField(choices=SHOW_STATUS_CHOICES, verbose_name="上架状态", default=1)
    region_add_time = models.DateTimeField(auto_now_add=True, verbose_name="专区添加时间")
    region_edit_time = models.DateTimeField(auto_now=True, verbose_name="专区修改时间")
    region_status = models.BooleanField(default=False, verbose_name="专区删除状态")

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name


class ActivityRegionProduct(models.Model):
    """
    首页专区活动商品表
    ID
    专区ID
    商品SKU ID
    添加时间
    修改时间
    是否删除
    """
    ARP_region_id = models.ForeignKey(to="ActivityRegion", on_delete=models.CASCADE, verbose_name="活动专区id")
    ARP_sku_id = models.ForeignKey(to="ProSKU", on_delete=models.CASCADE, verbose_name="专区活动商品sku_id")
    ARP_add_time = models.DateTimeField(auto_now_add=True, verbose_name="专区活动商品添加时间")
    ARP_edit_time = models.DateTimeField(auto_now=True, verbose_name="专区活动商品修改时间")
    ARP_status = models.BooleanField(default=False, verbose_name="专区活动商品删除状态")

    def __str__(self):
        return self.ARP_region_id

    class Meta:
        verbose_name = "专区活动商品管理"
        verbose_name_plural = verbose_name
