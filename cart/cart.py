# Файл в який записуємо всю основну логіку роботи для кошика
# Формат сесій, дані з кошика зберігаються в cookie (На телефоні збережене не буде видно, але як для практики варто попробувати)


# В views йдуть саме обробники які прив'язані до урл а в цьому файлі ми зробимо основну логіку яку потім імпортуємо
from django.conf import settings
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session # Ініціалізуємо сесії

        cart = self.session.get(settings.CART_SESSION_ID) # Отримуємо сесію користувача а саме корзину

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # Задаємо пусту корзину
        self.cart = cart # Якщо кошик є тоді ми призначаємо її вміст, а якщо немає то призначаємо що вона пуста (Локально призначаємо)

    def add(self, product, quantity=1, override_quantity=False): # скільки одиниць товару додати за замовчуванням 1, override_quantity=False значення більше 1. override_quantity — прапорець: False → додати до існуючої кількості True → повністю замінити кількіст
        product_id = str(product.id)
        if product_id not in self.cart: # Якщо товару немає в корзині
            self.cart[product_id] = {'quantity': 0 , 'price': str(product.price)} # То ми даємо cart к-сть 0 і ціну продукту. Товар створюється в корзині, але з кількістю 0 Це потрібно, щоб далі без помилок змінювати кількість

        if override_quantity: # Повністю перезаписуємо кількість. Користувач у формі ввів 10 → кількість стає рівно 10
            self.cart[product_id]['quantity'] = quantity # Міняємо кількість в корзині на 10
        else: #
            self.cart[product_id]['quantity'] += quantity # Додаємо до існуючої кількості. Додаємо +1 кожен раз як натиснули купити
        self.save() # Зберігаємо

    def save(self):
        self.session.modified = True # Сесії поміняли і їх зберігаємо


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id] # Якщо в корзині є продукт ід видаляємо і зберігаємо це
            self.save()


    def __iter__(self): # Проходиться по товарах в корзині і виводить їх параметри. for item in Сart
        product_ids = self.cart.keys() # Зберігаємо всі id які є в корзині. Отримуємо всі ID товарів з корзини
        products = Product.objects.filter(id__in=product_ids) # Беремо ці товари з бази даних. витягуються лише ті товари, які є в корзині
        cart = self.cart.copy() # Копія корзини/ не змінювати оригінальні дані в session. безпечно додавати нові поля (product, total_price)
        for product in products:
            cart[str(product.id)]['product'] = product # Привʼязка обʼєкта Product до корзини. в корзині був лише id a тепер є повноцінний Django-обʼєкт
        for item in cart.values(): # Фінальна обробка кожного товару. працюємо вже не з id, а з самим товаром.
            item['price'] = float(item['price']) # Перетворення ціни. ціна зберігалась як str (для session) a для розрахунків потрібне число
            item['total_price'] = item['price'] * item['quantity'] # Розрахунок загальної ціни для товарів ОДНОГО типу
            yield item # не повертає весь список одразу а віддає по одному товару за ітерацію

    def __len__(self): # Повертаємо кількість товарів в кошику
        return sum(item['quantity'] for item in self.cart.values()) # Сума кількості товарів які є в корзині

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values() ) # Сума цін помножених на кількість в cart value кошику

    def clear(self):
        del self.session[settings.CART_SESSION_ID] # ВИдаляємо куки повязані з нашою корзиною
        self.save()
