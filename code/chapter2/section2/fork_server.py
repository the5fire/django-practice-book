# coding:utf-8

import errno
import os
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> from the5fire 《Django企业开发实战》</h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sat, 10 jun 2017 01:01:01 GMT',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    pid = os.fork()  # 产生一个新的子进程
    if pid:  # 是否为父进程
        return

    # 子进程继续执行
    print(conn, addr)
    import time
    time.sleep(10)
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print('request handle by pid:', os.getpid())
    print(request)
    conn.send(response.encode())
    conn.close()


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(5)
    serversocket.setblocking(0)
    print('http://127.0.0.1:8000')

    try:
        while True:
            try:
                conn, address = serversocket.accept()
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise
                continue
            handle_connection(conn, address)
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
