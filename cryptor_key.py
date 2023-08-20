from cryptography.fernet import Fernet


def generate_key():
    """Генерирует ключ шифрования."""
    return Fernet.generate_key()


def encrypt_data(data, key):
    """Шифрует данные с использованием ключа."""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    """Расшифровывает данные с использованием ключа."""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


# Пример использования:

# 1. Генерируем ключ (это нужно сделать только один раз и сохранить ключ в безопасном месте)
key = generate_key()
print("Generated key:", key.decode())

# 2. Шифруем учетные данные
encrypted_username = encrypt_data("REPLACE_ADMIN_NAME", key)
encrypted_password = encrypt_data("REPLACE_ADMIN_PASSWORD", key)

print("encrypted_username: ", encrypted_username)
print("encrypted_password: ", encrypted_password)

# 3. Расшифровываем учетные данные (это вы будете делать в вашем основном скрипте)
decrypted_username = decrypt_data(encrypted_username, key)
decrypted_password = decrypt_data(encrypted_password, key)

print(decrypted_username, decrypted_password)
