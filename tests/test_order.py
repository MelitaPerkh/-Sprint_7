import pytest
import requests
import sys
import os

# Добавляем папку helpers в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers.courier import CourierHelper

class TestOrderCreation:
    
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    courier_helper = CourierHelper()
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Тест создания заказа с разными вариантами цветов"""
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Тестовая улица, 1",
            "metroStation": 1,
            "phone": "+79999999999",
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый комментарий",
            "color": color
        }
        
        response = requests.post(f'{self.BASE_URL}/orders', json=payload)
        
        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data
        assert isinstance(response_data["track"], int)


class TestOrdersList:
    
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    def test_get_orders_list(self):
        """Тест получения списка заказов"""
        response = requests.get(f'{self.BASE_URL}/orders')
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        
        if len(response_data["orders"]) > 0:
            order = response_data["orders"][0]
            assert "id" in order
            assert "track" in order