import redis
from django.conf import settings
from .models import Product_SubCategory, Products

r = redis.Redis(host=settings.REDIS_HOST,
                port = settings.REDIS_PORT,
                db = settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, id):
        return f'product:{id}:purchase_with'
    def products_brought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),1,with_id)
                
    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0],
                0,-1,desc=True)[:max_results]
            )
        else:
            flat_ids = ".join([str(id) for id in product_ids])"
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            
