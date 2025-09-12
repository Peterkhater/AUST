from django.db import models
from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = (
        ("fruits", "Fruits"),
        ("vegetables", "Vegetables"),
        ("grains", "Grains"),
        ("dairy", "Dairy"),
        ("meat", "Meat"),
        ("other", "Other"),
    )
    SHELF_LIFE = (
        ("day", "Day"),
        ("week", "Week"),
    )
    UNIT_CHOICES = (
        ("perKg", "Kg"),
        ("perUnit", "Unit"),
    )

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50,choices=UNIT_CHOICES,default="kg")

    min_order = models.PositiveIntegerField(default=0)

    harvest_date = models.DateField(auto_now=False, auto_now_add=False)

    #shelf Life
    shelf_life = models.PositiveIntegerField(default=0)
    shelf_life_type = models.CharField(max_length=50, choices=SHELF_LIFE, default="day")

    image1 = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True, null=True)

    is_available = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=True)
    is_Non_GMO = models.BooleanField(default=False)
    is_local_farm= models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.farmer.username}"

    def total_value(self):
        """Returns the total value of stock for this product."""
        return self.price * self.quantity
