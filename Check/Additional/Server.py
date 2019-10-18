import socket

class Server:
    def __init__(self):
        self.host = ''
        self.serv = socket.socket()
        self.serv.bind((self.host, 8080))
        self.conn = ''
        self.client =''

    def connect(self):
        self.serv.listen(1)
        self.conn, self.client = self.serv.accept()
        print("Connected to {}".format(self.client[0]))

    def recv_img(self, size):
        size_limit = 9500
        data = b''
        ref = 0
        for i in range(size_limit, size, size_limit):
            data += self.conn.recv(i-ref)
            self.conn.send(b'\r\n')
            ref = i
        data += self.conn.recv(size_limit-ref)
        self.conn.send(b'\r\n')
        file = open('img.jpg', 'wb+')
        file.write(data)
        file.close()

    def recv_txt(self, size=2048):
        return self.conn.recv(size).decode()

    def send_txt(self, txt=''):
        self.conn.send(txt.encode('utf-8'))

