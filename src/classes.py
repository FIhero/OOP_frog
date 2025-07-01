import json


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


def load_file_from_json(filepath):
    """Загрузка категорий из JSON-файла"""
    with open(filepath) as f:
        data = json.load(f)

        all_category_object = []

        for category_data in data:
            products_in_this_category = []

            category_name = category_data["name"]
            category_description = category_data["description"]
            for products_data in category_data["products"]:
                products_name = products_data["name"]
                products_description = products_data["description"]
                product_price = products_data["price"]
                product_quantity = products_data["quantity"]

                product_object = Product(
                    products_name, products_description, product_price, product_quantity
                )
                products_in_this_category.append(product_object)

            category_object = Category(
                category_name, category_description, products_in_this_category
            )
            all_category_object.append(category_object)

            return all_category_object
