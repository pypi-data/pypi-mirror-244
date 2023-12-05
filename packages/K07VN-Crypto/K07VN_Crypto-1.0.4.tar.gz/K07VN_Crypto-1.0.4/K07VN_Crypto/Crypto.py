

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

class Crypto:
    def __init__(self, public_key=None, private_key=None):
        if public_key:
            self.public_key = RSA.import_key(public_key)
        else:
            self.key = RSA.generate(2048)
            self.public_key = self.key.publickey()

        if private_key:
            self.private_key = RSA.import_key(private_key)
        else:
            self.private_key = None

    @staticmethod
    def generate_key():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return private_key.decode('utf-8'), public_key.decode('utf-8')

    def encrypt(self, plaintext):
        cipher = PKCS1_OAEP.new(self.public_key)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        encrypted_text = base64.b64encode(ciphertext).decode('utf-8')
        return encrypted_text

    def decrypt(self, encrypted_text):
        cipher = PKCS1_OAEP.new(self.private_key)
        ciphertext = base64.b64decode(encrypted_text)
        decrypted_text = cipher.decrypt(ciphertext).decode('utf-8')
        return decrypted_text


