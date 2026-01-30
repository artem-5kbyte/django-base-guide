from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None): # По category slug прередаючи параметр можна фільтрувати
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug) # Якщо є слаг, з бази даних категорію по категорі слаг
        products = products.filter(category=category) # Вибираємо всі продукти по категорії

    return render(request, 'main/product/list.html', {'categories': categories, 'products': products, 'category': category})
    # Рендеримо, реквест за замовчуванням, далі шлях до шаблону, і контекст, дані які ми передаємо в шаблон

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4] # "Схожі", вибираємо продукти з тієї ж  категорії, окрім того що вже є по ід, і виводимо тільки 4 товара

    return render(request, 'main/product/detail.html', {'product': product, 'related_products': related_products})