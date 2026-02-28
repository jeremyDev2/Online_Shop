from  django import forms

#[(1, "1"), (2, "2"), ..., (20, "20")]
PRODUCT_QUANTITY_CHOISES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOISES,coerce=int) #coerce - convert to int
    #False - new quantity added to existing one, True - existing quantity overrided with the given one
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
