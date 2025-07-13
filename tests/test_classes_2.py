import pytest

from src.classes import (
    Category,
    LawnGrass,
    Order,
    Product,
    Smartphone,
    ZeroQuantityError,
)


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


def test_class_smartphone_lawngrass(product_category):
    """Тестирует правильность ввода информации в класс Smartphone и LawnGrass"""
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


def test_value_error_in_quantity():
    """Тестирует ошибки при нуле и ниже количестве в классе Product"""
    with pytest.raises(
        ValueError,
        match="Товар с нулевым количеством не может быть добавлен",
    ):
        Product("Мазь", "Смешная мазь", 5000000, 0)
    with pytest.raises(
        ValueError,
        match="Товар с нулевым количеством не может быть добавлен",
    ):
        Product("Крем", "Грустный крем", 5, -300)


def test_add_order(product_category):
    """Проверка работы класса Order"""
    product, _ = product_category
    sp1, _, _ = product

    or1 = Order(sp1, 5)

    assert or1.__str__() == (
        "Заказ: Samsung Galaxy S25 Ultra",
        "Количество: 5 шт.",
        "Итого: 900000.0 руб.",
    )


def test_error_mail_in_order(product_category):
    """Тестирует возможные ощибки в Order"""
    empty = Product("", "", 0, 1)

    with pytest.raises(
        TypeError, match="Заказ должен содержать только объекты Product"
    ):
        o1 = Order("Туда-сюда", "И милионер")

        assert o1.quantity == 0
        assert o1.total_cost == 0

    with pytest.raises(
        ValueError,
        match="Количество товара в заказе должно быть положительным целым числом",
    ):
        o1 = Order(empty, 0)
    with pytest.raises(
        ValueError,
        match="Количество товара в заказе должно быть положительным целым числом",
    ):
        Order(empty, -5)

        assert o1.quantity == 0
        assert o1.total_cost == 0


def test_average_price_of_goods(product_category):
    """Тестирует average_price_of_goods в классе Category"""
    sp, lg = product_category
    category_sp = Category("Смартфоун", "Сделано в корее", sp)
    category_lg = Category(
        "Газонокосилка", "Не поняла что нужна была трава, так что да", lg
    )
    empty = Category("", "", [])

    assert category_sp.average_price_of_goods() == pytest.approx(111629.63)
    assert category_lg.average_price_of_goods() == pytest.approx(28611.54)
    assert empty.average_price_of_goods() == 0


def test_order_creation_prints_messages(capsys):
    """Тестирует сообщения об ошибках в классе Order"""
    valid_product = Product("gugu", "gaga", 100, 10)

    Order(valid_product, 5)
    captures = capsys.readouterr()
    assert "Начало обработки заказа" in captures.out
    assert "Заказ успешно создан" in captures.out
    assert "Обработка создания заказа завершена" in captures.out
    assert captures.err == ""

    with pytest.raises(ZeroQuantityError):
        error = Order(valid_product, -4)
        captures = capsys.readouterr()
        assert "Начало обработки заказа" in captures.out
        assert (
            "Ошибка создания заказа: Количество товара в заказе должно быть положительным целым числом"
            in captures.out
        )
        assert "Обработка создания заказа завершена" in captures.out
        assert captures.err == ""
        assert error.quantity == 0
        assert error.total_cost == 0

    with pytest.raises(TypeError):
        error = Order("Ох", 5)
        captures = capsys.readouterr()
        assert "Начало обработки заказа" in captures.out
        assert (
            "Ошибка создания заказа: Заказ должен содержать только объекты Product"
            in captures.out
        )
        assert "Обработка создания заказа завершена" in captures.out
        assert captures.err == ""
        assert error.quantity == 0
        assert error.total_cost == 0


def test_exception_error_prints_messages(capsys):
    """Тестирует ошибку Exception в классе Order"""

    class Milfa(Product):
        def __init__(self, name, description, price, quantity):
            super().__init__(name, description, price, quantity)

            if hasattr(self, "_price"):
                del self._price

    pro = Milfa("ЛАлал", "kfkfk", 6, 3)
    with pytest.raises(AttributeError) as excinfo:
        Order(pro, 2)
        message = str(excinfo.value)
        captures = capsys.readouterr()
        assert "Начало обработки заказа" in captures.out
        assert "Произошла непредвиденная ошибка при создания заказа:" in captures.out
        assert message in captures.out
        assert "Обработка создания заказа завершена" in captures.out
        assert captures.err == ""
