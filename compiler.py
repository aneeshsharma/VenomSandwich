import subprocess as sb


def compile_code(src_code, output_file):
    windres = sb.Popen(["x86_64-w64-mingw32-windres",
                        "icon.rc", "-O", "coff", "-o", "icon.res"])

    if windres.wait() != 0:
        print('Error creating icon resource')
        return False

    compiler = sb.Popen(["x86_64-w64-mingw32-g++",
                         "-c", src_code,
                         '-o', "loader.o"
                         ]
                        )

    if compiler.wait() != 0:
        print('Error compiling object')
        return False

    compiler = sb.Popen(["x86_64-w64-mingw32-g++",
                         "-o", output_file,
                         "loader.o",
                         "icon.res",
                         "-static",
                         "-lpthread"])

    if compiler.wait() != 0:
        print('Error creating exe')
        return False

    return True
