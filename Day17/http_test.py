"""
http请求 响应示例
"""
from socket import *

sockfd = socket()
sockfd.bind(('0.0.0.0', 7767))
sockfd.listen(5)

connfd, addr = sockfd.accept()
print('Connect from', addr)

data = connfd.recv(1024).decode()
print(data)

#将数据组织为响应格式
# response="""HTTP/1.1 200 OK
# Content-Type:text/html;charset=UTF-8
# Content-Length:109\r\n
#
# This is test surprise mother fuck
# \r\n
# 搞鸡儿
# """
with open('cat.jpg', 'rb') as f:
    data=f.read()
response="HTTP1.1 200 OK\r\n"
response+="Content-Type:image/jpeg\r\n"
response+='\r\n'
response=response.encode()+data


#向浏览器发送内容
connfd.send(response)

connfd.close()
sockfd.close()
