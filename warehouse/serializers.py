from rest_framework import serializers

from warehouse.models import ProductModel, MaterialModel, ProductMaterialModel, WarehouseModel




class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = [
            'material_name'
        ]


class ProductMaterialSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(source='warehouse.warehouse_id', default=None)
    material_name = serializers.CharField(source='material_id.material_name')
    qty = serializers.IntegerField(source='quantity')
    price = serializers.FloatField(source='material_id.price', default=None)

    class Meta:
        model = ProductMaterialModel
        fields = ['warehouse_id', 'material_name', 'qty', 'price']




class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = WarehouseModel
        fields = [
            'material', 'remainder', 'price'
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True,)
    product_qty = serializers.SerializerMethodField('get_product_qty')

    class Meta:
        model = ProductModel
        fields = [
            'product_name',
            'product_qty',
            'product_materials'
        ]

    @staticmethod
    def get_product_qty(obj):
        return obj.product_materials.count()
