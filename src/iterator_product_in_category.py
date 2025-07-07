from src.classes import Category

class CategoryProductIterator:
    def __init__(self, category_object: Category):
        self.category_object = category_object
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        product_list = self.category_object._Category__products

        if self.current_index >= len(product_list):
            raise StopIteration("Конец списка продуктов в данной категории")

        product = product_list[self.current_index]
        self.current_index += 1
        return product
