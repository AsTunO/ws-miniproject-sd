from cryptography.fernet import Fernet

class CryptographyService:
    def __init__(self, key):
        self.cipher_suite = Fernet(key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()
