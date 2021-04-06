def encrypt(src_filename, dest_filename, key):
    src_file = open(src_filename, 'rb')
    dst_file = open(dest_filename, 'wb')

    dst_file.write(src_file.read())
