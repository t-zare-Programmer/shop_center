from django.db import models

from apps.accounts.models import CustomUser
from apps.products.models import Product


#_________________________________________________________________________________________
class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50,verbose_name="نوع انبار")

    def __str__(self):
        return self.warehouse_type_title

    class Meta:
        verbose_name = 'نوع انبار'
        verbose_name_plural = 'انواع روش انبار'
#_________________________________________________________________________________________
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType,on_delete=models.CASCADE,related_name='warehouse',verbose_name='انبار')
    user_registered = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='warehouse_registered',verbose_name='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='warehouse_products',verbose_name='کد کالا')
    qty =models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت واحد',null=True,blank=True)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"{self.warehouse_type} - {self.product}"

    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'
