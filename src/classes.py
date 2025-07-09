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

    def __str__(self):
        """Строка информации продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"

    def __add__(self, other):
        """Считает общую цену на складе"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        if type(self) is not type(other):
            raise TypeError("Можно складывать товары только одного и того же класса")

        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        """Строка информации"""
        info = super().__str__()
        return (
            f"{info}{self.description}\nМодель: {self.model}\nЯдро: {self.efficiency}"
            f"\nОбъем памяти: {self.memory} GB\nЦвет: {self.color}\n"
        )


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        """Строка информации"""
        info = super().__str__()
        return (
            f"{info}{self.description}\nСтрана производитель: {self.country}"
            f"\nСрок службы: {self.germination_period} год\nЦвет: {self.color}\n"
        )


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
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

        if product.quantity < 1:
            raise ValueError(
                "Товар с нулевым или отрицательным количеством не может быть добавлен"
            )

        for product_ in self.__products:
            if product_.name == product.name:
                product_.quantity += product.quantity
                product_.price = max(product_.price, product.price)
                return
        else:
            self.__products.append(product)
            Category.product_count += 1

    def __str__(self):
        """Строка информации категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_total_stock_value(self):
        if not self.__products:
            return 0
        current_total = 0
        for i in range(0, len(self.__products)):
            current_total += self.__products[i].price * self.__products[i].quantity
        return current_total

    def __iter__(self):
        """Метод делает объекст Category итерируемым для CategoryProductIterator"""
        from src.iterator_product_in_category import CategoryProductIterator

        return CategoryProductIterator(self)
