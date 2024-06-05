# 채팅앱

# 구현 목표
###  본 프로젝트는 카카오톡을 목표로 클론 코딩을 진행한 프로젝트입니다. 회원가입 후 등록된 사용자와 친구를 맺은 뒤 1대1 채팅을 하는 것을 목표로 합니다.

# 구현 기능

* 회원가입, 로그인 기능
* 친구나 채팅방 클릭 시 채팅 시작하는 기능
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

# 실행 예시
<span style="color:red">동영상 업로드 시 gif로 변환 후 링크를 삽입</span>
<span style="color:red">아래 홈페이지 참고 : https://onlydev.tistory.com/15 </span>
![ezgif com-video-to-gif-converter](https://github.com/znznznxn/oss_final/assets/65123162/d5560a37-acf3-4cfa-b30a-24f211515a0d)
![example](https://github.com/RmKuma/oss_personal_project_phase1/assets/20412048/98ecfe0c-34c5-4592-86e9-defded705a36)

# 코드 설명
## main.py
### 

### 
 

# TODO List
* 그룹 채팅
