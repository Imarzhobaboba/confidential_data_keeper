from cryptography.fernet import Fernet
from config import settings


KEY = settings.FERNET_ENCRYPTION_KEY

cipher = Fernet(KEY)

def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()