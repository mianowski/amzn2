from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price_in_dollars = models.DecimalField(
        decimal_places=2,
        max_digits=6)
    barcode = models.CharField(
        max_length=13,
        help_text="Product Barcode (ISBN, UPC ...)"
    )
    description = models.TextField(help_text="Enter Product Description")

    def __str__(self):
        return "%s %s" % (self.barcode, self.name)


class Order(models.Model):

    items = models.ManyToManyField(Product, through='OrderItem')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.ordered_date)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
