from django.contrib import admin

# Register your models here.
from marketplace.models import Cart, Tax


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')



admin.site.register(Cart, CartAdmin)
admin.site.register(Tax)
