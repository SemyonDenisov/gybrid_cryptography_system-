from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as pad
import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding


def decryption(path_symmetric_key,secret_key, encrypted_file,decrypted_file):
    with open(path_symmetric_key, mode='rb') as key_file:
        content = key_file.read()
    print('symmetric_key was scanned')
    with open(secret_key, 'rb') as pem_in:
        private_bytes = pem_in.read()
    private_key = load_pem_private_key(private_bytes, password=None, )
    dc_symmetric_key = private_key.decrypt(content, pad.OAEP(mgf=pad.MGF1(algorithm=hashes.SHA256()),
                                                             algorithm=hashes.SHA256(), label=None))
    print('secret_key was scanned')
    with open(encrypted_file, 'rb') as c_file:
        scan_data = pickle.load(c_file)
    cipher = Cipher(algorithms.IDEA(dc_symmetric_key), modes.CBC(scan_data[0]))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(scan_data[1]) + decryptor.finalize()
    unpadder = padding.ANSIX923(64).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    with open(decrypted_file, 'wb') as dc_file:
        dc_file.write(unpadded_dc_text)
    print('data was decrypted and written')