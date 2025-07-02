import json
from src.classes import Product, Category

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