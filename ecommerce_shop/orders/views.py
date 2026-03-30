from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from cart.cart import Cart
from django.shortcuts import redirect, render, get_object_or_404
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
import weasyprint

def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order: OrderCreateForm = form.save()
            if card.coupon:
                order.coupon = cart.coupon
                ordfer.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            order_created.delay(order.id)
            #set the order in the session
            request.session['order_id'] = order.id
            #redirect for payment
            return redirect('payment:process')
        else:
            form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})

@staff_member_required
#get the Order object with the given ID and render a template to display the order.
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})

#only staff users can access this view
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename-order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])
    return response
