from typing import clear_overloads
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm
from .models import Coupon

@require_POST
def coupon_apply(request):
    now= timezone.now() 
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            #code_iexact -perform a case-insensitive exact match
            coupon = Coupon.objects.get(code_iexact=code, valid_from_lte=now, valid_to_gte=now,active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
