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


@pytest.fixture
def product_data_for_new_product():
    """Фикстура для тестирования new_product"""
    product_data = {
        "name": "Samsung Galaxy S25 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    return product_data


@pytest.mark.parametrize(
    "name, description, price, quantity",
    [
        ("Клубника", "красная ягода", 250.0, 240),
        ("Гороховый суп", "со вкусом гороха", 300.0, 2),
        ("", "", 0, 0),
    ],
)
def test_product(name, description, price, quantity):
    """Тестирует корректность инициализации объектов класса продуктов"""
    product = Product(name, description, price, quantity)
    assert product.name == name
    assert product.description == description
    assert product._Product__price == price
    assert product.quantity == quantity


@pytest.mark.parametrize(
    "name, description",
    [("Клубника", "красная ягода"), ("Гороховый суп", "со вкусом гороха"), ("", "")],
)
def test_category_initialization(name, description, product_category):
    """Тестирует корректность инициализации объектов класса категории"""
    product_list, category_list = product_category
    category = Category(name, description, product_list)
    assert category.name == name
    assert category.description == description


def test_counts_product_category(product_category):
    """Тестирует количество продуктов и категорий"""
    product_list, category_list = product_category
    assert Category.category_count == len(category_list)
    assert Category.product_count == len(product_list)


def test_add_product_and_privat_access(product_category):
    product_list, _ = product_category
    Category.category_count = 0
    Category.product_count = 0
    category = Category("Смартфоны", "Качественные и крутые только у нас!", [])
    for i, product in enumerate(product_list):
        category.add_product(product)
    assert category.products == (
        "Samsung Galaxy S25 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 16, 210000.0 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
        '55" QLED 4K, 123000.0 руб. Остаток: 7 шт.\n'
    )
    assert category.product_count == len(product_list)


def test_add_product_merge_duplicate(product_category):
    """Тестирует функцию add_product"""
    Category.product_count = 0
    product_list, _ = product_category
    new_product1 = Product(
        "Samsung Galaxy S25 Ultra", "256GB, Серый цвет, 200MP камера", 60000.0, 2
    )

    new_product2 = Product("Iphone 16", "512GB, Gray space", 250000.0, 7)
    new_product3 = Product(
        "Nokia Clear Phone",
        "Кусок стекла похожий на телефон, 10GB, Transparent",
        50000.0,
        10,
    )
    category = Category(
        "Смартфоны", "Качественные и крутые только у нас!", product_list
    )
    assert len(category._Category__products) == 4
    assert Category.product_count == 4

    category.add_product(new_product1)
    assert len(category._Category__products) == 4
    assert Category.product_count == 4
    assert category._Category__products[0].name == "Samsung Galaxy S25 Ultra"
    assert category._Category__products[0].quantity == 5 + 2
    assert category._Category__products[0].price == 180000.0

    category.add_product(new_product2)
    assert len(category._Category__products) == 4
    assert Category.product_count == 4
    assert category._Category__products[1].name == "Iphone 16"
    assert category._Category__products[1].quantity == 8 + 7
    assert category._Category__products[1].price == 250000.0

    category.add_product(new_product3)
    assert len(category._Category__products) == 5
    assert Category.product_count == 5
    assert category._Category__products[4].name == "Nokia Clear Phone"
    assert category._Category__products[4].quantity == 10
    assert category._Category__products[4].price == 50000.0


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
    assert category_smartphones.description == "Смартфоны, для удобства жизни"
    assert len(category_smartphones._Category__products) == 2

    samsung = category_smartphones._Category__products[0]
    assert samsung.name == "Samsung Galaxy S25 Ultra"
    assert samsung._Product__price == 180000.0
    assert samsung.quantity == 5

    category_tvs = loaded_categories[0]
    assert category_tvs.name == "Смартфоны"
    assert len(category_tvs._Category__products) == 2

    qled_tv = category_tvs._Category__products[0]
    assert qled_tv.name == "Samsung Galaxy S25 Ultra"
    assert qled_tv._Product__price == 180000.0


def test_load_file_from_json_file_not_found():
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


def test_new_product_classmethod(product_data_for_new_product):
    """Тестирование new_product"""
    data = product_data_for_new_product
    new_product_instance = Product.new_product(data)
    assert isinstance(new_product_instance, Product)
    assert new_product_instance.name == data["name"]
    assert new_product_instance.description == data["description"]
    assert new_product_instance._Product__price == data["price"]
    assert new_product_instance.quantity == data["quantity"]


@pytest.mark.parametrize(
    "name, description, price, quantity, expected, mail",
    [
        (
            "Российский Т-90",
            "Лучший народный танк! Сделан в РОССИИ!",
            2500000,
            500,
            2500000,
            None,
        ),
        (
            "Китайский MBT-2000",
            "Китайцы решили поделиться со своими танками! Вот это дружба, я понимаю!",
            0,
            2000,
            0.0,
            "Цена не должна быть нулевая или отрицательная",
        ),
        (
            "Немецкий Leopard 2",
            "Немцы нам еще не выплатили долг! Пусть оплатят и тогда купим у них танк!"
            "(нельзя снабжать фашистов! это грех!)",
            -2499000000,
            270,
            0.0,
            "Цена не должна быть нулевая или отрицательная",
        ),
    ],
)
def test_price_list(name, description, price, quantity, expected, mail, capsys):
    """Тестирует сеттер price_list"""
    data = Product(name, description, price, quantity)
    assert data.price == expected

    captured = capsys.readouterr()
    if mail:
        assert mail in captured.out
    else:
        assert captured.out == ""


def test_y_n_price(capsys, mocker):
    """Проверка сообщений ответа на вопрос в сеттер"""
    product = Product(
        "Американский M1 Abrams",
        "У америкосов плохие танки, лучше купите РУССКИЕ!",
        8600000,
        150,
    )
    new_price = 5000

    mocker.patch("builtins.input", side_effect=["4", "n", "y"])

    product.price = new_price
    assert product.price == 8600000
    captured = capsys.readouterr()
    assert (
        "Неправильно введено значение(yes - y/n - no). Снижение цены отменено"
        in captured.out
    )

    product.price = new_price
    assert product.price == 8600000
    captured = capsys.readouterr()
    assert "Снижение цены отменено" in captured.out

    product.price = new_price
    assert product.price == new_price
    captured = capsys.readouterr()
    assert f"Цена снижена до {new_price} руб." in captured.out
