from cryptography.fernet import Fernet
import os

# encrypt_key = '55ee9fd08e4c6449044b6e58528a7a09cd5c3d7aa31db0c302a23fb9d36e6006'


# Генерируем ключ (сохраните его в .env!)
# KEY = Fernet.generate_key()  # Пример: b'APM1JDVgT8WDGjBg6v0ZM2BwQ5lY0k-5PJ8f1B5Z3oE='

KEY = 'cagezW5S11_5QejppMzX1lzi66lZGh3HNDYRMwEiZvg='

cipher = Fernet(KEY)

def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()