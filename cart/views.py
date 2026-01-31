from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST # Декоратор який дозволяє використовувати функцію тільки з методом РОST
def cart_add(request, product_id):
    cart = Cart(request) # Ініціалізужмо обєкт
    product = get_object_or_404(Product, id=product_id) # Беремо товар з вказаним продукт ід
    form = CartAddProductForm(request.POST) # Підключаємо форму

    if form.is_valid(): # Якщо форма валідна
        cd = form.cleaned_data # Беремо з неї чисту інформацію
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override']) # Додаємо в раніше ініціалізований обєкт свтореним нами методом add cart.py дані необхідня для додавання в корзину
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)  # Ініціалізужмо обєкт
    product = get_object_or_404(Product, id=product_id)  # Беремо товар з вказаним продукт ід
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True}) # Форма оновлення кількості товарів. Спочатку ініціалізуємо ту ксть яка вже є і додаємо оверріде

    return render(request, 'cart/cart_detail.html', {'cart': cart})
