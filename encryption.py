
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as pad
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import pickle


def encryption(path_symmetric_key, secret_key, inicial_file, encrypted_file):
    with open(path_symmetric_key, mode='rb') as key_file:
        content = key_file.read()
    with open(secret_key, 'rb') as pem_in:
        private_bytes = pem_in.read()
    private_key = load_pem_private_key(private_bytes, password=None, )
    dc_symmetric_key = private_key.decrypt(content, pad.OAEP(mgf=pad.MGF1(algorithm=hashes.SHA256()),
                                                             algorithm=hashes.SHA256(), label=None))
    with open(inicial_file, 'rb') as start_text:
        text = start_text.read()
    padder = padding.ANSIX923(64).padder()
    padded_text = padder.update(text) + padder.finalize()
    iv = os.urandom(8)
    cipher = Cipher(algorithms.IDEA(dc_symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    with open(encrypted_file, 'wb') as c_file:
        pickle.dump([iv, c_text], c_file)
