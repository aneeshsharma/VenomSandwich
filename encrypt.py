import sys


def encrypt(src_filename, dest_filename, key):
    plain_text = open(src_filename, 'rb').read()
    key = bytes(key, 'utf-8')
    len_key = len(key)
    encoded = []
    for i in range(0, len(plain_text)):
        encoded.append(plain_text[i] ^ key[i % len_key])
    open(dest_filename, 'wb').write(bytes(encoded))
