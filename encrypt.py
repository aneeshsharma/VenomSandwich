import sys
def encrypt(src_filename, dest_filename, key):
    data = open(src_filename, 'rb').read()
    dst_file = open(dest_filename, 'w')
    key = str(key)
    l = len(key)
    output_str = ""
    for i in range(len(data)):
        current = chr(data[i])
        current_key = key[i % len(key)]
        output_str += chr(ord(current) ^ ord(current_key))
    enc_string = '{ 0x' + ', 0x'.join(hex(ord(x))[2:] for x in output_str) + ' };'  
   # print(enc_string)
    dst_file.write(enc_string)


#except:
#    print("File argument needed! %s " % sys.argv[0]) 
#    sys.exit()