import hashlib
import json
import random
import time
from Cryptodome.Cipher import AES
import base64

def generate_salt(length):
    random.seed(time.time())
    data = "AbcDE123IJKLMN67QRSTUVWXYZ"
    data += "aBCdefghijklmn123opq45rs67tuv89wxyz"
    data += "0FGH45OP89"
    salt = ''.join(random.choice(data) for _ in range(length))
    return salt

def pad_key(key, length):
    if len(key) >= length:
        return key[:length]
    else:
        return key.ljust(length, '0')

def encrypt(input_str, key):
    iv = "@@@@&&&&####$$$$".encode('utf-8')
    key = pad_key(key, 16).encode('utf-8')  # AES-128-CBC uses a 16-byte key
    input_str = input_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding_length = 16 - (len(input_str) % 16)
    padded_input = input_str + bytes([padding_length]) * padding_length
    encrypted_bytes = cipher.encrypt(padded_input)
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_b64

def get_checksum_from_string(data_str, key):
    salt = generate_salt(4)
    final_string = f"{data_str}|{salt}"
    print("Final string with salt:", final_string)
    hash_str = hashlib.sha256(final_string.encode('utf-8')).hexdigest()
    print("SHA-256 hash:", hash_str)
    hash_salt_str = f"{hash_str}{salt}"
    print("Hash with salt appended:", hash_salt_str)
    checksum = encrypt(hash_salt_str, key)
    print("Encrypted checksum:", checksum)
    return checksum
class get_checksum_hash:
    @classmethod
    def get_hash_string(cls,sadad_checksum_array,secret_key,merchant_id):

        sadad__checksum_data = {
            'postData': sadad_checksum_array,
            'secretKey': secret_key
        }

        # Trim spaces and create final post data
        sadad_checksum_array1 = {}
        for key, value in sadad_checksum_array.items():
            if key == 'checksumhash':
                continue
            if isinstance(value, list):
                sadad_checksum_array1['productdetail'] = [
                    {k: str(v).strip() for k, v in item.items()} for item in value
                ]
            else:
                sadad_checksum_array1[key] = str(value).strip()

        sadad__checksum_data['postData'] = sadad_checksum_array1
        sadad__checksum_data['secretKey'] = secret_key

        # Ensure consistent JSON encoding
        sadad_checksum_data_str = json.dumps(sadad__checksum_data, separators=(',', ':')).replace("/", "\\/")

        # Generate checksum
        checksum = get_checksum_from_string(sadad_checksum_data_str, secret_key + str(merchant_id))# "9288463")
        print("Generated Checksum:", checksum)

        return checksum

