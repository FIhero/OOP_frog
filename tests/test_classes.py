import json

import pytest

from src.classes import Category, Product
from src.load_json_file import load_file_from_json


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


@pytest.mark.parametrize(
    "name, description, price, quantity",
    [
        ("Клубника", "красная ягода", 250.0, 240),
        ("Гороховый суп", "со вкусом гороха", 300.0, 0),
        ("", "", 0, 0),
    ],
)
def test_product(name, description, price, quantity):
    """Тестирует корректность инициализации объектов класса продуктов"""
    product = Product(name, description, price, quantity)
    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.quantity == quantity


@pytest.mark.parametrize(
    "name, description",
    [("Клубника", "красная ягода"), ("Гороховый суп", "со вкусом гороха"), ("", "")],
)
def test_category(name, description, product_category):
    """Тестирует корректность инициализации объектов класса категории"""
    product_list, category_list = product_category
    category = Category(name, description, product_list)
    assert category.name == name
    assert category.description == description
    assert category.products == product_list


def test_counts_product_category(product_category):
    """Тестирует количество продуктов и категорий"""
    product_list, category_list = product_category
    assert Category.category_count == len(category_list)
    assert Category.product_count == len(product_list)


@pytest.fixture
def mock_json_data():
    """
    Фикстура, предоставляющая тестовые данные JSON в виде строки.
    """
    return """
    [
      {
        "name": "Смартфоны",
        "description": "Смартфоны, для удобства жизни",
        "products": [
          {
            "name": "Samsung Galaxy S25 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5
          },
          {
            "name": "Iphone 16",
            "description": "512GB, Gray space",
            "price": 210000.0,
            "quantity": 8
          }
        ]
      },
      {
        "name": "Телевизоры",
        "description": "Современный телевизор, позволяет наслаждаться просмотром",
        "products": [
          {
            "name": "55\\\" QLED 4K",
            "description": "Фоновая подсветка",
            "price": 123000.0,
            "quantity": 7
          }
        ]
      }
    ]
    """


def test_load_file_from_json_success(mocker, mock_json_data):
    """
    Тестирует успешную загрузку данных из JSON-файла
    и корректность создания объектов Category и Product, а также счетчиков.
    """
    Category.category_count = 0
    Category.product_count = 0

    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_json_data))

    loaded_categories = load_file_from_json("dummy_path.json")

    assert len(loaded_categories) == 1

    assert Category.category_count == 1
    assert Category.product_count == 1 + 1

    category_smartphones = loaded_categories[0]
    assert category_smartphones.name == "Смартфоны"
    assert (
        category_smartphones.description
        == "Смартфоны, для удобства жизни"
    )
    assert len(category_smartphones.products) == 2

    samsung = category_smartphones.products[0]
    assert samsung.name == "Samsung Galaxy S25 Ultra"
    assert samsung.price == 180000.0
    assert samsung.quantity == 5

    category_tvs = loaded_categories[0]
    assert category_tvs.name == "Смартфоны"
    assert len(category_tvs.products) == 2

    qled_tv = category_tvs.products[0]
    assert qled_tv.name == "Samsung Galaxy S25 Ultra"
    assert qled_tv.price == 180000.0


def test_load_file_from_json_file_not_found(mocker):
    """Тестирует случай, когда JSON-файл не найден."""
    Category.category_count = 0
    Category.product_count = 0

    with pytest.raises(FileNotFoundError):
        load_file_from_json("non_existent_file.json")

    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_file_from_json_malformed_json(mocker):
    """Тестирует случай с некорректным JSON-файлом."""
    Category.category_count = 0
    Category.product_count = 0

    mocker.patch("builtins.open", mocker.mock_open(read_data='{"invalid json"'))

    with pytest.raises(json.JSONDecodeError):
        load_file_from_json("malformed.json")

    assert Category.category_count == 0
    assert Category.product_count == 0
