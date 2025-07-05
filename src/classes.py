class Product:
    def __init__(self, name, description, price, quantity):
        """Создаение атрибутов для данного класса"""
        self.name = name
        self.description = description
        self.__price = 0.0
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Класс-метод для добавления нового продукта"""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif self.__price > new_price:
            approval = input("Вы уверены что хотите снизить цену?(y/n):").lower()
            if approval == "y":
                self.__price = new_price
                print(f"Цена снижена до {new_price} руб.")

            elif approval == "n":
                print("Снижение цены отменено")

            else:
                print(
                    "Неправильно введено значение(yes - y/n - no). Снижение цены отменено"
                )
        else:
            self.__price = new_price


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Создаение атрибутов для данного класса"""
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        """Добавление продукта в категорию"""
        for product_ in self.__products:
            if product_.name == product.name:
                product_.quantity += product.quantity
                product_.price = max(product_.price, product.price)
                return
        else:
            self.__products.append(product)
            Category.product_count += 1

    @property
    def products(self):
        """Геттер для атрибута __products. Возвращает строку со всеми продуктами"""
        all_products_info = []
        for product in self.__products:
            list_of_products = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
            all_products_info.append(list_of_products)
        return "".join(all_products_info)
