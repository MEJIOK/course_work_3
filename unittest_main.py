import unittest
import json
import tempfile
import os
import sys
import io

from main import get_operations, filter_exec_operations, hide_bank_account, print_operation


class TestAllFunctions(unittest.TestCase):
    def setUp(self):
        # Создаем фиктивные операции для тестирования
        self.fake_operations = [
            {"state": "EXECUTED", "date": "2024-03-10T08:00:00.000Z", "description": "Test operation 1",
             "from": "1234567890123456", "to": "9876543210987654",
             "operationAmount": {"amount": 100, "currency": {"name": "USD"}}},
            {"state": "PENDING", "date": "2024-03-09T08:00:00.000Z", "description": "Test operation 2",
             "from": "9876543210987654", "to": "1234567890123456",
             "operationAmount": {"amount": 200, "currency": {"name": "EUR"}}},
            {"state": "EXECUTED", "date": "2024-03-08T08:00:00.000Z", "description": "Test operation 3",
             "from": "1234567890123456", "to": "9876543210987654",
             "operationAmount": {"amount": 300, "currency": {"name": "GBP"}}}
        ]

    def test_get_operations(self):
        # Создаем временный файл для тестирования
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump(self.fake_operations, f)

        # Тестируем функцию get_operations
        result = get_operations(f.name)

        # Проверяем, что результат не пустой и содержит ожидаемое количество операций
        self.assertTrue(result)
        self.assertEqual(len(result), len(self.fake_operations))

        # Удаляем временный файл
        os.remove(f.name)

    def test_filter_exec_operations(self):
        # Тестируем функцию filter_exec_operations
        result = filter_exec_operations(self.fake_operations, 2)

        # Проверяем, что результат не пустой и содержит ожидаемое количество операций
        self.assertTrue(result)
        self.assertEqual(len(result), 2)

        # Проверяем, что операции отсортированы по дате в порядке убывания
        expected_dates = ['2024-03-10T08:00:00.000Z', '2024-03-08T08:00:00.000Z']
        self.assertEqual([op['date'] for op in result], expected_dates)

    def test_hide_bank_account(self):
        # Тестируем функцию hide_bank_account
        bank_acc_1 = '1234567890123456'
        bank_acc_2 = 'Счет 1234567890123456'
        bank_acc_3 = '1234123412341234'

        self.assertEqual(hide_bank_account(bank_acc_1), '1234 56** **** 3456')
        self.assertEqual(hide_bank_account(bank_acc_2), 'Счет **3456')
        self.assertEqual(hide_bank_account(bank_acc_3), '1234 12** **** 1234')

    def test_print_operation(self):
        # Тестируем функцию print_operation
        operation = {
            "date": "2024-03-10T08:00:00.000Z",
            "description": "Test operation",
            "from": "1234567890123456",
            "to": "9876543210987654",
            "operationAmount": {"amount": 100, "currency": {"name": "USD"}}
        }

        # Воспользуемся перенаправлением вывода stdout для проверки вывода функции
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_operation(operation)
        printed_output = captured_output.getvalue()

        expected_output = '''10.03.2024 Test operation
1234 56** **** 3456 -> 9876 54** **** 7654
100 USD\n'''

        self.assertEqual(printed_output, expected_output)


if __name__ == '__main__':
    unittest.main()
