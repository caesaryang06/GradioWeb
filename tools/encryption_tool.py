from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64



class EncryptionUtils:
    @staticmethod
    def encrypt(key, plaintext):
        """
        使用AES算法加密明文

        :param key: 加密密钥，字符串类型
        :param plaintext: 要加密的明文，字符串类型
        :return: 加密后的密文，字符串类型（Base64编码）
        """
        key = key.encode('utf - 8')
        cipher = AES.new(key, AES.MODE_CBC)
        plaintext = plaintext.encode('utf - 8')
        padded_plaintext = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        iv = base64.b64encode(cipher.iv).decode('utf - 8')
        encrypted_text = base64.b64encode(ciphertext).decode('utf - 8')
        return iv + encrypted_text

    @staticmethod
    def decrypt(key, ciphertext):
        """
        使用AES算法解密密文

        :param key: 解密密钥，字符串类型
        :param ciphertext: 要解密的密文，字符串类型（Base64编码）
        :return: 解密后的明文，字符串类型
        """
        key = key.encode('utf - 8')
        iv = base64.b64decode(ciphertext[:24])
        ciphertext = base64.b64decode(ciphertext[24:])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf - 8')
