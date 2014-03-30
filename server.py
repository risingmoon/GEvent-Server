import socket
from os.path import isdir, isfile, exists
from os import listdir
from email.utils import formatdate
from mimetypes import guess_type
from gevent.server import StreamServer
from gevent.monkey import patch_all
ADDRESS, PORT, BUFFER_SIZE = '127.0.0.1', 8000, 4092


def recv(conn, buffer_size=4092):
    """parses buffer strings into response"""
    response = ''
    while True:
        msg_part = conn.recv(buffer_size)
        response += msg_part
        if len(msg_part) < buffer_size:
            conn.shutdown(socket.SHUT_RD)
            return response


def check_uri(uri):
    path_list = ["webroot"]
    path_list.extend([w for w in uri.split('/')
                      if len(w) > 0])
    path = '/'.join(path_list)
    #determine if uri path maps to webroot
    if not exists(path):
        raise Error404('FILE NOT FOUND')
    else:
        return path


def map_uri(uri):
    """Maps URI onto webroot system"""
    path = check_uri(uri)
    #uri maps onto a folder directory
    if isdir(path):
        list_dir = ['Current Path: %s \n' % (path)]
        list_dir.extend(listdir(path))
        body = "\r\n".join(list_dir)
        return (body, 'text/plain')
    #uri maps onto a file source
    elif isfile(path):
        with open(path, 'rb') as file_handler:
            body = file_handler.read()
        return (body, guess_type(path)[0])
    else:
        msg = "SOMEBODY CALL 911, SERVER BURNING ON THE DANCE FLOOR!"
        raise Error500(msg)


def build_response(message, content_type='None', code=200):
    """Builds HTTP response based on HTTP Statuse"""
    header = []
    if code == 200:
        header.append("HTTP/1.1 200 OK")
        header.append('Content-Type: %s' % content_type)
        header.append('Content-Length:%s' % str(len(message)))
        header.append("Date:%s" % formatdate(usegmt=True))
    else:
        header.append("HTTP/1.1 %s" % code)
        header.append(
            'Content-Type:text/plain; Char-Type:None')

    return "\r\n".join(header) + '\r\n\r\n' + message


def parse_request(message):

    request = message.split('\r\n', 1)[0]
    method, uri, protocol = request.split()
    if method != 'GET':
        raise Error405("METHOD NOT ALLOWED")
    else:
        return map_uri(uri)


def server(connection, address):
    """Setups and continually runs until Keyboard Interrupt"""

    while True:
        response = ''
        try:
            message = recv(connection)
            body, content_type = parse_request(message)
            response = build_response(body, content_type)
        except Error404:
            response = build_response("FILE NOT FOUND", 404)
        except Error405:
            response = build_response("METHOD NOT ALLOWED", 405)
        except ValueError as e:
            print e.message
        except KeyboardInterrupt:
            print "SERVER TERMINATED"
        finally:
            connection.sendall(response)
            connection.shutdown(socket.SHUT_WR)


class Error404(Exception):
    pass


class Error405(Exception):
    pass


class Error500(Exception):
    pass
if __name__ == "__main__":
    patch_all()
    server = StreamServer((ADDRESS, PORT), server)
    print('Starting echo server on port 80000')
    server.serve_forever()
