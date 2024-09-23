import uuid
from dataclasses import field

from django.db import models
from django.db.models import UniqueConstraint

from shared.models import BaseModel


class ProductModel(BaseModel):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=6, unique=True)

    class Meta:

        constraints = [
            UniqueConstraint(
                fields=['product_code'], name='unique_product_code'
            )
        ]

    def __str__(self):
        return self.product_name


class MaterialModel(BaseModel):
    material_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_name = models.CharField(max_length=255)

    def __str__(self):
        return self.material_name


class ProductMaterialModel(BaseModel):
    product_id = models.ForeignKey(ProductModel, related_name='product_materials', on_delete=models.CASCADE)
    material_id = models.ForeignKey(MaterialModel, related_name='materials_product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.material_id.material_name} for {self.product_id.product_name}"


class WarehouseModel(BaseModel):
    material_id  = models.ForeignKey(to=MaterialModel, related_name='warehouses', on_delete=models.CASCADE)
    remainder = models.PositiveIntegerField()  # Omborda qolgan miqdor
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.remainder} left of {self.material_id.material_name} at {self.price} per unit"
