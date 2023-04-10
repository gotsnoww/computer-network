from socket import *
import json

#소켓 생성
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)
print('서버-클라이언트 연결 준비 완료.')

packet = {}
error_packet = {}

while True:
    #클라이언트-서버 연결
    connectionSocket, addr = serverSocket.accept()

    #클라이언트 패킷 받음
    json_packet = connectionSocket.recv(1024).decode('utf-8')
    packet = json.loads(json_packet) #패킷 풀기

    name = packet['이름']
    message = packet['메시지']

    #에코 옵션에 따라 메시지 처리
    if packet["옵션"] == 1:  #일반적인 에코
        print('Before: ', '[', name, ']: ', message)
        print('After: ', '[', name, ']: ', message, '\n')
        connectionSocket.send(message.encode())
    elif packet["옵션"] == 2:  #소문자로 에코
        AfterMessage = message.lower()
        print('Before: ', '[', name, ']: ', message)
        print('After: ', '[', name, ']: ', AfterMessage, '\n')
        connectionSocket.send(AfterMessage.encode())
    elif packet["옵션"] == 3:  #대문자로 에코
        AfterMessage = message.upper()
        print('Before: ', '[', name, ']: ', message)
        print('After: ', '[', name, ']: ', AfterMessage, '\n')
        connectionSocket.send(AfterMessage.encode())
    elif packet["옵션"] == 4:  #종료
        break
    
    
    #오류 메시지 출력 기능
    else : #else 부분에서 정수가 아닌 숫자를 찾아내기위해 is_integer() 함수 사용
        if packet["옵션"].is_integer and packet["옵션"] < 1: #1보다 작은 정수 입력
            error_packet['st_code'] = 403
            error_packet['error_msg'] = 'option input error: integer less than 1'
            json_error_packet = json.dumps(error_packet)
            connectionSocket.send(json_error_packet.encode())
        elif packet["옵션"].is_integer and packet["옵션"] > 4: #4보다 큰 정수 입력
            error_packet['st_code'] = 404
            error_packet['error_msg'] = 'option input error: integer greater than 4'
            json_error_packet = json.dumps(error_packet)
            connectionSocket.send(json_error_packet.encode())
        else : #정수가 아닌 숫자 입력
            error_packet['st_code'] = 407
            error_packet['error_msg'] = 'option input error: non-integer'
            json_error_packet = json.dumps(error_packet)
            connectionSocket.send(json_error_packet.encode())

    connectionSocket.close()