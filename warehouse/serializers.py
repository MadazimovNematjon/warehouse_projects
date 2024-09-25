from rest_framework import serializers

from warehouse.models import ProductModel, MaterialModel, ProductMaterialModel, WarehouseModel


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = [
            'material_name', 'material_id', 'created_at', 'updated_at'
        ]


class ProductMaterialSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.SerializerMethodField('get_warehouse_id')
    material_name = serializers.CharField(source='material_id.material_name')
    qty = serializers.IntegerField(source='quantity')
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = ProductMaterialModel
        fields = [
            'product_id',
            'material_id',
            'quantity',
            'warehouse_id',
            'material_name',
            'qty',
            'price',
            'created_at',
            'updated_at',
        ]

        extra_kwargs = {
            'warehouse_id': {'required': False, 'read_only': True},
            'material_name': {'required': False, 'read_only': True},
            'price': {'required': False, 'read_only': True},
        }

    # Get the warehouse_id based on the material

    def get_warehouse_id(self, obj):
        return self.get_warehouse_data(obj)[0]

    # Get the price based on the material

    def get_price(self, obj):
        return self.get_warehouse_data(obj)[1]

    @staticmethod
    def get_warehouse_data(obj):
        quantity_needed = obj.quantity
        warehouses = WarehouseModel.objects.filter(material_id=obj.material_id).order_by('id')
        total_reserved = 0

        for warehouse in warehouses:
            remaining = warehouse.remainder - total_reserved

            if remaining > 0:
                if quantity_needed <= remaining:
                    return warehouse.id, warehouse.price
                else:
                    quantity_needed -= remaining
                    total_reserved += remaining
            else:
                total_reserved += warehouse.remainder
        return None, None


class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True, source='material_id')

    class Meta:
        model = WarehouseModel
        fields = [
            'id', 'material_id', 'remainder', 'price', 'material', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'material': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, )
    product_qty = serializers.SerializerMethodField('get_product_qty')

    class Meta:
        model = ProductModel
        fields = [
            'product_name',
            'product_qty',
            'product_materials',
            'created_at',
            'updated_at'
        ]

    @staticmethod
    def get_product_qty(obj):
        return obj.product_materials.count()
