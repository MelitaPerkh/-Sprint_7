import pytest
import requests
import allure

class TestOrderCreation:
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Создание заказа с разными вариантами цветов")
    def test_create_order_with_different_colors(self, color, base_url):
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
        
        response = requests.post(f'{base_url}/orders', json=payload)
        
        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data
        assert isinstance(response_data["track"], int)


class TestOrdersList:
    
    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, base_url):
        response = requests.get(f'{base_url}/orders')
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        
        assert len(response_data["orders"]) > 0, "Список заказов не должен быть пустым"
        order = response_data["orders"][0]
        assert "id" in order
        assert "track" in order