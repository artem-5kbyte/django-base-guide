from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True) # Створити індекс для поля. Те що часто викорстовується для фільтрації
    slug = models.SlugField(max_length=100, unique=True)

    class Meta: # Параметри з якими працюватиме база даних і адмінка
        ordering = ('name',) # Сортування по імені

        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self): # Метод, який визначає як відображатиметься обєкт в адмінці
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=(self.slug,))

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # Зовнішній ключ. Параметр має всі ті можливості що і модкль категорії вище
    # релатед наме те як ми хлчемо це бачити в адмінці, при видаленні КАСКАДЕ тобто Якзо видалити категорію видаляться продукти які привязані до неї
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) # Загружаємо в папку рік місяць день, бланк тру каже що це поле може бути пустим
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Число з плавачую точкою? заукруглення до 2 точок після коми
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) # Автоматична дата створення
    updated = models.DateTimeField(auto_now=True) # Автоматична дата оновлення

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_detail", args=(self.id, self.slug,))