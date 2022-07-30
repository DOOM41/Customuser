from django import forms
from shop.models import Product, BasketItem


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["id"]


class SearchForm(forms.Form):
    my_search = forms.CharField(
        label='Поиск'
    )


class AddProductToBasketForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        exclude = [
            "id",
            "basket",
        ]


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        exclude = [
            "text",
        ]