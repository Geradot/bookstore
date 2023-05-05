from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class BookCategory(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name
     
    
class Book(models.Model):
    category = models.ForeignKey(BookCategory, blank=True, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="customers")
    purchase_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Paid: {self.paid}. Purchase #{self.pk} worth ${self.total_price} by {self.user.username}'
    
    def save(self, *args, **kwargs):
        if self.paid and not self.purchase_date:
            self.purchase_date = timezone.now()
        super().save(*args, **kwargs)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchases')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="purchase_books")
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} × {self.book.title} in Purchase #{self.purchase.pk}'