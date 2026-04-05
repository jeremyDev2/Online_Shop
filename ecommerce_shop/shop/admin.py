from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    #specify fields where the value is automatically set using the value of other fields.
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    #set the fields that can be edited from the list display page of the administration site.
    list_editable  =['price', 'available']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
