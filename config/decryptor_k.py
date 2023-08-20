from cryptography.fernet import Fernet


def decrypt_data(encrypted_data, key):
    """Расшифровывает данные с использованием ключа."""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data