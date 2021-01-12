from cryptography.fernet import Fernet
from pprint import pformat

# This is how you originally generate the key
# key = Fernet.generate_key()


# Load the saved key_file
with open('file_key.txt', 'rb') as f:
    key = f.read()
cypher = Fernet(key)

file = 'e_mine.inventory'

# Open the encrypted file
with open(file, 'rb') as f:
    encrypted_file = f.read()
    print(pformat(encrypted_file, indent=4))

# Decrypt the encrypted data
decrypted_file = cypher.decrypt(encrypted_file)
print(pformat(decrypted_file, indent=4))
