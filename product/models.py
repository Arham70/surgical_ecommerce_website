
from django.db import models
from authentication.models import CustomUser

class Size(models.Model):
    name = models.CharField(max_length=10)


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class CartItem(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
