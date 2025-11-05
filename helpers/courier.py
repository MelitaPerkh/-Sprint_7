import allure
from helpers.generators import DataGenerator
from helpers.api_client import ScooterApiClient

class CourierHelper:
    
    def __init__(self):
        self.api_client = ScooterApiClient()
        self.generator = DataGenerator()

    @allure.step("Регистрация нового курьера")
    def register_new_courier_and_return_login_password(self):
       
        login_pass = []
        
        # Генерация данных
        login, password, first_name = self.generator.generate_courier_data()
        
        # API вызов
        response = self.api_client.register_new_courier(login, password, first_name)
        
        # Обработка результата
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)
        
        return login_pass
    
    @allure.step("Авторизация курьера")
    def login_courier(self, login, password):
        return self.api_client.login_courier(login, password)
    
    @allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
       return self.api_client.delete_courier(courier_id)
    
    @allure.step("Генерация случайной строки")
    def generate_random_string(self, length):
        return self.generator.generate_random_string(length)