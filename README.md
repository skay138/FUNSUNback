# FunSun: 즐거운 펀딩 플랫폼

FunSun은 상대방의 취향과 필요성을 고려하여 정말 받고싶은 선물을 받을 수 있도록 친구들이 함께 서포트하는 플랫폼입니다. 크라우드 펀딩의 개념을 도입하여 여러 사용자들이 함께 모여 선물을 구매하고 불필요한 비용을 줄이는 서비스를 제공합니다.

## 상세 설명
해당 프로젝트는 FUNSUN 플랫폼(https://github.com/FUNFUNSUN/funsunfront) 의 BACKEND 서버입니다.

http://projectsekai.kro.kr:5000/swagger/ 에서 API를 확인할 수 있습니다.



## 사용 기술

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

## 깨달은 점
교수님의 조언으로 이번 BACKEND 프로젝트에서는 JWT를 적용시켜 보기로 했습니다. JWT가 막연하게 데이터를 암호화/복호화 하며 송수신하는 기술이라 생각했었는데, 공부를 하며 유저인증과 관련된 기술이라는 사실을 알게 되었습니다. 첫 로그인 시 해당 유저에 대해 accessToken과 refreshToken을 발행하고, 이를 response 데이터에 넣어주면 FRONT에서는 토큰정보를 Local Storage(flutter_secure_storage)에 저장해 두었다가 API호출 시 header에 토큰을 넣어 보냅니다. BACKEND에서는 그 토큰이 유효한지만 검증하여 유저에 대한 인증이 이루어지게 됩니다. 이를 통해 API호출 시 요청하는 유저가 누구인지  DB로의 I / O 없이 알 수 있으며, 자동로그인 시스템을 구현하는데도 적용해 볼 수 있었습니다. JWT를 적용하며 BACKEND서버와 DB서버를 분리해보고 싶었기에 AWS RDS와 MySQL을 이용해봤으나, Free Tier를 이용해서인지 데이터 호출이 너무 느려서 테스트만 해보고 현재는 BACKEND 서버안에 Django 내장 DB를 이용하고 있습니다. 그 밖에 paging 처리를 하여 게시글 리스트를 호출하는 함수에서는 페이지에 따라 8개의 게시글씩 반환하거나, Kakao Pay / Kakao Login api를 구현했습니다.

## MEMO

### 왜 Kakao Pay API를 사용하였는가?

상용화를 감안한다면, 카카오페이는 펀딩 플랫폼에는 허가가 떨어지지 않기 때문에 그리 좋은 선택은 아니었습니다. 부트페이등 다른 PG API를 사용하는 게 더 적절했다고 생각합니다. 그럼에도 카카오페이를 사용해본 이유는 다른 PG API보다 한단계 절차가 더 복잡하다고 들어서 입니다. 어려운 API를 사용하여 적용시킬 수 있다면 다른 API도 쉽게 이용할 수 있을거라는 판단에 상용화에는 적합하지 않을 수 있지만 연습을 위해 카카오페이를 사용했습니다.
