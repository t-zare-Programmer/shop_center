# from lib2to3.pgen2.tokenize import group
from tokenize import group

from django.contrib import admin
from .models import Brand, Product, ProductGroup, ProductFeature, Feature, ProductGallery, FeatureValue
from  django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
#______________________________________________________________________________
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title','slug',)
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)
#______________________________________________________________________________
def de_active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد گروه {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)
#==========================================
def active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request, message)
#==========================================
def export_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json', queryset,stream=response)
    return response
#==========================================
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 1
#______________________________________________________________________________
class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'
    parameter_name = 'group'
    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id,item.group_title) for item in groups]

    # ==========================================
    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
#______________________________________________________________________________
#
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group','count_product_of_group')
    list_filter = (GroupFilter,'is_active',)
    search_fields = ('group_title',)
    ordering = ('group_title','group_parent',)
    inlines = [ProductGroupInstanceInlineAdmin,]
    actions = [de_active_product_group, active_product_group, export_json]
    list_editable = ('is_active',)
    #==========================================
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group = Count ('groups'))
        qs = qs.annotate(product_of_group=Count('products_of_group'))
        return qs
    #==========================================
    def count_sub_group(self, obj):
        return obj.sub_group

    # ==========================================
    @short_description('تعداد گروه های کالا')
    @order_field('products_of_group')
    def count_product_of_group(self, obj):
        return obj.product_of_group

    # ==========================================
    count_sub_group.short_description = 'تعداد زیر گروه ها'
    de_active_product_group.short_description = 'غیر فعال کردن گروه های انتخاب شده'
    active_product_group.short_description = 'فعال کردن گروه های انتخاب شده'
    export_json.short_description = 'خروجی json از گروه های انتخاب شده'
#_________________________________________________________________________________________________
def de_active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

#==========================================
def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)
#==========================================
class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 3

    class Media:
        css = {'all':('css/admin_style.css',)}
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',  # ✅ آدرس jQuery CDN
            'js/admin_script.js',
        )
#==========================================
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3
#==========================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','display_product_groups','price','brand','is_active','update_date','slug',)
    list_filter = (('brand__brand_title',DropdownFilter),('product_group__group_title',DropdownFilter),('is_active',DropdownFilter))
    search_fields = ('product_name',)
    ordering = ('update_date','product_name',)
    actions = [de_active_product, active_product,]
    inlines = [ProductFeatureInline,ProductGalleryInline]
    list_editable = ('is_active',)

    de_active_product.short_description = 'غیر فعال کردن کالا های انتخاب شده'
    active_product.short_description = 'فعال کردن کالا های انتخاب شده'

    # ==========================================
    def display_product_groups(self, obj):
       return ' , '.join([group.group_title for group in obj.product_group.all()])

    display_product_groups.short_description = 'گروه های کالا'

    # ==========================================
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_group":
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # ==========================================
    fieldsets = (
        ('اطلاعات محصول',{'fields':(
            'product_name',
            'image_name',
            ('product_group','brand','is_active'),
            'price',
            'description',
            'slug'
        )}),
        ('تاریخ و زمان',{'fields':(
            'published_date',
        )}),
    )
#_________________________________________________________________________________________________
class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','display_groups','display_feature_values')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_groups":
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def display_groups(self, obj):
        return ','.join([group.group_title for group in obj.product_group.all()])

    def display_feature_values(self, obj):
        return ','.join([feature_value.value_title for feature_value in obj.feature_values.all()])

    display_groups.short_description='گروه های داراری این ویژگی'
    display_feature_values.short_description='مقادیر ممکن برای این ویژگی'