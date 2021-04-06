import subprocess as sb


def compile_code(src_code, output_file):
    compiler = sb.Popen(["x86_64-w64-mingw32-g++", src_code,
                         '-o', output_file,  '-static', '-lpthread'])

    if compiler.wait() != 0:
        return False
    return True
