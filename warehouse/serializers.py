from rest_framework import serializers

from warehouse.models import ProductModel, MaterialModel, ProductMaterialModel, WarehouseModel


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = [
            'material_name'
        ]


class ProductMaterialSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.SerializerMethodField('get_warehouse_id')
    material_name = serializers.CharField(source='material_id.material_name')
    qty = serializers.IntegerField(source='quantity')
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = ProductMaterialModel
        fields = ['warehouse_id', 'material_name', 'qty', 'price']

    # Get the warehouse_id based on the material
    @staticmethod
    def get_warehouse_id(obj):
        warehouse = WarehouseModel.objects.filter(material_id=obj.material_id).first()
        return warehouse.id if warehouse else None

    # Get the price based on the material
    @staticmethod
    def get_price(obj):
        warehouse = WarehouseModel.objects.filter(material_id=obj.material_id).first()
        return warehouse.price if warehouse else None


class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = WarehouseModel
        fields = [
            'material', 'remainder', 'price'
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, )
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
