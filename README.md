
# FunSun: 즐거운 펀딩 플랫폼
![KakaoTalk_20230822_103135088](https://github.com/skay138/FUNSUNback/assets/102957619/ccfd29c5-6b32-410c-af4f-aee707bb2351)
FunSun은 상대방의 취향과 필요성을 고려하여 정말 받고싶은 선물을 받을 수 있도록 친구들이 함께 서포트하는 플랫폼입니다. 크라우드 펀딩의 개념을 도입하여 여러 사용자들이 함께 모여 선물을 구매하고 불필요한 비용을 줄이는 서비스를 제공합니다.

## 요약
해당 프로젝트는 FUNSUN 플랫폼(https://github.com/FUNFUNSUN/funsunfront) 의 BACKEND 서버입니다.

http://projectsekai.kro.kr:5000/swagger/ 에서 API를 확인할 수 있습니다.

### 기술 설명
- OracleCloud에 ubuntu 운영체제로 nignx와 uWSGI를 이용하여 Backend 서버 구현
- rest_framework_simplejwt를 이용하여 DB의 유저id값을 필터링하여 jwt 적용
- 테이블별로 app으로 나누어 관리
- 라우트마다 하나의 클래스로 CRUD를 함수 컴포넌트형태로 API 구현
- 전체공개, 친구공개, 팔로워, 팔로잉 상태에 따라 게시글 목록을 필터링하여 전송하는 4개의 API 구현
- Paginator를 이용하여 게시글 페이징 적용
- response에 http status code(200, 201, 204, 400, 401) 이용
- request와 response를 이용한 데이터 송수신
- 이미지 등 media data 핸들링
- 결제정보 처리를 위한 json데이터 생성, 수정, 삭제
- django admin을 활용하여 관리 페이지 구현
- swagger를 활용하여 API 문서화

## 🎞️ 시연 영상

  ### [https://youtu.be/yqIR-TgG6qE](https://youtu.be/yqIR-TgG6qE)

## 🌉 기획 배경

한국인의 대다수가 카카오톡을 사용하는 요즘, 생일날에 우리는 기프티콘을 주고 받곤 합니다. 좋아하는 음료나 음식을 보내주기도 하고 우스꽝스러운 선물을 보냅니다. 하지만 커피를 선호하지 않는 사람에게 스타벅스 기프티콘을 보내는 등 종종 우리는 만족스럽지 못한 선물을 주고 받을 때도 있습니다. 또 진정 원하는 선물이 있더라도 가격이 부담스러울 때도 있습니다. 이것이 정말 아쉬운 점은 받은 선물의 총액이 그 선물을 상회할 때가 많다는 사실입니다. 이런 불편한 상황을 인지하고 저희 팀은 선물 펀딩 플랫폼을 기획하게 되었습니다. "FunSun"은 친구들이 모여 더욱 특별한 선물을 준비하는데 도움을 주는 펀딩 플랫폼입니다. 저희는 사용자들에게 간단하고 편리한 방식으로 선물을 공동으로 펀딩하고 나누는 기회를 제공합니다. 이 서비스를 통해 사용자들은 함께 모여 선물을 준비하며, 그 과정에서 더욱 의미 있는 연결과 감동을 느낄 수 있길 기대해봅니다.

## 📖 상세 내용


    
### 💁🏻‍♂️ 프로젝트 소개

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-04](https://github.com/skay138/FUNSUNback/assets/102957619/a083e5f1-07d8-4f79-9df2-84830c368be1)

### ⭐ 최종목표

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-05](https://github.com/skay138/FUNSUNback/assets/102957619/d41f0d92-0293-4435-bad8-ea79fc898169)

### ⌨️ 기획 상세

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-06](https://github.com/skay138/FUNSUNback/assets/102957619/df15c99a-028d-441d-9d6b-68074d8fd0f5)

### 🛠️ 개발환경

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-07](https://github.com/skay138/FUNSUNback/assets/102957619/695fe85a-0985-4673-b235-62719f49c315)

### 🔍 구조도

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-09](https://github.com/skay138/FUNSUNback/assets/102957619/f6b6827b-bb1b-4935-98f4-2006589ba636)

### ⛓️와이어프레임

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-10](https://github.com/skay138/FUNSUNback/assets/102957619/8e24125c-c1a3-4f97-970f-355b4b5bcf61)

### 📋 IA 설계

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-11](https://github.com/skay138/FUNSUNback/assets/102957619/8581a8f7-8c8b-414d-9751-1a7fa88f40c8)

### 👤 USER FLOW

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-12](https://github.com/skay138/FUNSUNback/assets/102957619/201c4fb9-8fb0-4079-b600-4b9ddaff6e73)

### 💾 ERD

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-13](https://github.com/skay138/FUNSUNback/assets/102957619/c6dfdf2a-f657-475d-b591-4651f51455ca)

### 💰 주요 API


![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-20](https://github.com/skay138/FUNSUNback/assets/102957619/79661825-0eb3-4458-9415-2aff87230f8d)

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-21](https://github.com/skay138/FUNSUNback/assets/102957619/971db3d0-fb04-4c39-abc0-94bc6483e4ae)

![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-22](https://github.com/skay138/FUNSUNback/assets/102957619/eeb09317-84a5-4e7f-a2a6-3724c90860fd)
    
![FunSun_%EC%8B%AC%ED%99%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_V2 2-23](https://github.com/skay138/FUNSUNback/assets/102957619/0033a801-d5b4-4c94-9e81-c5667dfd5d45)
    

## 💡 깨달은 점

 ### BACKEND

교수님의 조언으로 이번 BACKEND 프로젝트에서는 JWT를 적용시켜 보기로 했습니다. JWT가 막연하게 데이터를 암호화/복호화 하며 송수신하는 기술이라 생각했었는데, 공부를 하며 유저인증과 관련된 기술이라는 사실을 알게 되었습니다. 첫 로그인 시 해당 유저에 대해 accessToken과 refreshToken을 발행하고, 이를 response 데이터에 넣어주면 FRONT에서는 토큰정보를 Local Storage(flutter_secure_storage)에 저장해 두었다가 API호출 시 header에 토큰을 넣어 보냅니다. BACKEND에서는 그 토큰이 유효한지만 검증하여 유저에 대한 인증이 이루어지게 됩니다. 이를 통해 API호출 시 요청하는 유저가 누구인지  DB로의 I / O 없이 알 수 있으며, 자동로그인 시스템을 구현하는데도 적용해 볼 수 있었습니다. JWT를 적용하며 BACKEND서버와 DB서버를 분리해보고 싶었기에 AWS RDS와 MySQL을 이용해봤으나, Free Tier를 이용해서인지 데이터 호출이 너무 느려서 테스트만 해보고 현재는 BACKEND 서버안에 Django 내장 DB를 이용하고 있습니다. 그 밖에 paging 처리를 하여 게시글 리스트를 호출하는 함수에서는 페이지에 따라 8개의 게시글씩 반환하거나, Kakao Pay / Kakao Login api를 구현했습니다.

### FRONTEND

저번 프로젝트에서는 Provider 사용이 미흡한 점이 있어 이번 프로젝트에서는 데이터(변수)관리를 최대한 고려하며 코드를 작성했습니다.  직접 새로운 페이지를 작성하기 보다 이번 프로젝트에서는 API 호출 및 데이터 관리, 디버깅 및 오류 제어, 코드의 리팩토링에 좀 더 집중했습니다. 또한 FRONT를 담당했던 팀원 중 한명과 멘토-멘티식 협업을 진행하였고, 팀원의 코드리뷰 및 오류 해결을 도왔습니다. 처음에는 프로젝트 진행도가 더디더라도 갈수록 가속도가 붙는 경험을 할 수 있었습니다.

카카오페이 API 데모를 연결하는 데 있어 다소 어려움이 있었습니다. 처음에는 Kakao에 전달해야 하는 redirect url(approval URL)의 문제라고 생각하였으나 아니었고, 어떤 단계에서 문제가 생기는 건지 다이어그램을 그려보며 파악했습니다. 문제는 결제 진행 URL을 인 앱 브라우저로 실행하지 않고 앱의 밖(external view)에서 실행하였기 때문에 결제 후 브라우저로 돌아가는 것이 아닌 앱으로 돌아가 버려 승인 URL에서 pg_token을 받을 수가 없던 것이었습니다. 앱의 밖에서 URL을 실행한 이유는 인 앱 브라우저에서 실행 시 에러 화면이 뜨기 때문이었기에, 인 앱 브라우저의 오류를 해결해보기로 했습니다. 문제는 첫 redirect URL 접속 시 앱에서 바로 Kakao 결제를 진행하기 위해 indent 링크로 넘어가게 되는데, 이를 안드로이드에서 URL로 바로 인식할 수 없었기 때문이었습니다. 해결 방안을 모색하다 보니 이 문제는 flutter에서 직접 수정할 수 없다는 사실을 인지하였습니다. 따라서 android 폴더의 manifest.kt 에서 추가적인 메소드를 만들고, 이를 flutter에서 호출하여 URL을 android에 호환될 수 있게끔 수정해주었습니다.

## 📝 메모


### 왜 Kakao Pay API를 사용하였는가?

상용화를 감안한다면, 카카오페이는 펀딩 플랫폼에는 허가가 떨어지지 않기 때문에 그리 좋은 선택은 아니었습니다. 부트페이등 다른 PG API를 사용하는 게 더 적절했다고 생각합니다. 그럼에도 카카오페이를 사용해본 이유는 다른 PG API보다 한단계 절차가 더 복잡하다고 들어서 입니다. 어려운 API를 사용하여 적용시킬 수 있다면 다른 API도 쉽게 이용할 수 있을거라는 판단에 상용화에는 적합하지 않을 수 있지만 연습을 위해 카카오페이를 사용했습니다.
