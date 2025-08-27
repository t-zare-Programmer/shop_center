from datetime import datetime
from django.db import models
from django.db import models
from email.mime import image
from utils import FileUpload
from django.utils import timezone
# from ckeditor_uploader.fields import RichTextUploadingField
# from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField
# from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db.models import Sum,Avg
#____________________________________________________________________________________
class Brand(models.Model):
    brand_title = models.CharField(max_length=100,verbose_name="نام برند")
    file_upload=FileUpload('images','brand')
    image_name = models.ImageField(upload_to= file_upload.upload_to , verbose_name='تصویر برند کالا')
    slug = models.SlugField(max_length=200,null=True)

    def __str__(self):
        return self.brand_title

    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'
#____________________________________________________________________________________

class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100,verbose_name='عنوان گروه کالا')
    file_upload = FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    description = models.TextField(blank=True,null=True,verbose_name='توضیحات گروه کالا')
    is_active = models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال/غیرفعال')
    group_parent = models.ForeignKey('ProductGroup',on_delete=models.CASCADE,verbose_name='والد گروه کالا',related_name='groups',null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروزرسانی')
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.group_title

    class Meta:
        verbose_name='گروه کالا'
        verbose_name_plural='گروه های کالا'
 #___________________________________________________________________________________
class Feature(models.Model):
     feature_name = models.CharField(max_length=100,verbose_name='نام ویژگی')
     product_group = models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_group')

     def __str__(self):
         return self.feature_name

     class Meta:
         verbose_name = 'ویژگی'
         verbose_name_plural = 'ویژگی ها'
#____________________________________________________________________________________

class Product(models.Model):
    product_name = models.CharField(max_length=500,verbose_name='نام کالا')
    summery_description = models.TextField(blank=True,default='',null=True)
    description = RichTextUploadingField(blank=True,config_name='special',null=True)
    file_upload = FileUpload('images', 'product')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price = models.PositiveIntegerField(default=0,verbose_name='قیمت کالا')
    product_group = models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_group')
    brand = models.ForeignKey(Brand,verbose_name='برند کالا',on_delete=models.CASCADE,null=True,related_name='products_of_brand')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال/غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروزرسانی')
    features = models.ManyToManyField(Feature,through='ProductFeature')
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})

    #قیمت با تخفیف کالا
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details2.all():
            if(dbd.discount_basket.is_active==True and
                dbd.discount_basket.start_date <= datetime.now() and
                datetime.now() <= dbd.discount_basket.end_date) :
                list1.append(dbd.discount_basket.discount)
        discount=0
        if(len(list1)>0):
            discount=max(list1)
        return self.price-(self.price*discount/100)

    #تعداد موجودی کالا در انبار
    def get_number_in_warehouse(self):
        sum1 = self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        sum2 = self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))
        input = 0
        if sum1['qty__sum']!=None:
            input=sum1['qty__sum']
        output=0
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
        return input-output


    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'

#____________________________________________________________________________________
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100,verbose_name='عنوان مقدار')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,blank=True,null=True,related_name='feature_values',verbose_name='ویژگی')

    def __str__(self):
        return f"{self.id} {self.value_title}"

    class Meta:
        verbose_name='مقدار ویژگی'
        verbose_name_plural='مقدار ویژگی ها'
#____________________________________________________________________________________

class ProductFeature(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_features')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    value = models.CharField(max_length=100,verbose_name='مقدار ویژگی کالا')
    filter_value = models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار ویژگی برای فیلتر')

    def __str__(self):
        return f"{self.product} - {self.feature} : {self.value}"

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
#____________________________________________________________________________________
class ProductGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='gallery_images')
    file_upload = FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


