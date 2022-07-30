from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView
from django.contrib.auth.decorators import login_required


from shop.forms import SearchForm, AddProductToBasketForm, AddCommentForm
from shop.models import BasketItem, Basket, Product, Comments


class ProductsView(ListView):
    template_name = "products.html"
    model = Product
    context_object_name = "products"


class ProductDetail(DetailView):
    template_name = "product.html"
    model = Product
    slug_url_kwarg: str = "pk"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(
            product=self.get_object()
        )
        return context


class SearchView(View):
    template_name = "search.html"

    def get(self,  request):
        form = SearchForm()
        return render(
            request,
            self.template_name,
            {
                'form': form,
            }
        )

    def post(self,  request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_data = form.cleaned_data.get('my_search')
            products = Product.objects.all()
            result = []
            for product in products:
                if search_data in product.title:
                    result.append(product)
        return render(
            request,
            self.template_name,
            context={
                "products": result,
                'form': form,
            }
        )


class AddProductToBasket(FormView):
    template_name = 'core/add_product_to_basket.html'
    form_class = AddProductToBasketForm
    success_url = reverse_lazy("so")

    def form_valid(self, form):
        form.cleaned_data["basket"] = Basket.objects.get(
            user=self.request.user)
        BasketItem.objects.create(**form.cleaned_data)
        return super().form_valid(form)


class ProductInBasketList(ListView):
    model = BasketItem
    template_name = "basket.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(basket=self.request.user.basket)


@login_required(login_url=reverse_lazy("login"))
def add_to_basket(request):
    user = request.user
    basket = user.basket
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    try:
        my_product = BasketItem.objects.get(product=product)
        my_product.quantity += 1
        my_product.save()

    except:
        BasketItem.objects.create(
            basket=basket,
            product=product,
        )

    finally:
        return JsonResponse(data={
            "count": basket.items.count()
        })


@login_required(login_url=reverse_lazy("login"))
def buy_from_basket(request):
    user = request.user
    basket = user.basket
    BasketItem.objects.filter(basket=basket).delete()
    return JsonResponse(data={
        "count": basket.items.count()
    })


def add_comment(request):
    user = request.user
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    text = request.POST.get("comment")
    if text!="":
        Comments.objects.create(
            user=user,
            product=product,
            text=text
        )
    return redirect(reverse("products"))
