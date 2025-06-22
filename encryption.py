from cryptography.fernet import Fernet

# Load secret key from file
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher = Fernet(key)

def encrypt_message(msg):
    return cipher.encrypt(msg)

def decrypt_message(token):
    return cipher.decrypt(token)
