import unittest
from decimal import Decimal
from datetime import date, timedelta

from main import Frige

class TestAdd(unittest.TestCase):
    def setUp(self):
        self.goods = {}
    # 1 - проверка на None в expiration_date (None допускается)
    def test_none_expiration_date(self):
        Frige.add(self.goods, name="Пельмени", quantity=Decimal("1"), expiration_date=None)
        self.assertIn("Пельмени", self.goods)

    # 2 - проверка добавления продукта со всеми параметрами
    def test_add_with_all_parametrs(self):
        Frige.add(self.goods, name="Хлеб", quantity=Decimal("2"), expiration_date="2025-09-29")
        self.assertIn("Хлеб", self.goods)
        self.assertEqual(self.goods["Хлеб"]["quantity"], Decimal("2"))

    #3 - проверка корректного добавления продукта с указанием только обязательных параметров
    def test_add_all_essential_parametrs(self):
        Frige.add(self.goods, name="Масло", quantity=Decimal("1"))
        self.assertIn("Масло", self.goods)
    
    # 4 - проверка не добавления продукта с неверно заданными значениями параметров
    def test_add_with_incorrect_parametrs(self):
        with self.assertRaises(ValueError):
            Frige.add(self.goods, name="Масло", quantity=Decimal("-2"))

class TestAddByNote(unittest.TestCase):
    def setUp(self):
        self.goods = {}
    # 1. Тест для проверки возможности передачи аргумента note без срока годности
    def test_none_expiration_date(self):
        Frige.add_by_note(self.goods, "Пельмени 1 None")
        self.assertIn("Пельмени", self.goods)
    # 2. Тест для проверки корректного добавления продукта с указанием всех параметров
    def test_addbynote_with_all_parametrs(self):
        Frige.add_by_note(self.goods, "Хлеб 2 2025-09-29")
        self.assertIn("Хлеб", self.goods)
        self.assertEqual(self.goods["Хлеб"]["quantity"], Decimal("2"))
    # 3. Тест для проверки корректного добавления продукта без указания срока годности
    def test_addbynote_all_essential_parametrs(self):
        Frige.add_by_note(self.goods, "Масло 1")
        self.assertIn("Масло", self.goods)
    # 4. Тест для проверки не добавления продукта с неверно заданными значениями параметров
    def test_add_with_incorrect_parametrs(self):
        with self.assertRaises(ValueError):
            Frige.add_by_note(self.goods, name="Масло много")

class TestFind(unittest.TestCase):
    def setUp(self):
        self.goods = {
            "Сыр": [{"amount": Decimal("1"), "expiration_date": None}],
            "сырники": [{"amount": Decimal("2"), "expiration_date": "2025, 9, 29"}],
            "Хлеб": [{"amount": Decimal("3"), "expiration_date": "2025, 9, 30"}],
        }

    # 1. Тест для проверки обязательной передачи двух параметров: словарь и строка
    def test_find_requires_dict_and_string(self):
        with self.assertRaises(TypeError):
            Frige.find("Сыр")

    # 2. Тест для проверки корректного поиска одного продукта по точному совпадению названия
    def test_find_exact_match(self):
        result = Frige.find(self.goods, "Хлеб")
        self.assertEqual(result, ["Хлеб"])

    # 3. Тест для проверки корректного поиска нескольких продуктов с одинаковыми фрагментами названия, записанными в разных регистрах
    def test_find_case_insensitive_partial(self):
        result = Frige.find(self.goods, "сыр")
        self.assertIn("Сыр", result)
        self.assertIn("Сырники", result)

    # 4. Тест для проверки поиска с отсутствующим подходящим продуктом
    def test_find_no_result(self):
        result = Frige.find(self.goods, "манка")
        self.assertEqual(result, [])

class TestAmout(unittest.TestCase):
    def setUp(self):
        self.goods = {
            "Сыр": [{"amount": Decimal("1"), "expiration_date": None}, {"amount": Decimal("2"), "expiration_date": "2025, 9, 15"}],
            "Сырники": [{"amount": Decimal("2"), "expiration_date": "2025, 9, 29"}],
            "Хлеб": [{"amount": Decimal("3"), "expiration_date": "2025, 9, 30"}],
        }
    # 1. Тест для проверки возвращаемого значения в формате Decimal
    def test_amount_format(self):
        result = Frige.amount(self.goods, "Молоко")
        self.assertIsInstance(result, Decimal)

    # 2. Тест для проверки возвращаемого корректного количества продукта с указанием ключевого слова для поиска единственного продукта
    def test_amount_correct(self):
        result = Frige.amount(self.goods, "Хлеб")
        self.assertEqual(result, Decimal("3"))
    # 3. Тест для проверки возвращаемого корректного количества продукта с указанием ключевого слова для поиска нескольких партий продукта
    def test_amount_multiple_batches(self):
        result = Frige.amount(self.goods, "Сыр")
        self.assertEqual(result, Decimal("3"))

    # 4. Тест для проверки количества продуктов, отсутствующих в списке продуктов
    def test_amount_no_products(self):
        result = Frige.amount(self.goods, "кукурузные палочки")
        self.assertEqual(result, Decimal("0"))

class TextExpire(unittest.TestCase):
    def setUp(self):
        self.goods = {
            "Сыр": [{"amount": Decimal("1")}, {"amount": Decimal("2"), "expiration_date": "2025, 9, 15"}],
            "Сырники": [{"amount": Decimal("2"), "expiration_date": "2025, 10, 5"}],
            "Хлеб": [{"amount": Decimal("3"), "expiration_date": "2025, 9, 30"}],
        }

    # 1. Тест для проверки возможности вызова функции без параметра in_advance_days
    def test_expire_without_in_advance_days(self):
        result = Frige.expire(self.goods)
        self.assertIn("Сыр", result)

    # 2. Тест для проверки корректного вывода продуктов с истекшим сроком хранения
    def test_expire_correct_output(self):
        result = Frige.expire(self.goods, in_advance_days=0)
        self.assertIn([("Сыр", Decimal("2"))], result)

    # 3. Тест для проверки корректного вывода продуктов, срок хранения которых истекает через несколько дней
    def test_expire_correct_output_in_advance(self):
        result = Frige.expire(self.goods, in_advance_days=2)
        self.assertIn([("Сыр", Decimal("2")), ("Хлеб", Decimal("3"))], result)

    # 4. Тест для проверки корректной обработки продуктов, для которых не указан срок хранения
    def test_expire_correct_output_in_advance(self):
        result = Frige.expire(self.goods)
        self.assertNotIn(["Сыр", Decimal("1")], result)

if __name__ == "__main__":
    unittest.main()