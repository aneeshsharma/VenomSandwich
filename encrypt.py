import sys


def encrypt(src_filename, dest_filename, key):
    src_file = open(src_filename, 'rb')
    dst_file = open(dest_filename, 'wb')
    key = int(ord(key))

    src_data = src_file.read()

    dst_data = b''

    for s in src_data:
        dst_data += bytes(chr(s ^ key), 'UTF-8')

   # print(enc_string)
    dst_file.write(dst_data)
