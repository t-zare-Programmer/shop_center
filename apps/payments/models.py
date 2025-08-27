from django.db import models
from django.utils import timezone
from apps.accounts.models import Customer
from apps.orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_order',verbose_name='سفارش')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payment_customer',verbose_name='مشتری')
    register_date = models.DateTimeField(default=timezone.now,verbose_name='تاریخ پرداخت')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش پرداخت')
    amount = models.IntegerField(verbose_name='مبلغ پرداخت')
    description = models.TextField(verbose_name='توضیحات پرداخت')
    is_finally = models.BooleanField(default=False,verbose_name='وضعیت پرداخت')

    status_code = models.IntegerField(verbose_name='کد وضعیت درگاه پرداخت',null=True,blank=True)
    ref_id = models.CharField(max_length=50,verbose_name='شماره پیگیری پرداخت',null=True,blank=True)

    def __str__(self):
        return f"{self.order} {self.customer} {self.ref_id}"

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'