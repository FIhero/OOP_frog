class Product:
    def __init__(self, name, description, price, quantity):
        """Создаение атрибутов для данного класса"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Создаение атрибутов для данного класса"""
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(self.products)
