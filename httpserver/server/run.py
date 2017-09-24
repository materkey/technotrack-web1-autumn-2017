# -*- coding: utf-8 -*-
import socket
import os


def get_response(request):
    if (request == ''):
        return ''
    strokes = request.split('\r\n')
    command = strokes[0].split()[0]
    path = strokes[0].split()[1]
    request_version = strokes[0].split()[2]
    status = '200 OK'
    text = ''
    header = dict()
    strokes = strokes[1:]
    for str in strokes:
        if (len(str.split(':')) > 1):
            header[str.split(':')[0]] = str.split(':')[1]
    if (command != 'GET'):
        status = '405 Method Not Allowed'
    if (path == '/'):
        text = 'Hello mister!\nYou are: ' + header['User-Agent']
    elif (path.split('/')[1] == 'media'):
        if (path == '/media/' or path == '/media'):
            text  = '<br>'.join(os.listdir('files'))
        else:
            try:
                file = open('./files/' + path.split('/')[2], 'r')
                text = file.read()
            except IOError:
                text = 'File not found'
                status = '404 Not Found'
    elif (path == '/test' or path == '/test/'):
        text = request.replace('\n', '<br>')
    else:
        status = '404 Not Found'
        text = 'Page not found'
    return request_version + ' ' + status + '\r\nContent-Type: text/html\r\n\r\n' + text


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # Привязка сокета к localhost:8000
server_socket.listen(0)  # Готовность прянимать connect() от клиентов

print 'Started'

while True:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # Вывод адреса клиента
        request_string = client_socket.recv(2048)  # Получение до 2048 байт от клиента
        print request_string
        client_socket.send(get_response(request_string))  # Отправка ответа от сервера
        client_socket.close()
    except KeyboardInterrupt:  # Обработка нажатия клавиш прерывания
        print 'Stopped'
        server_socket.close()  # Остановка операций сокетом сервера и освобождение ресурсов
        exit()
