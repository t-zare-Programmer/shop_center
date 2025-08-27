from apps.products.models import Product

#__________________________________________________________________________
class ShopCart(object):
    def __init__(self,request):
        self.session=request.session
        temp=self.session.get('shop_cart')
        if not temp:
            temp=self.session['shop_cart']={}
        self.shop_cart=temp
        self.count=len(self.shop_cart.keys())

# __________________________________________________________________________
    def save(self):
            self.session.modified = True
# __________________________________________________________________________

    def __iter__(self):
        list_id = self.shop_cart.keys()
        products = Product.objects.filter(id__in=list_id)
        temp = self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]["product"] = product

            if "final_price" not in temp[str(product.id)]:   # مقداردهی به final_price در صورت نبود
                temp[str(product.id)]["final_price"] = product.get_price_by_discount()

        for item in temp.values():
            item["total_price"] = int(item["final_price"]) * item["qty"]
            yield item
#__________________________________________________________________________
    def add_to_shop_cart(self,product,qty):
        product_id=str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id]={"qty":0,"price":product.price,"final_price":product.get_price_by_discount()}
        self.shop_cart[product_id]["qty"]+=int(qty)
        self.count=len(self.shop_cart.keys())
        self.save()

# __________________________________________________________________________
    def delete_from_shop_cart(self,product):
        product_id=str(product.id)
        del self.shop_cart[product_id]
        self.save()

# __________________________________________________________________________
    def update(self,product_id_list,qty_list):
        i=0
        for product_id in product_id_list:
            self.shop_cart[product_id]["qty"]=int(qty_list[i])
            i+=1
            self.save()
# __________________________________________________________________________
#     def calc_total_price(self):
#         sum=0
#         for item in self.shop_cart.values():
#             sum+=int(item["final_price"])*item["qty"]
#         return sum
    def calc_total_price(self):
        sum = 0
        for key, item in self.shop_cart.items():
            product = Product.objects.get(id=key)
            final_price = item.get("final_price", product.get_price_by_discount())
            sum += int(final_price) * item["qty"]
        return sum
#__________________________________________________________________________

