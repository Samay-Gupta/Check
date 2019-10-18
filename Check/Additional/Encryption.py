import os


class Encryption:
    def __init__(self, directory='Additional', filename="Key.txt"):
        file_path = os.getcwd() + '\\' + directory + '\\'
        key_file = file_path + filename
        with open(key_file, 'r') as file:
            self.encryption_key = file.read()

    def encrypt(self, data=''):
        key = self.encryption_key*(len(str(data))//64+1)
        encrypted = ''
        for i in range(len(data)):
            char_id = str(ord(data[i])+ord(key[i]))
            char_val = '0'*(3-len(str(char_id)))+char_id
            encrypted += char_val
        return encrypted

    def decrypt(self, data=''):
        key = self.encryption_key*(len(data)//64+1)
        decrypted = ''
        ctr = 0
        for i in range(0, len(data)//3):
            char_id = int(data[ctr:ctr+3])
            decrypted += chr(char_id-ord(key[i]))
            ctr += 3
        return decrypted

