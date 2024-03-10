from json import load
from re import sub
from datetime import datetime


def get_operations(file_name: str) -> list:
    """Getting user operations from local file"""
    file = open(file_name, 'r', encoding='UTF-8')
    result = load(file)
    file.close()
    return result


def filter_exec_operations(operations: list, last_count: int) -> list:
    """Filtered by status and sorted by date"""
    return sorted(
        [item for item in operations if item.get('state') == 'EXECUTED'],
        key=lambda x: x.get('date'))[-last_count:]


def hide_bank_account(bank_acc: str) -> str:
    if bank_acc is None or len(bank_acc) == 0:
        return 'UNKNOWN'

    if bank_acc.startswith('Счет'):
        return f"Счет **{bank_acc[-4:]}"
    else:
        return sub(r'(\d{4})(\d{2})\d{6}(\d{4})', r'\1 \2** **** \3', bank_acc)


def print_operation(operation: dict) -> None:
    """Operation output"""
    print(f"{datetime.strptime(operation.get('date'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')} "
          f"{operation.get('description')}")
    print(f"{hide_bank_account(operation.get('from'))} -> {hide_bank_account(operation.get('to'))}")
    print(f"{operation.get('operationAmount').get('amount')} "
          f"{operation.get('operationAmount').get('currency').get('name')}\n")


user_operations = get_operations('operations.json')
[print_operation(op) for op in filter_exec_operations(user_operations, 5)]
