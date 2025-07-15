from cryptography.fernet import Fernet

# Generate a secure random Fernet key
key = Fernet.generate_key()

# Print the key so you can copy it to your .env file
print("Your FERNET_KEY is:\n", key.decode())