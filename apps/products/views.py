from lib2to3.fixes.fix_input import context
from django.shortcuts import render,get_object_or_404
from pyexpat import features
from .models import Product, ProductGroup, FeatureValue, Brand
from django.db.models import Q, Count,Min,Max
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator

def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
#___________________________________________________________________________________________________________
#ارزانترین محصولات
def get_cheapest_products(request,*args,**kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:5]
    product_groups = get_root_group()
    context = {'products':products,'product_groups':product_groups}
    return render(request, 'products_app/partials/cheapest_products.html', context)
#___________________________________________________________________________________________________________
#جدیدترین محصولات
def get_last_products(request,*args,**kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_groups = get_root_group()
    context = {'products':products,'product_groups':product_groups}
    return render(request, 'products_app/partials/last_products.html', context)
#___________________________________________________________________________________________________________
# گروه های محبوب
def get_popular_product_groups(request,*args,**kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_group')).order_by('-count')[:6]
    context = {'product_groups':product_groups}
    return render(request,'products_app/partials/popular_product_groups.html', context)
#___________________________________________________________________________________________________________
# جزییات محصول
class ProductDetailView(View):
    def get(self, request, slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,'products_app/product_detail.html',{'product':product})
#___________________________________________________________________________________________________________
# محصولات مرتبط
# def get_related_products(request,*args,**kwargs):
#     current_product = get_object_or_404(Product,slug=kwargs['slug'])
#     related_products=[]
#     for group in current_product.product_group.all():
#         related_products.extend(Product.objects.filter(Q(product_group=group) & ~Q(id=current_product.id)))
#         # related_products.extend(Product.objects.filter(Q(product_group=group)))
#     return render(request,'products_app/partials/related_products.html',{'related_products':related_products})

def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])

    # گرفتن همه محصولات مرتبط با گروه‌های مشترک و حذف محصول فعلی از نتایج
    related_products = Product.objects.filter(
        product_group__in=current_product.product_group.all(),
        is_active=True  # فقط محصولات فعال
    ).exclude(id=current_product.id).distinct()

    return render(request, 'products_app/partials/related_products.html', {
        'related_products': related_products
    })
#___________________________________________________________________________________________________________
# لیست کلیه گروههای محصولات
class ProductGroupsView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_group')).order_by('-count')
        return render(request,'products_app/product_groups.html/',{'product_groups':product_groups})
#___________________________________________________________________________________________________________
# لیست برندها برای فیلتر
def get_brands(request,*args,**kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id=product_group.products_of_group.filter(is_active=True).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id)\
                                .annotate(count=Count('products_of_brand'))\
                                .filter(~Q(count=0))\
                                .order_by('-count')
    return render(request,'products_app/partials/brands.html',{'brands':brands})

#___________________________________________________________________________________________________________
# لیست های دیگر فیلترها برحسب مقادیر ویژگی های کالاهای درون گروه
def get_features_for_filter(request,*args,**kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list=product_group.features_of_group.all()
    feature_dict=dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_values.all()
    return render(request,'products_app/partials/features_filter.html',{'feature_dict':feature_dict})

#___________________________________________________________________________________________________________
#لیست گروه محصولات برای فیلتر
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_group'))\
                    .filter(Q(is_active=True) & ~Q(count=0)).order_by('-count')
    return render(request,'products_app/partials/product_groups.html/',{'product_groups':product_groups})
#___________________________________________________________________________________________________________
# لیست محصولات هر گروه محصولات
class ProductsByGroupView(View):
    def get(self,request, *args, **kwargs):
        slug = kwargs['slug']
        current_group=get_object_or_404(ProductGroup,slug=slug)
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))

        res_aggregate=products.aggregate(min=Min('price'),max=Max('price'),)

        # price filter
        filter=ProductFilter(request.GET, queryset=products)
        products=filter.qs

        # brand filter
        brands_filter = request.GET.getlist('brands')
        if brands_filter:
            products=products.filter(brand__id__in=brands_filter)

        # features filter
        features_filter=request.GET.getlist('features')
        if features_filter:
            products=products.filter(product_feature__filter_value__id__in=features_filter).distinct()

        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type='0'

        if sort_type=='1':
            products=products.order_by('price')
        elif sort_type=='2':
            products=products.order_by('-price')

        group_slug=slug
        product_per_page=5
        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()

        # لیست اعداد برای ساخت منو بازشونده برای تعیین تعداد کالای هر صفحه توسط کاربر
        show_count_product=[]
        i=product_per_page
        while i<product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)

        context = {
            'products':products,
            'res_aggregate':res_aggregate,
            'filter':filter,
            'current_group':current_group,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'show_count_product':show_count_product,
            'sort_type' : sort_type,
        }
        return render(request,'products_app/products.html',context)

#___________________________________________________________________________________________________________
# two dropdown in adminpanel
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res,safe=False)