
from django.db import models


class Address(models.Model):
    uid = models.ForeignKey('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.IntegerField()


# Create your models here.


class User(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.name} ({self.role})"


class Contact(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=15)  # ✅ changed
    email = models.EmailField()
    sub = models.CharField(max_length=50)
    msg = models.TextField()  # ✅ better than CharField(50)


class Add_to_cart(models.Model):
    uid = models.ForeignKey('User', on_delete=models.CASCADE)
    pid = models.ForeignKey('myapp2.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    qty = models.IntegerField()
    img = models.ImageField(upload_to='pictures/')
    total_price = models.IntegerField()


class Wishlist(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey('myapp2.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    img = models.ImageField(upload_to='pictures/')
    price = models.IntegerField()


class Order(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    sub_total = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    payment_id = models.CharField(max_length=150, blank=True)
    payment_order_id = models.CharField(max_length=150, blank=True)

    status = models.CharField(max_length=20, default='paid')
    items_json = models.JSONField(default=list)

    def __str__(self):
        return f"Order #{self.id}"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Newsletter Subscriptions"
