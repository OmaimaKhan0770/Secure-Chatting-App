from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import base64

# ================= AES =================
aes_key = b'1234567890abcdef'


def encrypt_aes(msg):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()



def decrypt_aes(data):
    raw = base64.b64decode(data)
    nonce = raw[:16]
    ciphertext = raw[16:]

    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()


# ================= DES =================
des_key = b'8bytekey'


def encrypt_des(msg):
    cipher = DES.new(des_key, DES.MODE_ECB)
    padded = pad(msg.encode(), 8)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode()



def decrypt_des(data):
    cipher = DES.new(des_key, DES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(data))
    return unpad(decrypted, 8).decode()


# ================= RSA + AES HYBRID =================
rsa_key = RSA.generate(2048)
public_key = rsa_key.publickey()
private_key = rsa_key



def encrypt_hybrid(msg):
    # AES encryption
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(msg.encode())

    # RSA encrypt AES key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    # FIX: use fixed-length prefix (RSA-2048 always produces 256 bytes)
    # instead of b'||' separator which can randomly appear in binary RSA output
    final = encrypted_key + cipher_aes.nonce + ciphertext
    return base64.b64encode(final).decode()



def decrypt_hybrid(data):
    raw = base64.b64decode(data)

    # FIX: RSA-2048 encrypted key is always exactly 256 bytes
    encrypted_key = raw[:256]
    rest = raw[256:]

    # decrypt AES key using RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_key = cipher_rsa.decrypt(encrypted_key)

    nonce = rest[:16]
    ciphertext = rest[16:]

    cipher_aes = AES.new(decrypted_key, AES.MODE_EAX, nonce=nonce)
    return cipher_aes.decrypt(ciphertext).decode()