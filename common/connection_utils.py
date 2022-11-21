import json


def read_message(connection):
    data = bytearray()
    while True:
        try:
            data += connection.recv(1024)
        except Exception as error:
            print(error)
        try:
            message = json.loads(data)
        except json.JSONDecodeError:
            pass
        except UnicodeDecodeError:
            pass
        else:
            break
    #print(f'get: {message}')
    return message
