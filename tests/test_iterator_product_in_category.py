from src.classes import Category, Product
from src.iterator_product_in_category import CategoryProductIterator
import pytest

@pytest.fixture
def product_category():
    """Фикстура для тестирования счетчиков категорий и продуктов"""

    Category.category_count = 0
    Category.product_count = 0

    product1 = Product(
        "Samsung Galaxy S25 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 16", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    products = [product1, product2, product3, product4]

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    categorys = [category1, category2]

    return products, categorys


def test_category_is_iterable(product_category):
    """Тестирует как итерирует класс CategoryProductIterator"""
    _, category = product_category
    c_one, _ = category
    assert hasattr(c_one, "__iter__")
    iterator_instance = iter(c_one)
    assert isinstance(iterator_instance, CategoryProductIterator)
    assert hasattr(iterator_instance, "__next__")

    second_iterator_call = iter(iterator_instance)
    assert isinstance(second_iterator_call, CategoryProductIterator)


def category_product_iterator_older_and_coantent(product_category):
    """Тестирует порядок и корректность итерации по продуктам в категории"""
    products, category = product_category
    c_one, _ = category

    actual_product_from_iterator = []
    for product in c_one:
        actual_product_from_iterator.append(product)

    assert actual_product_from_iterator == c_one
    assert len(actual_product_from_iterator) == len(c_one)

def test_stop_iteration(product_category):
    """Тестирует корректность вывода StopIteration"""
    _, category = product_category
    _, c_two = category

    iterator = iter(c_two)
    first_p = next(iterator)
    assert first_p == c_two._Category__products[0]
    with pytest.raises(StopIteration):
        next(iterator)


def test_empty_iteration():
    """Тестирует итерацию по пустой категории"""
    empty_iterator = Category("Пустота", "Как в моей голове", [])

    iterator = iter(empty_iterator)

    with pytest.raises(StopIteration):
        next(iterator)
