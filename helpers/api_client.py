import requests
import allure
from helpers.generators import DataGenerator

class ScooterApiClient:
    
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    @allure.step("Регистрация курьера (login: {login})")
    def register_new_courier(self, login, password, first_name):
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        return response
    
    @allure.step("Авторизация курьера (login: {login})")
    def login_courier(self, login, password):
       
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        return response
    
    @allure.step("Удаление курьера (id: {courier_id})")
    def delete_courier(self, courier_id):
        response = requests.delete(f'{self.BASE_URL}/courier/{courier_id}')
        return response
    
    @allure.step("Создание заказа")
    def create_order(self, order_data):
        response = requests.post(f'{self.BASE_URL}/orders', json=order_data)
        return response
    
    @allure.step("Получение списка заказов ")
    def get_orders_list(self):
        response = requests.get(f'{self.BASE_URL}/orders')
        return response