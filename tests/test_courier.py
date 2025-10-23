import pytest
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers.courier import CourierHelper

class TestCourierCreation:
    
    courier_helper = CourierHelper()
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    def setup_method(self):
        self.courier_data = []
    
    def teardown_method(self):
        # Очистка созданных курьеров
        for data in self.courier_data:
            if len(data) >= 2:
                login, password = data[0], data[1]
                response = self.courier_helper.login_courier(login, password)
                if response.status_code == 200:
                    courier_id = response.json().get("id")
                    if courier_id:
                        self.courier_helper.delete_courier(courier_id)
    
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        courier_data = self.courier_helper.register_new_courier_and_return_login_password()
        self.courier_data.append(courier_data)
        
        assert len(courier_data) == 3, "Курьер не был создан"
        assert isinstance(courier_data[0], str), "Логин должен быть строкой"
        assert isinstance(courier_data[1], str), "Пароль должен быть строкой"
    
    def test_create_duplicate_courier(self):
        """Тест создания дубликата курьера"""
        # Создаем первого курьера
        courier_data = self.courier_helper.register_new_courier_and_return_login_password()
        self.courier_data.append(courier_data)
        
        login, password, first_name = courier_data
        
        # Пытаемся создать курьера с таким же логином
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        
        assert response.status_code == 409, "Ожидался код 409 для дубликата"
        assert "Этот логин уже используется" in response.text
    
    def test_create_courier_missing_login(self):
        """Тест создания курьера без логина"""
        payload = {
            "password": self.courier_helper.generate_random_string(10),
            "firstName": self.courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        
        assert response.status_code == 400, "Ожидался код 400 при отсутствии логина"
    
    def test_create_courier_missing_password(self):
        """Тест создания курьера без пароля"""
        payload = {
            "login": self.courier_helper.generate_random_string(10),
            "firstName": self.courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        
        assert response.status_code == 400, "Ожидался код 400 при отсутствии пароля"
    
    def test_create_courier_success_response(self):
        """Тест корректного ответа при успешном создании курьера"""
        login = self.courier_helper.generate_random_string(10)
        password = self.courier_helper.generate_random_string(10)
        first_name = self.courier_helper.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        self.courier_data.append([login, password, first_name])
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}


class TestCourierLogin:
    
    courier_helper = CourierHelper()
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    def setup_method(self):
        self.courier_data = []
    
    def teardown_method(self):
        for data in self.courier_data:
            if len(data) >= 2:
                login, password = data[0], data[1]
                response = self.courier_helper.login_courier(login, password)
                if response.status_code == 200:
                    courier_id = response.json().get("id")
                    if courier_id:
                        self.courier_helper.delete_courier(courier_id)
    
    def test_login_success(self):
        """Тест успешной авторизации курьера"""
        courier_data = self.courier_helper.register_new_courier_and_return_login_password()
        self.courier_data.append(courier_data)
        
        login, password = courier_data[0], courier_data[1]
        response = self.courier_helper.login_courier(login, password)
        
        assert response.status_code == 200
        assert "id" in response.json()
    
    def test_login_missing_login(self):
        """Тест авторизации без логина"""
        payload = {
            "password": self.courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        
        assert response.status_code == 400
    
    def test_login_missing_password(self):
        """Тест авторизации без пароля"""
        payload = {
            "login": self.courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        
        assert response.status_code == 400
    
    def test_login_wrong_password(self):
        """Тест авторизации с неправильным паролем"""
        courier_data = self.courier_helper.register_new_courier_and_return_login_password()
        self.courier_data.append(courier_data)
        
        login = courier_data[0]
        wrong_password = self.courier_helper.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": wrong_password
        }
        
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        
        assert response.status_code == 404
    
    def test_login_nonexistent_user(self):
        """Тест авторизации несуществующего пользователя"""
        payload = {
            "login": self.courier_helper.generate_random_string(10),
            "password": self.courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        
        assert response.status_code == 404
    
    def test_login_success_returns_id(self):
        """Тест, что успешная авторизация возвращает ID"""
        courier_data = self.courier_helper.register_new_courier_and_return_login_password()
        self.courier_data.append(courier_data)
        
        login, password = courier_data[0], courier_data[1]
        response = self.courier_helper.login_courier(login, password)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)