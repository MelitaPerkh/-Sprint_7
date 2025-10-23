import requests
import random
import string

class CourierHelper:
    
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def register_new_courier_and_return_login_password(self):
        login_pass = []
        
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{self.BASE_URL}/courier', data=payload)
        
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)
        
        return login_pass
    
    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{self.BASE_URL}/courier/login', data=payload)
        return response
    
    def delete_courier(self, courier_id):
        response = requests.delete(f'{self.BASE_URL}/courier/{courier_id}')
        return response