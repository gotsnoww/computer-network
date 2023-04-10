from socket import *
import json

serverName = '127.0.0.1'
serverPort = 12000

#사용자 이름 입력
print('TCP 기반 에코 채팅 프로그램')
name = input("[이름] : ")
print()

while True:
    #소켓 생성
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #옵션 선택 기능, option값이 정수가 아닐 경우를 찾아내기 위해 float 사용
    option = float(input("1. 일반적인 에코 메시지\n"
                    +"2. 모든 메시지를 소문자로 에코\n"
                    +"3. 모든 메시지를 대문자로 에코\n"
                    +"4. 종료\n"
                    +"옵션을 선택하세요: "))

    #에코 할 메시지 입력
    message = input("[메시지 입력] : ")

    #Request packet (client -> server)
    packet = {
        '이름' : name,
        '메시지' : message,
        '옵션' : option
    }

    #패킷 전송 기능
    json_packet = json.dumps(packet)
    clientSocket.send(json_packet.encode('utf-8')) #클라이언트 패킷 전송

    #option의 값이 1, 2, 3, 4 이외의 숫자라면 else부분 실행(오류 검출)
    #else 부분에서 정수가 아닌 숫자를 찾아내기위해 is_integer() 함수 사용
    if option.is_integer() and 1 <= option <= 4:
        AfterMessage = clientSocket.recv(1024) #전달 받은 서버 패킷 저장
        print('[에코된 메시지] : ', AfterMessage.decode(), '\n\n') #패킷 메시지 출력

    else: #오류 메시지를 패킷으로 받고 출력
        error_packet = {}
        json_error_packet = clientSocket.recv(1024).decode()
        error_packet = json.loads(json_error_packet)
        st_code = error_packet['st_code']
        error_msg = error_packet['error_msg']
        print('ERROR:', st_code, ',', error_msg, '\n\n')

    clientSocket.close()