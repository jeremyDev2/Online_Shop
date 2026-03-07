from .cart import Cart

# add dict with context, to global access
def cart(request):
    return {'cart':Cart(request)}
