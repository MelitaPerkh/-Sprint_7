import pytest
import allure
import sys
import os

# Добавляем папку helpers в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импортируем напрямую из модуля
from helpers.courier import CourierHelper

@pytest.fixture
def courier_helper():
    """Фикстура для работы с курьерами"""
    return CourierHelper()

@pytest.fixture
def base_url():
    """Фикстура с базовым URL"""
    return "https://qa-scooter.praktikum-services.ru/api/v1"

@pytest.fixture
def courier_data():
    """Фикстура для хранения данных курьеров"""
    return []

@pytest.fixture
def setup_courier(courier_helper):
    """Фикстура для создания и очистки тестового курьера"""
    courier_data = []
    
    # Создаем курьера перед тестом
    new_courier = courier_helper.register_new_courier_and_return_login_password()
    if new_courier:  # Проверяем что курьер создан
        courier_data.append(new_courier)
    
    yield courier_data  # Передаем данные в тест
    
    # Очищаем после теста
    for data in courier_data:
        if len(data) >= 2:
            login, password = data[0], data[1]
            response = courier_helper.login_courier(login, password)
            if response.status_code == 200:
                courier_id = response.json().get("id")
                if courier_id:
                    courier_helper.delete_courier(courier_id)