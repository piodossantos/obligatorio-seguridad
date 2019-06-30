import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

'''
Created by Pio dos Santos, Dhiago Rivera, Pedro Heguy
'''


class AESCipher(object):
    def __init__(self, key="default", isCipherKey=False, block_size=32):
        self.bs = block_size
        if isCipherKey:
            # No necesito cifrar la clave
            self.key = key
        else:
            # Se obtiene una clave cifrada
            self.key = SHA256Cipher().hashDigest(text=key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

class RSACipher(object):
    def __init__(self):
        pass;
    def encrypt(self,raw):
        pass
    def decrypt(self,enc):
        pass

class SHA256Cipher(object):
    def __init__(self):
        self.instance = SHA256.new()

    def hashDigest(self, text):
        self.instance.update(text.encode())
        return self.instance.digest()
    def hash(self,text):
        self.instance.update(text.encode())
        return self.instance.hexdigest()
