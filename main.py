import argparse
from generation import generation
from encryption import encryption
from decryption import decryption

settings = {
    'initial_file': 'start_text.txt',
    'encrypted_file': 'encrypted_file.txt',
    'decrypted_file': 'decrypted_file.txt',
    'symmetric_key': 'symmetric_key.txt',
    'public_key': 'public_key.txt',
    'secret_key': 'secret_key.txt',
}

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-gen', '--generation', help='Запускает режим генерации ключей', action='store_true')
group.add_argument('-enc', '--encryption', help='Запускает режим шифрования', action='store_true')
group.add_argument('-dec', '--decryption', help='Запускает режим дешифрования', action='store_true')

args = parser.parse_args()
if args.generation:
    generation(settings['initial_file'], settings['secret_key'], settings['symmetric_key'])
else:
    if args.encryption:
        encryption(settings['symmetric_key'], settings['secret_key'], settings['initial_file'],
                   settings['encrypted_file'])
    else:
        decryption(settings['symmetric_key'], settings['secret_key'], settings['encrypted_file'],
                   settings['decrypted_file'])
