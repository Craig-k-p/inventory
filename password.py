import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

pass_from_user = input('pass: ')
password = pass_from_user.encode()

# Generate a secure SALT even if a small password is used this will make
# brute force attacks more difficult
mysalt = b'\xba\xfb\x14\x0b\x04\xf1\xdc\x16\xcf\xfa=\x9d6\xac\xe3C'

# Key derivation function
kdf =PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=166214,
        backend=default_backend()
    )

key = base64.urlsafe_b64encode(kdf.derive(password))

print(key.decode())
