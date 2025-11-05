import pytest
import requests
import allure

class TestCourierCreation:
    
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_helper):
        courier_data = courier_helper.register_new_courier_and_return_login_password()
        
        assert len(courier_data) == 3, "Курьер не был создан"
        assert isinstance(courier_data[0], str), "Логин должен быть строкой"
        assert isinstance(courier_data[1], str), "Пароль должен быть строкой"
    
    @allure.title("Cозданиe дубликата курьера")
    def test_create_duplicate_courier(self, setup_courier, base_url):
        courier_data = setup_courier
        login, password, first_name = courier_data[0]
        
        # Пытаемся создать курьера с таким же логином
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{base_url}/courier', data=payload)
        
        assert response.status_code == 409, "Ожидался код 409 для дубликата"
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Этот логин уже используется" in response_data["message"]
    
    @allure.title("Cозданиe курьера без логина")
    def test_create_courier_missing_login(self, courier_helper, base_url):
        payload = {
            "password": courier_helper.generate_random_string(10),
            "firstName": courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{base_url}/courier', data=payload)
        
        assert response.status_code == 400, "Ожидался код 400 при отсутствии логина"
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Недостаточно данных" in response_data["message"]
   
    @allure.title("Cозданиe курьера без пароля")
    def test_create_courier_missing_password(self, courier_helper, base_url):
        payload = {
            "login": courier_helper.generate_random_string(10),
            "firstName": courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{base_url}/courier', data=payload)
        
        assert response.status_code == 400, "Ожидался код 400 при отсутствии пароля"
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Недостаточно данных" in response_data["message"]
    
    @allure.title("Проверка ответа при успешном создании курьера")
    def test_create_courier_success_response(self, courier_helper, base_url, courier_data):
        login = courier_helper.generate_random_string(10)
        password = courier_helper.generate_random_string(10)
        first_name = courier_helper.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{base_url}/courier', data=payload)
        courier_data.append([login, password, first_name])
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}


class TestCourierLogin:
    
    @allure.title("Проверка успешной авторизации курьера")
    def test_login_success(self, setup_courier, courier_helper):
        courier_data = setup_courier
        login, password = courier_data[0][0], courier_data[0][1]
        response = courier_helper.login_courier(login, password)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)
    
    @allure.title("Проверка авторизации без логина")
    def test_login_missing_login(self, courier_helper, base_url):
        payload = {
            "password": courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{base_url}/courier/login', data=payload)
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Недостаточно данных" in response_data["message"]
    
    @allure.title("Проверка авторизации без пароля")
    def test_login_missing_password(self, courier_helper, base_url):
        payload = {
            "login": courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{base_url}/courier/login', data=payload)
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Недостаточно данных" in response_data["message"]
    
    @allure.title("Проверка авторизации с неправильным паролем")
    def test_login_wrong_password(self, setup_courier, courier_helper, base_url):
        courier_data = setup_courier
        login = courier_data[0][0]
        wrong_password = courier_helper.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": wrong_password
        }
        
        response = requests.post(f'{base_url}/courier/login', data=payload)
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Учетная запись не найдена" in response_data["message"]
    
    @allure.title("Проверка авторизации несуществующего пользователя")
    def test_login_nonexistent_user(self, courier_helper, base_url):
        payload = {
            "login": courier_helper.generate_random_string(10),
            "password": courier_helper.generate_random_string(10)
        }
        
        response = requests.post(f'{base_url}/courier/login', data=payload)
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data, "В ответе должно быть поле message"
        assert "Учетная запись не найдена" in response_data["message"]