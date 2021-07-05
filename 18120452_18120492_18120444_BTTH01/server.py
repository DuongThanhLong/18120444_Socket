from socket import *
import codecs

s = socket(AF_INET, SOCK_STREAM)
s.bind(("", 80))
s.listen(1)
code = ""
while True:
    conn, addr = s.accept()
    temp = conn.recv(32768)
    conn.setblocking(False)
    request = temp.decode('utf8')
    try:
        if request != "":
            header_part = request.split('\r\n\r\n')[0]
            request_line = header_part.split('\r\n')[0]
            method = request_line.split(' ')[0]
            link = request_line.split(' ')[1]
            if link != '/':
                if link.split('.')[1] == "html":
                    link = link.replace("/", "")
                    code = '200 OK\n'
                    file = codecs.open(link, "r", "utf8")
                    response = file.read()
                else:
                    code = '204 No content'
            else:
                code = '301 Moved permanently\nLocation: index.html'

            if method == 'POST':
                data_part = request.split('\r\n\r\n')[1]
                user, pwd = data_part.split('&')
                user = user.split('=')[1]
                pwd = pwd.split('=')[1]
                if user == 'admin' and pwd == 'admin':
                    code = '200 OK\n'
                    file = codecs.open(link, "r", "utf8")
                    response = file.read()
                else:
                    code = '301 Moved permanently\nLocation: 404.html'
            conn.sendall(bytes('HTTP/1.1 ', "utf8"))
            conn.sendall(bytes(code, "utf8"))
            if code.split(' ')[0] == '200':
                conn.sendall(bytes('Content-Type: text/html\n', "utf8"))
                conn.sendall(bytes('\n', "utf8"))
                conn.sendall(bytes(response, "utf8"))
        conn.close()
    finally:
        conn.close()
s.close()