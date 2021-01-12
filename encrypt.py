from cryptography.fernet import Fernet

# This is how you originally generate the key
# key = Fernet.generate_key()


# Load the saved key_file
with open('file_key.txt', 'rb') as f:
    key = f.read()
cypher = Fernet(key)

filename = 'mine.inventory'

# Open the saved data file
with open(filename, 'rb') as f:
    e_file = f.read()

# Encrypt the data file
encrypted_file = cypher.encrypt(e_file)

# Save the encrypted file
with open(f'e_{filename}', 'wb') as f:
    f.write(encrypted_file)






# encrypted_text = cypher.encrypt(b'something safe')
# print(encrypted_text)

# original_text = cypher.decrypt(encrypted_text)
# print(original_text)
