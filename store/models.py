from django.db import models

MEMBERSHIP_CHOICES = [
    ("S", "Silver"),
    ("B", "Bronze"),
    ("G", "Gold")
]

# MACROS ORDER PAYMENT
ORDER_STATUS_PENDING = "P"
ORDER_STATUS_COMPLETE = "C"
ORDER_STATUS_FAILED = "F"

ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING, "Pending"),
    (ORDER_STATUS_FAILED, "Failed"),
    (ORDER_STATUS_COMPLETE, "Complete")
]


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',
                                         on_delete=models.SET_NULL,
                                         null=True, related_name="+")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['title']


class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(null=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name="products")


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=2, choices=MEMBERSHIP_CHOICES, default="B")

    # class Meta:
    #     db_table = 'store_customer'
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name'])
    #     ]


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, null=False, default="P", choices=ORDER_STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255, null=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
