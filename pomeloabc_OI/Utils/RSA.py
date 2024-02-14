import os, base64
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5

class RSA():
    def __init__(self, bit = 1024):
        self.bit = bit
        self.__rsa_key = rsa.generate(self.bit)
        self.__pub_key = self.__rsa_key.publickey().export_key("PEM")
        self.__pri_key = self.__rsa_key.export_key("PEM")

        self.__generate__()

        self.__pub_cipher = PKCS1_v1_5.new(self.__get_pub__())
        self.__pri_cipher = PKCS1_v1_5.new(self.__get_pri__())

    def __generate__(self):
        if not os.path.exists("./RSA_keys"):
            os.mkdir("./RSA_keys")
        if not os.path.exists("./RSA_keys/pub_key.pem"):
            with open("./RSA_keys/pub_key.pem", "wb") as file:
                file.write(self.__pub_key)
        if not os.path.exists("./RSA_keys/pri_key.pem"):
            with open("./RSA_keys/pri_key.pem", "wb") as file:
                file.write(self.__pri_key)

    def __get_pub__(self):
        with open("./RSA_keys/pub_key.pem", "rb") as file:
            return rsa.import_key(file.read())
    
    def __get_pri__(self):
        with open("./RSA_keys/pri_key.pem", "rb") as file:
            return rsa.import_key(file.read())

    def text_encode(self, data, charset = 'utf-8'):
        data = data.encode(charset)
        length = len(data)
        default_length = 117
        res = []
        for i in range(0, length, default_length):
            res.append(self.__pub_cipher.encrypt(data[i:i + default_length]))
        byte_data = b''.join(res)
        return base64.b64encode(byte_data)

    def text_decode(self, data, sentinel = b'Decrypt Error'):
        data = base64.b64decode(data)
        length = len(data)
        default_length = 128
        res = []
        for i in range(0, length, default_length):
            res.append(self.__pri_cipher.decrypt(data[i:i + default_length], sentinel))
        return str(b''.join(res), encoding = "utf-8")
    
    def file_encode(self, filename):
        with open("./{}".format(filename), "r") as file:
            text = file.read()
        with open("./{}".format(filename), "wb") as file:
            file.write(self.text_encode(text))
        
    def file_decode(self, filename):
        with open("./{}".format(filename), "r") as file:
            text = file.read()
        with open("./{}".format(filename), "w") as file:
            file.write(self.text_decode(text))