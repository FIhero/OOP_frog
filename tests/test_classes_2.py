import pytest

from src.classes import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def product_category():
    """Фикстура для тестирования счетчиков категорий и продуктов"""

    Category.category_count = 0
    Category.product_count = 0

    sp1 = Smartphone(
        "Samsung Galaxy S25 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        "Qualcomm Snapdragon 8 Elite",
        "SM-S938B",
        256,
        "Gray",
    )
    sp2 = Smartphone(
        "Iphone 16",
        "512GB, Gray space",
        210000.0,
        8,
        "A18",
        "iPhone 16",
        512,
        "Gray space",
    )
    sp3 = Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        "Qualcomm Snapdragon 680",
        "Xiaomi Redmi Note 11",
        1024,
        "Blue",
    )

    products_sp = [sp1, sp2, sp3]

    ld1 = LawnGrass(
        "Huter GLM-460ST", "Бензиновая газонокосилка", 25500, 10, "Китай", 1, "красный"
    )
    ld2 = LawnGrass(
        "CHAMPION LM4630", "Самоходная газонокосилка", 35000, 6, "Китай", 5, "черный"
    )
    ld3 = LawnGrass(
        "Hyundai LE 4600S",
        "Электрическая газонокосилка",
        27890,
        10,
        "Китай",
        3,
        "синий",
    )

    products_lg = [ld1, ld2, ld3]

    return products_sp, products_lg


@pytest.fixture
def empty_category():
    """Фикстура для пустой категории"""
    Category.product_count = 0
    return Category("Юмор", "Смешные цены на несмешные товары", [])


def test_class_smartphone_lowngrass(product_category):
    """Тестирует правильность ввода информации в класс Smaprtphone и LawnGrass"""
    sp, lg = product_category
    sp, _, _ = sp
    lg, _, _ = lg

    assert sp.__str__() == (
        "Samsung Galaxy S25 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "256GB, Серый цвет, 200MP камера\n"
        "Модель: SM-S938B\n"
        "Ядро: Qualcomm Snapdragon 8 Elite\n"
        "Объем памяти: 256 GB\n"
        "Цвет: Gray\n"
    )

    assert lg.__str__() == (
        "Huter GLM-460ST, 25500 руб. Остаток: 10 шт.\n"
        "Бензиновая газонокосилка\n"
        "Страна производитель: Китай\n"
        "Срок службы: 1 год\n"
        "Цвет: красный\n"
    )


def test_add_class(product_category):
    """Тестирует метод __add__ правильный и ошибочный вариант"""
    sp, lg = product_category
    sp1, sp2, sp3 = sp
    lg1, lg2, lg3 = lg

    exp1 = sp1.price * sp1.quantity
    exp2 = sp2.price * sp2.quantity
    exp4 = lg1.price * lg1.quantity
    exp5 = lg2.price * lg2.quantity

    assert sp1 + sp2 == exp1 + exp2
    assert lg1 + lg2 == exp4 + exp5
    with pytest.raises(
        TypeError, match="Можно складывать товары только одного и того же класса"
    ):
        _ = sp3 + lg3


def test_value_error_in_quntity(empty_category):
    """Тестирует ошибки при нуле и ниже количество в add_product"""
    category = empty_category
    p1 = Product("Мазь", "Смешная мазь", 5000000, 0)
    p2 = Product("Крем", "Грустный крем", 5, -300)
    with pytest.raises(
        ValueError,
        match="Товар с нулевым или отрицательным количеством не может быть добавлен",
    ):
        category.add_product(p1)
    with pytest.raises(
        ValueError,
        match="Товар с нулевым или отрицательным количеством не может быть добавлен",
    ):
        category.add_product(p2)
