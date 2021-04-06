import re


def insert_payload(raw_src, key, payload_loader_template, payload_loader_output):
    raw_file = open(raw_src, 'rb')

    raw_data = raw_file.read()

    raw_file.close()

    data = []

    for b in raw_data:
        data.append(hex(b))

    array_string = ', '.join(data)

    deployer_code = open(payload_loader_template, 'r')

    initial_code = deployer_code.read()

    deployer_code.close()

    final_code = re.sub('__CODE_HERE__', array_string, initial_code)
    final_code = re.sub('__KEY_HERE__', key, final_code)

    final_src = open(payload_loader_output, 'w')

    final_src.write(final_code)

    final_src.close()
