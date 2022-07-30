from django.contrib import admin
from shop.models import Product, Comments

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
