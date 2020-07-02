from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from secrets import token_urlsafe

import uuid

# Create your models here.


class UnitType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={"pk": self.pk})

    def get_stock_quantity(self):
        stock_quantity = 0
        stock_entries = ProductStockEntry.objects.filter(product=self.pk)
        for stock_entry in stock_entries:
            stock_quantity += stock_entry.amount
        return stock_quantity

    def get_price(self):
        price_raw = float(self.unit_price * self.unit)
        return format(price_raw, '.2f')

    def get_delete_url(self):
        return reverse('product-delete', kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={"pk": self.pk})

    def get_make_order_ready_for_delivery_url(self):
        return reverse('make-order-ready-for-delivery', kwargs={"pk": self.pk})


class ProductStockEntry(models.Model):
    entry_date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()


class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Placed'),
        ('D', 'Delivered')
    )

    reference_number = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    date_placed = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="P")

    def get_checkout_url(self):
        return reverse('checkout', kwargs={"pk": self.pk})

    def get_order_items_queryset(self):
        order_items_queryset = OrderItem.objects.filter(order=self.pk)
        return order_items_queryset

    def get_make_order_ready_for_delivery_url(self):
        return reverse('make-order-ready-for-delivery', kwargs={"pk": self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        price = self.product.unit_price * self.product.unit
        return price*self.quantity

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={"pk": self.pk})

   


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('R', 'In route'),
        ('D', 'Delivered')
    )
    driver = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True)
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="P")

    def get_full_address(self):
        streetname = self.address.street
        number = self.address.number
        floor = self.address.floor
        direction = self.address.direction
        postal = self.address.postal
        city = self.address.city
        return f"{streetname} {number}, {floor}.{direction}. {postal}, {city}"
    

class Address(models.Model):
    DIRECTION_CHOICES = (
        ('TV', 'Til venstre'),
        ('MF', 'Midt for'),
        ('TH', 'Til højre'),
    )
    postal = models.CharField(max_length=4)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    floor = models.CharField(max_length=5, blank=True, null=True)
    direction = models.CharField(
        max_length=2, choices=DIRECTION_CHOICES, blank=True, null=True)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=43, default=token_urlsafe)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
