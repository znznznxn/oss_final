# 채팅앱

# 구현 목표
###  본 프로젝트는 카카오톡을 목표로 클론 코딩을 진행한 프로젝트입니다. 회원가입 후 등록된 사용자와 친구를 맺은 뒤 1대1 채팅을 하는 것을 목표로 합니다.

# 구현 기능

* 회원가입, 로그인 기능
* 친구나 채팅방 클릭 시 채팅 시작하는 기능
* 실시간 채팅
* 친구 추가 기능
* 채팅방의 마지막 메시지를 보여주는 기능

# Reference
[1] https://fastapi.tiangolo.com/ko/ "FastAPI" 

# 지원 Operating Systems 및 실행 방법

## 지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :o:  |
| Linux  | :o: |
|MacOS  | :o:  |

## 실행 방법
### Windows

1. python3.9 이상의 버전을 설치한다
2. powershell 창에서 아래 pip3 library를 설치
```
> pip3 install fastapi[all]
> pip3 install sqlalchemy
> pip3 install fastapi_login
```
3. 라이브러리 설치 이후 python3 main.py를 실행하면 uvicorn이 돌면서 로컬 서버가 실행됨.
4. URL에 "localhost:8000"을 입력하면 로그인 화면이 뜨게됨.

### Linux & MacOs

1. python3.9 이상의 버전을 설치한다
2. terminal 창에서 아래 pip3 library를 설치
```
$ pip3 install fastapi[all]
$ pip3 install sqlalchemy
$ pip3 install fastapi_login
```
3. 라이브러리 설치 이후 python3 main.py를 실행하면 uvicorn이 돌면서 로컬 서버가 실행됨.
4. URL에 "localhost:8000"을 입력하면 로그인 화면이 뜨게됨.

### 🔔 로컬 서버로만 접속 가능
### 🔔 웹소켓으로 구현되었기에 세션이 달라야 다른 사용자로 접속 가능
### 🔔 추천 방법
- 본인이 사용하는 브라우저 외 다른 브라우저를 추가로 띄워 각각 접속
- 본인이 사용하는 브라우저의 기본 모드 창과 시크릿 모드 창을 띄워 각각 접속

# 실행 예시
![ezgif com-video-to-gif-converter](https://github.com/znznznxn/oss_final/assets/65123162/d5560a37-acf3-4cfa-b30a-24f211515a0d)

# 코드 설명(프론트엔드)
## login.html
### 로그인
- Function login: 아이디, 비번 데이터를 /token으로 post하여 사용자 인증 요청
### 회원가입
- Function register: 유저 정보 불러온 후 등록된 사용자인지 확인, 미등록된 경우 /register에 post하여 등록 요청

## friends.html
 친구 추가, 친구 목록 불러오기, 채팅 시작

## chatlist.html
- 채팅 목록 불러오기, 채팅 시작

## chatting.html
- 웹소켓으로 받은 메시지, 사용자와의 연관성 확인 후 수신 혹은 무시
### 채팅 불러오기
- Function get_chats, get_all_chats: 현재 채팅방의 채팅 불러오기
### 채팅 전송
- Function sendClick: 첫 채팅일 경우 방 생성 + 채팅 전송 및 기록 요청 + 마지막 메시지 업데이트 요청

# 코드 설명(백엔드)
## main.py
### 사용자 인증
- OAuth2 라이브러리를 사용하여 사용자 인증 메커니즘 삽입
  1. Def login: 로그인 정보 검증 및 쿠키 발급
  2. Def auth_exception_handler: 미인증된 사용자 확인 시 로그인 창으로 이동
  3. Def get_user: 사용자 확인

### 창 로딩 또는 데이터 수정 및 불러오기
- FastAPI 사용하여 각 URL+메소드 요청에 대한 응답
- **창 로딩**
  1. Def get_root: 친구 목록 창으로 리다이렉션
  2. Def get_friends, get_login, get_chatlist: 각 페이지 html 응답
  3. Def chat_start: 채팅방으로 이동
- **데이터 수정 및 불러오기**
  - 유저 관련
    1. Def register, get_users: 사용자 등록 및 등록된 사용자 목록 불러오기
    2. Def get_current_user: 현재 로그인된 사용자 불러오기
  - 친구 관련
    1. Def get_friends, add_friends: 친구 목록 불러오기 및 친구 맺기
  - 채팅 관련
    1. Class ConnectionManager, Def websocket_endpoint: 웹소켓 통신
    2. Def get_room, make_room: 방 정보 불러오기 및 방 생성
    3. Def update_room: 채팅방 마지막 메시지 업데이트
    4. Def get_chat, add_chat, get_chatlist: 채팅 불러오기, 채팅 추가, 채팅 목록 불러오기

## database.py
### DB 엔진 설정

## models.py
### 데이터베이스 테이블
- Class User: 이름, 비밀번호로 구성된 데이블 생성
- Class Friends: 친구 관계인 pair로 구성된 테이블 생성
- Class Header: 채팅방 정보로 구성된 테이블 생성
- Class Chat: 모든 채팅을 기록하는 테이블 생성

## schema.py
### DB와 호환되는 데이터 Format
- Class UserSchema: 이름, 비밀번호의 형태
- Class FriendSchema: 유저1, 2의 형태
- Class LastchatSchema: 채팅방 id, 마지막 메시지 내용의 형태
- Class HeaderSchema: 송신자, 수신자, 마지막 메시지 내용의 형태
- Class ChatSchema: 송신자 이름, 수신자 이름, 채팅방 id, 메시지 내용, 보낸 시간의 형태

# 미구현 기능
* 그룹 채팅
* 원격 서버
