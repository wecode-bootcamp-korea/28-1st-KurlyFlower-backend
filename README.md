# kurlyflower 프로젝트

### 마켓컬리 백엔드 클론코딩 프로젝트입니다.

### 이커머스 사이트의 필수 기능들을 구현했습니다.

### 개발된 API는 프론트엔드 서버와 연동되어 실제 운영중입니다.

<br>

## 🚀 개발 인원 및 기간

- 개발 기간 : 2021/12/27 ~ 2022/1/7 (2주간)
- 개발 인원 : 프론트엔드 3명, 백엔드 2명
- [프론트 github 링크](https://github.com/wecode-bootcamp-korea/westagram-frontend)

<br>

## 📍 데모 영상

![kurly2_final](https://user-images.githubusercontent.com/50139787/148687461-6ffc6500-3a1d-4898-8c61-da06e43a9a9d.gif)

- [컬리플라워 프로젝트 링크 바로가기](http://kurlyflower.s3-website.ap-northeast-2.amazonaws.com/)

<br>

## 🛠️ 기술스택

- Language : python3
- Framework : Django
- Database : MySQL
- Infra : AWS (EC2, RDS)

<br>

# ERD

![kurlyflower수정-1](https://user-images.githubusercontent.com/50139787/148689923-f91f787f-4bc6-40f5-b580-4f21451ac12f.jpg)

### 이찬주

- Mission 1 | 모델링

  ManyToMany, OneToMany 관계를 유의하여 ERD를 작성. 확장성을 고려해 이미지 테이블을 따로 두고, 요구사항에 맞게 데이터 베이스 모델 설계.

- Mission 2 | 로그인 기능

  password는 bcrypt를 이용해 유효 값을 확인하고, 로그인 성공시 secret key와 해시 알고리즘을 이용해 jwt 토큰을 발행. Decorator를 구현하여 각 엔드포인트에 적용.

- Mission 3 | 메인페이지

  데이터 중심의 api를 구성하고 페이지 스크롤시에 제한된 범위 안에 있는 객체만을 프론트엔드에 전달.

- Mission 4 | 장바구니 (create, update, delete)

  REST하게 엔드포인트를 구성하고 각 목적에 맞는 메소드를 활용해 자원을 관리. 장고 ORM을 활용해 적절한 쿼리 생성.

- Mission 5 | AWS 서버 배포

  aws EC2 인스턴스와 RDB 데이터베이스를 통해 배포. ssh를 통해서 원격서버에 접속하는 방법을 이해함. 데몬 프로그램으로 실행해 쉘을 꺼도 서버가 자동으로 실행되도록 함. nginx 웹서버를 앞 단에 띄워 보안성을 고려했고 리버스 프록시 기능을 이용해 8000포트를 숨김.

  ![aws 네트워크 구성도](https://user-images.githubusercontent.com/50139787/148691845-8d6cb7be-4dd5-4328-a8ed-6e683c6ca2bd.jpg)

<br>

### 장민욱

- Mission 1 | 프로젝트 초기 세팅

  Django 프로젝트를 생성하고, 초기 개발 환경을 구성
  .gitignore 파일을 생성하고, Git 버전 관리에서 제외할 파일(민감한 정보 등)을 지정하였다.
  Branch 를 생성하고, 기능별로 코드를 관리
  Github Repository 를 생성하고 로컬의 Git 과 연동
  <br>

- Mission 2 | 회원 가입

  re.match 모듈을 이용하여 사용자로 부터 입력받은 값을 처음부터 시작해서 작성한 정규식 패턴과 일치하는지 유효성 검사 진행(ID, PASSWORD, EMAIL)
  ValidationError를 이용하여 서로 다른 유효성 검사에 맞게 에러메세지 반환
  bcrypt 라이브러리 이용하여 패스워드 암호화
  <br>

- Mission 3 | 상세페이지

  상세페이지에 맞는 데이터값을 ORM의 쿼리문을 이용(get,filter,first), 정참조와 역참조를 활용하여 연결된 데이터 조회
  <br>

- Mission 4 | 장바구니(READ)

  로그인한 회원의 장바구니 목록을 ORM의 쿼리문을 이용(get,filter,first), 정참조와 역참조를 활용하여 연결된 데이터 조회

<br>

# API document

- 백엔드에서 개발한 API는 프론트엔드와 커뮤니케이션을 위해 포스트맨으로 문서화하여 공유했습니다.
- 프론트엔드는 각 엔드포인트와 키 값을 문서를 통해 확인할 수 있고 커뮤니케이션 비용을 절감할 수 있습니다.

![컬리플라워-최종발표 014](https://user-images.githubusercontent.com/50139787/148512490-12f3edc9-c53b-4b5b-bbd5-d38764d3677e.jpeg)

## Trello

- 트렐로를 이용해 모든 업무들을 세분화 시켜 하나의 티켓으로 만들었습니다.
- 전체 프로세스를 크게 앞으로 해야 할 것들(Backlog), 이번주에 해야 할 것들(This Week), 현재 진행 중인 것들(In Progress), 완료한 것들(Done) 이렇게 네 가지 카테고리로 나눠서 각각의 티켓을 과정에 따라 하나씩 이동 시키며 프로젝트의 모든 일정과 업무를 관리했습니다.

<img width="1440" alt="스크린샷 2021-12-30 오후 9 42 25" src="https://user-images.githubusercontent.com/50139787/148688356-1a27857d-39fa-4e30-b991-4f7a3a8ffcc4.png">

<br>

## Scrum

> Planning Meeting

- 매 주 월요일 이번 sprint에 진행할 업무에 대한 전반적인 기획을 관리
- 기본적인 기능 구현에 초점을 두고, 모두 구현이 되었다면 추가적으로 기능을 하나씩 추가하도록 계획
- 필수 구현 기능 : 회원가입, 로그인, 메인페이지, 카테고리페이지, 상세페이지, 장바구니
- 추가 구현 기능 : 구매하기, 멤버쉽

<br>

> Daily Standup Meeting

- 매일 아침 팀원들이 정해진 시간에 모여 어제 한일, 오늘 할일, 블로킹 포인트, 새로 배운 내용을 모든 참여자가 보고가 아닌 수평적으로 공유 차원에서 진행하였다.
- 서로의 진행 상황을 알 수 있었고, 블로킹 포인트에 대해 팀원들끼리 해결 방법을 찾아보았다.

<br>

> Retrospective Meeting

- 프로젝트의 처음 시점으로 돌아가서 진행된 프로젝트의 흐름을 따라가며 변곡점들에 어떤 일들이 일어났는지 살펴보는 시간을 갖음
- 좋았던 부분, 아쉬웠던 부분 등을 정리
- 문제가 발생한 원인을 파악하고 파악된 원인들을 어떻게 개선해나갈 수 있을지 의견 공유
