import redis
from django.conf import settings
from .models import Product

redis_var = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

class Recommender:
    def product_key(self, id):
        return f"product:{id}:purchased_with"

    def product_bought(self, products):
        product_ids=[getattr(p, "id") for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    redis_var.zincrby(self.product_key(product_id), 1, with_id)

    def suggest_the_product(self, product, max_result=6):
        if hasattr(product, "id"):
            products= [product]
        else:
            products = list(product)
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = redis_var.zrange(
                self.product_key(product_ids[0]),0, max_result - 1, desc=True
            )
        else:
            # generate a temporary key
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys= [self.product_key(id) for id in product_ids]
            redis_var.zunionstore(tmp_key, keys)

            # remove ids for the products the recommendation is for
            redis_var.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions =redis_var.zrange(tmp_key,0, max_result - 1,desc=True)
            # remove the temp. key
            redis_var.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    #clear recomendation
    def clear_purchases(self):
        for id in Product.objects.values_list(id, flat=True):
            redis_var.delete(self.product_key(id))
