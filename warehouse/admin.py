from django.contrib import admin

from warehouse.models import WarehouseModel, ProductModel, MaterialModel, ProductMaterialModel


class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'material_id',
        'price',
        'remainder',
    )



class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'product_code',
        'product_name'
    )

class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'material_id',
        'material_name',

    )

class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'material_id',
        'quantity'
    )




admin.site.register(WarehouseModel, WarehouseAdmin)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(MaterialModel, MaterialAdmin)
admin.site.register(ProductMaterialModel, ProductMaterialAdmin)