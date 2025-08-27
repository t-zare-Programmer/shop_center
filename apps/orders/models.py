import uuid
from apps.products.models import Product
from django.db import models
from apps.accounts.models import Customer
from django.utils import timezone

#___________________________________________________________________________________________________
class PaymentType(models.Model):
    payment_title = models.CharField(max_length=50,verbose_name='نوع پرداخت')

    def __str__(self):
        return self.payment_title

    class Meta:
        verbose_name = 'نوع پرداخت'
        verbose_name_plural = 'انواع روش پرداخت'
#___________________________________________________________________________________________________
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='orders',verbose_name='مشتری')
    register_date = models.DateField(default=timezone.now,verbose_name='تاریخ درج سفارش')
    update_date = models.DateField(auto_now=True,verbose_name='تاریخ ویرایش سفارش')
    is_finally = models.BooleanField(default=False,verbose_name='نهایی شده')
    order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,verbose_name='کد تولیدی برای سفارش')
    discount = models.IntegerField(blank=True,null=True,default=0,verbose_name='تخفیف روی فاکتور')
    description = models.TextField(blank=True,null=True,verbose_name='توضیحات')
    payment_type = models.ForeignKey(PaymentType,default=None,on_delete=models.CASCADE,null=True,blank=True,verbose_name='نوع پرداخت',related_name='payment_types')

    def get_order_total_price(self):
        sum = 0
        for item in self.orders_details1.all():
            sum += item.price*item.qty
        delivery = 25000
        if sum > 500000 :
            delivery = 0
        tax = sum * 0.09

        return sum + delivery + tax

    def __str__(self):
        return f"{self.customer}\t{self.id}\t{self.is_finally}"

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
#___________________________________________________________________________________________________
class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orders_details1',verbose_name='سفارش')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='orders_details2',verbose_name='کالا')
    qty = models.PositiveIntegerField(default=1,verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت کالا')

    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}"


