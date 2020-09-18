import re
from socket import *
# from multiprocessing import Process,Queue
from select import *
# import os

class WebSeerver():
    def __init__(self, host, port, html):
        self.host=host
        self.port=port
        self.html=html
        self.get_socket()
        self.start()

    def get_socket(self):
        self.sockfd=socket()
        self.get_bind()



    def get_bind(self):
        self.sockfd.bind((self.host,self.port))
        self.sockfd.setblocking(False)
        


    def start(self):
        self.sockfd.listen(5)
        self.get_epoll()

    def get_epoll(self):
        map={}
        self.p=epoll()

        self.p.register(self.sockfd,EPOLLIN)
        map[self.sockfd.fileno()]=self.sockfd
        while True:
            events=self.p.poll()
            for fd,event in events:
                if fd==self.sockfd.fileno():
                    connfd,addr=map[fd].accept()
                    print('Connect from',addr)
                    connfd.setblocking(False)
                    map[connfd.fileno()]=connfd
                    self.p.register(connfd,EPOLLIN)

                elif event==EPOLLIN:
                    data=map[fd].recv(1024).decode()
                    print(data)
                    if not data:
                        self.p.unregister(fd)
                        map[fd].close()
                        del map[fd]
                        continue
                    request=data.split(' ')[1]
                    self.do_request(map[fd],request)
                # elif event==POLLOUT:
                #     map[fd].send()

    def do_request(self, connfd,request):
        # dir=os.listdir('./static')
        if request =='/':
            filename=self.html+'/index.html'

        else:
            filename=self.html+request
        #打开失败说明文件不存在
        try:
            file=open(filename,'rb')
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html;charset=UTF-8\r\n"
            response += "Content-Length:%d\r\n"%(len(data))
            response += '\r\n'
            response = response.encode() + data
            file.close()
        except:
            response = """HTTP/1.1 404 Not Found
Content-Type:text/html

<h1>Sorry...</h1>
            """.encode()
            # connfd.send(response)

        finally:
            connfd.send(response)



if __name__ == '__main__':
    httpd=WebSeerver(host='0.0.0.0',port=8000,html='./static')
    httpd.start()


# result=re.match(r"[A-Z]+\s+(/\S*)","GET /favicon.ico HTTP/1.1")
# print(result.group(1))