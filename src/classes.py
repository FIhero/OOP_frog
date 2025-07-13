from abc import ABC, abstractmethod


class BaseProduct(ABC):
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = 0.0
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass


class CreationLogMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Создан объект класса: {self.__class__.__name__}")
        print(f"Параметры: Позиционные: {args}, Именованные: {kwargs}\n")


class Product(CreationLogMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        """Создание атрибутов для данного класса"""
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        super().__init__(name, description, price, quantity)

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
        return self._price

    @price.setter
    def price(self, new_price):
        """Функция изменения цены"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif self._price > new_price:
            approval = input("Вы уверены что хотите снизить цену?(y/n):").lower()
            if approval == "y":
                self._price = new_price
                print(f"Цена снижена до {new_price} руб.")

            elif approval == "n":
                print("Снижение цены отменено")

            else:
                print(
                    "Неправильно введено значение(yes - y/n - no). Снижение цены отменено"
                )
        else:
            self._price = new_price

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


class BaseShopEntity(ABC):
    @abstractmethod
    def __str__(self):
        pass


class ZeroQuantityError(ValueError):
    def __init__(
        self,
        message="Товар с нулевым или отрицательным количеством не может быть добавленным",
    ):
        self.message = message
        super().__init__(self.message)


class Category(BaseShopEntity):
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Создание атрибутов для данного класса"""
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        """Добавление продукта в категорию"""
        print("Начинаем обработку добавления товара")
        try:
            if not isinstance(product, Product):
                raise TypeError(
                    "Можно добавлять только объекты класса Product или его наследников"
                )

            if not isinstance(product.quantity, int) or product.quantity <= 0:
                raise ZeroQuantityError(
                    "Товар с нулевым или отрицательным количеством не может быть добавленным"
                )

            for product_ in self.__products:
                if product_.name == product.name:
                    product_.quantity += product.quantity
                    product_.price = max(product_.price, product.price)
                    print(f"Товар {product_.name} успешно обновлен")
                    return
            else:
                self.__products.append(product)
                Category.product_count += 1
                print(f"Товар {product.name} успешно добавлен")

        except ZeroQuantityError as e:
            print(f"Ошибка добавления товара: {e.message}")
            raise e

        except TypeError as e:
            print(f"Ошибка добавления товара: {e}")
            raise e

        except Exception as e:
            print(f"Произошла непредвиденная ошибка при добавления товара: {e}")
            raise e

        else:
            pass

        finally:
            print("Обработка добавления товара завершена")

    def __str__(self):
        """Строка информации категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_total_stock_value(self):
        """Считает стоимость всех товаров на складе"""
        if not self.__products:
            return 0
        current_total = 0
        for i in range(0, len(self.__products)):
            current_total += self.__products[i].price * self.__products[i].quantity
        return current_total

    def __iter__(self):
        """Метод делает объект Category итерируемым для CategoryProductIterator"""
        from src.iterator_product_in_category import CategoryProductIterator

        return CategoryProductIterator(self)

    def average_price_of_goods(self):
        """Считает среднюю цену товара"""
        try:
            total_sum = self.get_total_stock_value() / sum(
                product.quantity for product in self.__products
            )
            return round(total_sum, 2)
        except ZeroDivisionError:
            return 0


class Order(BaseShopEntity):
    def __init__(self, product, quantity):
        print("Начало обработки заказа")
        try:
            if not isinstance(product, Product):
                raise TypeError("Заказ должен содержать только объекты Product")

            if not isinstance(quantity, int) or quantity <= 0:
                raise ZeroQuantityError(
                    "Количество товара в заказе должно быть положительным целым числом"
                )

            self.product = product
            self.quantity = quantity
            self.total_cost = product.price * quantity

        except ZeroQuantityError as e:
            print(f"Ошибка создания заказа: {e.message}")
            self.quantity = 0
            self.total_cost = 0
            raise e

        except TypeError as e:
            print(f"Ошибка создания заказа: {e}")
            self.quantity = 0
            self.total_cost = 0
            raise e

        except Exception as e:
            print(f"Произошла непредвиденная ошибка при создания заказа: {e}")
            self.quantity = 0
            self.total_cost = 0
            raise e

        else:
            print("Заказ успешно создан")

        finally:
            print("Обработка создания заказа завершена")

    def __str__(self):
        """Строка информации о заказе"""
        return (
            f"Заказ: {self.product.name}",
            f"Количество: {self.quantity} шт.",
            f"Итого: {self.total_cost} руб.",
        )
