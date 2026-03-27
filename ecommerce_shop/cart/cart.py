from decimal import Decimal
from typing import TypedDict
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest
from shop.models import Product
from coupons.models import Coupon

class CartItem(TypedDict):
    product:Product
    price:Decimal
    quantity:int
    total_price: Decimal


class Cart(object):
    def __init__(self, request:HttpRequest) -> None:
        self.session:SessionBase = request.session
        cart= self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart= cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity: int, override_quantity: bool) -> None:
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self) -> None:
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product) -> None:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        # iterate over the items in the cart and get product from DB

        product_list = self.cart.keys()
        # get product obj. and add them to the cart
        products = Product.objects.filter(id__in=product_list)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        """
        cart = {
                "12": {"quantity": 2, "price": "9.99", "product": <Product id=12>},
                "15": {"quantity": 1, "price": "19.99", "product": <Product id=15>},
            }
        """
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(
            (Decimal(item["price"]) * item["quantity"] for item in self.cart.values()),
            Decimal(0),
        )

    def clear(self) -> None:
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
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
            return(self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
