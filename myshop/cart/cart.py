from decimal import Decimal
from django.conf import settings
from shop.models import Products ,Product_SubCategory
from coupons.models import Coupon

class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)       
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self,product,weight=0.5,override_quantity=False):
        product_id = str(product.id)
        slug = product.slug
        if ((product_id + '=' + product.slug) not in self.cart ):
            self.cart[product_id + '=' + slug] = {'weight':0,'price':str(product.selling_price),'slug':product.slug} 

        if override_quantity:
            self.cart[product_id + '=' +slug]['weight'] = weight
        
        else:
            self.cart[product_id + '=' +slug]['weight'] += weight
        
        self.save()

    def save(self):
        self.session.modified = True


    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    
    def remove(self, product):
        product_id = str(product.id)
        slug = product.slug
        if((str(product_id) + '=' + slug) in self.cart):
            del self.cart[product_id + '=' + slug]
            self.save()

    def __iter__(self):
        products_ids =  self.cart.keys()
        products = []
        products_id = []
        products_slug = []
        
        for ids in products_ids:
            try:
                products_id.append((ids.split('=')[0]))
                products_slug.append(ids.split('=')[1])
            except:
                continue
                
        products_1 =  Product_SubCategory.objects.filter(id__in = products_id,slug__in = products_slug) 
        products_2 = Products.objects.filter(id__in = products_id,slug__in = products_slug)
        
        for pro in products_1:
            # if(pro.slug in products_slug):
            products.append(pro)

        for pro in products_2:
            # if(pro.slug in products_slug):
            products.append(pro)

        cart = self.cart.copy()

        for product in products:
            try:
                cart[str(product.id)+'='+ (product.slug)]['product'] = product
            except:
                continue
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['weight']
            yield item

    def __len__(self):
        return sum(item['weight'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price'])*item['weight'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()