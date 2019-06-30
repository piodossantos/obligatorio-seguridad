from django.contrib.auth.hashers import (
    PBKDF2PasswordHasher,
)
import base64

from utils.Ciphers import SHA256Cipher


class Seguridad03Hasher(PBKDF2PasswordHasher):
    algorithm = 'sha256'
    iterations = 1000000
    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        if not iterations:
            iterations = self.iterations
        hash = SHA256Cipher().hash(text=password)
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)