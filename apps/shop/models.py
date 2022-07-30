from django.db import models
from auths.models import CustomUser

# Create your models here.


class Product(models.Model):
    title = models.CharField(verbose_name="Название", max_length=255)
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="media/products",
        null=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Содержимое")
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Basket(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE
    )


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
