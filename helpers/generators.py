import random
import string

class DataGenerator:
    
    @staticmethod
    def generate_random_string(length):
        """Генерация случайной строки из букв нижнего регистра"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    @staticmethod
    def generate_courier_data():
        """Генерация данных для курьера"""
        login = DataGenerator.generate_random_string(10)
        password = DataGenerator.generate_random_string(10)
        first_name = DataGenerator.generate_random_string(10)
        return login, password, first_name