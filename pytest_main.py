import pytest
from main import filter_exec_operations, hide_bank_account, print_operation


@pytest.fixture
def fake_operations():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2019-08-25T12:34:56.789123",
            "operationAmount": {
                "amount": "10000.00",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Покупка товара",
            "from": "Visa 1234567890123456",
            "to": "Магазин 'Мой товар'"
        }
    ]


def test_filter_exec_operations(fake_operations):
    # Тестируем функцию filter_exec_operations
    result = filter_exec_operations(fake_operations, 5)

    # Проверяем, что результат не пустой
    assert result

    # Проверяем, что количество операций в результате соответствует ожидаемому
    assert len(result) == min(len(fake_operations), 5)

    # Проверяем, что операции отсортированы по дате в порядке возрастания
    expected_dates = sorted((op['date'] for op in fake_operations if op.get('state') == 'EXECUTED'))
    assert [op['date'] for op in result] == expected_dates


def test_hide_bank_account():
    # Тестируем функцию hide_bank_account
    assert hide_bank_account(None) == 'UNKNOWN'
    assert hide_bank_account('Счет 1234567890123456') == 'Счет **3456'
    assert hide_bank_account('1234123412341234') == '1234 12** **** 1234'


def test_print_operation(capfd):
    # Создаем операцию
    operation = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }

    # Перенаправляем вывод stdout для проверки вывода функции
    print_operation(operation)

    # Проверяем, что вывод функции соответствует ожидаемому
    captured = capfd.readouterr()
    expected_output = '''\
26.08.2019 Перевод организации
Maestro 1596 83** **** 5199 -> Счет **9589
31957.58 руб.
'''
    # Убедимся, что строки совпадают
    assert captured.out.strip() == expected_output.strip()
