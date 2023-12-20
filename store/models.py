from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="media/category_icons/", null=True, blank=True)
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/product_images/", null=True, blank=True)
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"
        
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey("Client", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(6)])
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

class Client(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"

class Order(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    preferred_delivery_time = models.DateTimeField()
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}, {self.price} грн."

class Table(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()
    shape = models.CharField(
        max_length=10, choices=[("rectangle", "Прямокутний"), ("rectangle2", "Прямокутний"), ("oval", "Овальний")]
    )
    horizontal_coordinate = models.FloatField()
    vertical_coordinate = models.FloatField()
    width_percentage = models.FloatField()
    length_percentage = models.FloatField()
    
    class Meta:
        verbose_name = "Місця"
        verbose_name_plural = "Місця"

class Reservation(models.Model):
    date = models.DateField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    
    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

class ReservedTable(models.Model):
    reservation = models.ForeignKey(
        Reservation, related_name="reserved_tables", on_delete=models.CASCADE
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE)