from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price")

class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("purchase", "book", "quantity", "subtotal")

admin.site.register(BookCategory)
admin.site.register(Book, BookAdmin)
admin.site.register(Purchase)
admin.site.register(PurchaseItem, PurchaseItemAdmin)