from django.contrib import admin

from . models import Product, ProductStockEntry, UnitType, ProductStockEntry, Delivery


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_type', 'unit_price',
                    'unit', 'get_price', 'get_stock_quantity')


admin.site.register(Product, ProductAdmin)

admin.site.register(Delivery)
admin.site.register(UnitType)
admin.site.register(ProductStockEntry)
