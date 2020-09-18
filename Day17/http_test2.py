from socket import *
sockfd=socket()
sockfd.bind(('0.0.0.0',4366))
sockfd.listen(5)

while True:
    connfd,addr=sockfd.accept()
    print('Connect from',addr)
    data=connfd.recv(1024*10).decode()
    if not  data:
        connfd.close()
        continue
    data_list=data.split(' ')
    # print(data_list[1:2])

    if data_list[1]=='/first.html':
        with open('first.html','rb') as f:
            data=f.read()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html;charset=UTF-8\r\n"
        response += '\r\n'
        response = response.encode() + data

        connfd.send(response)
    else:
        response = """HTTP/1.1 404 Not Found
        Content-Type:text/html

""".encode()
        connfd.send(response)
        # continue

sockfd.close()