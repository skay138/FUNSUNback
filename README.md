
# FunSun: 즐거운 펀딩 플랫폼
![KakaoTalk_20230822_103135088](https://github.com/skay138/FUNSUNback/assets/102957619/ccfd29c5-6b32-410c-af4f-aee707bb2351)
FunSun은 상대방의 취향과 필요성을 고려하여 정말 받고싶은 선물을 받을 수 있도록 친구들이 함께 서포트하는 플랫폼입니다. 크라우드 펀딩의 개념을 도입하여 여러 사용자들이 함께 모여 선물을 구매하고 불필요한 비용을 줄이는 서비스를 제공합니다.

## 요약
해당 프로젝트는 FUNSUN 플랫폼(https://github.com/FUNFUNSUN/funsunfront) 의 BACKEND 서버입니다.

http://projectsekai.kro.kr:5000/swagger/ 에서 API를 확인할 수 있습니다.

- 기술 스택 : Python(Django), MySQL, Nginx, Dart(Flutter)
- 진행 기간 : 2023.07 ~ 2023.08 (약 1개월)
- 개발 인원 : FE 3명, BE 1명

### 기술 설명
- OracleCloud(Ubuntu)에 nignx와 uWSGI를 이용하여 Backend 서버 구현
- jwt를 활용한 토큰기반 인증 구현
- request와 response를 이용한 데이터 송수신 및 http status code(200, 201, 204, 400, 401) 명시
- KakaoPay API를 이용하여 결제 시스템 구현
- Paginator를 이용하여 게시글 페이징 적용
- django admin을 활용하여 관리 페이지 구현
- swagger를 활용하여 API 문서화

### Backend서버를 구축하며 다음과 같은 사항을 고려했습니다.
#### 1. API 요청 시 검증과 예외처리
반복적인 코드 작성을 피하기 위해 API 요청 시 유저, 게시글, 댓글에 대한 검증과 예외처리를 모듈화했습니다.
예외처리를 하며 API 요청의 결과를 HTTP Status Code(200, 201, 204, 400, 401)를 이용하여 명시했습니다.
#### 2. 유저 인증의 DB I/O 최소화
API를 호출할 때 마다 유저 인증을 위한 DB의 I/O가 생기는 점을 인지했고, 이를 해결하기 위해 JWT를 적용했습니다.
토큰을 기기의 Local Storage에 저장한다는 점을 착안해 플랫폼의 자동로그인 시스템 구현에도 적용했습니다.
#### 3. 화이트 박스 테스트
카카오 결제를 구현하며 토큰이 서버로 제대로 전달되지 않는 문제가 발생했습니다. 문제의 원인을 파악하기 위해 시퀀스 다이어그램을 기준으로 분기를 나누어 검증을 진행했습니다. 이 과정을 통해 정확히 어느 지점에서 문제가 발생하는지 파악 후 해결할 수 있었습니다.
#### 4. 데이터 전송 경량화
게시글 리스트의 요청 시 한번에 전송하면 게시글이 많아질수록 성능저하가 일어나는 문제가 발생했습니다. 이를 해결하기 위해 Paginator를 이용하여 게시글 페이징을 적용했습니다.

## 🎞️ 시연 영상

  ### [https://youtu.be/yqIR-TgG6qE](https://youtu.be/yqIR-TgG6qE)

## 🌉 기획 배경

한국인의 대다수가 카카오톡을 사용하는 요즘, 생일날에 우리는 기프티콘을 주고 받곤 합니다. 좋아하는 음료나 음식을 보내주기도 하고 우스꽝스러운 선물을 보냅니다. 하지만 커피를 선호하지 않는 사람에게 스타벅스 기프티콘을 보내는 등 종종 우리는 만족스럽지 못한 선물을 주고 받을 때도 있습니다. 또 진정 원하는 선물이 있더라도 가격이 부담스러울 때도 있습니다. 이것이 정말 아쉬운 점은 받은 선물의 총액이 그 선물을 상회할 때가 많다는 사실입니다. 이런 불편한 상황을 인지하고 저희 팀은 선물 펀딩 플랫폼을 기획하게 되었습니다. "FunSun"은 친구들이 모여 더욱 특별한 선물을 준비하는데 도움을 주는 펀딩 플랫폼입니다. 저희는 사용자들에게 간단하고 편리한 방식으로 선물을 공동으로 펀딩하고 나누는 기회를 제공합니다. 이 서비스를 통해 사용자들은 함께 모여 선물을 준비하며, 그 과정에서 더욱 의미 있는 연결과 감동을 느낄 수 있길 기대해봅니다.

## 📖 상세 내용

![FUNSUN~1](https://github.com/skay138/FUNSUNback/assets/102957619/b18fe75e-3c27-49e1-a633-0ed02fb626e5)
![FUNSUN~2](https://github.com/skay138/FUNSUNback/assets/102957619/1e5591bc-fe73-4616-b8ec-4dac77c9a02f)
![FUNSUN~3](https://github.com/skay138/FUNSUNback/assets/102957619/4ebddf3f-a2a9-4c9c-b563-20777a424490)
![FUNSUN~4](https://github.com/skay138/FUNSUNback/assets/102957619/74c77292-af81-4fa3-952a-187ece93d9ee)
![FU3FBA~1](https://github.com/skay138/FUNSUNback/assets/102957619/9f546379-780c-43b1-a904-f6f1dd58c25d)
![FUAAC7~1](https://github.com/skay138/FUNSUNback/assets/102957619/43918aca-f194-49a2-8148-ba24c20bd8ba)
![FUD923~1](https://github.com/skay138/FUNSUNback/assets/102957619/a2b0c56f-5481-4e35-8591-89504be6df17)
![FU006F~1](https://github.com/skay138/FUNSUNback/assets/102957619/9e99c4cf-dd13-4b2a-92ae-44fb578130d6)
![FUBA2B~1](https://github.com/skay138/FUNSUNback/assets/102957619/79b76028-62f3-4a94-b408-92fbb1c61c23)
![FUC8C4~1](https://github.com/skay138/FUNSUNback/assets/102957619/f995e65f-b098-407a-bcb5-f4daf7de07db)
![FUA021~1](https://github.com/skay138/FUNSUNback/assets/102957619/2caf3ecf-248a-401c-94e5-3a115746396a)
![FU5BEC~1](https://github.com/skay138/FUNSUNback/assets/102957619/bcf44bf5-f60a-431b-a3fa-2e60df2342a9)
![FU06B8~1](https://github.com/skay138/FUNSUNback/assets/102957619/d93a6668-2d77-4bff-807e-3126c83a051e)
![FUB084~1](https://github.com/skay138/FUNSUNback/assets/102957619/aed7e3c7-de5b-4a33-84d9-4f36defa50d9)
![FUDBEC~1](https://github.com/skay138/FUNSUNback/assets/102957619/8d1243d7-4372-4ad6-9e65-476850a09742)
![FU8947~1](https://github.com/skay138/FUNSUNback/assets/102957619/7570a6c9-ccc2-400c-8c68-3134756570a7)
![FU3184~1](https://github.com/skay138/FUNSUNback/assets/102957619/dc7e192a-d5c4-4e94-85da-ba7590e5042e)
![FU24BF~1](https://github.com/skay138/FUNSUNback/assets/102957619/616a2706-f35b-49a7-b8a9-6311ff3a7d00)


## 📝 메모

### 왜 Kakao Pay API를 사용하였는가?

상용화를 감안한다면, 카카오페이는 펀딩 플랫폼에는 허가가 떨어지지 않기 때문에 그리 좋은 선택은 아니었습니다. 부트페이등 다른 PG API를 사용하는 게 더 적절했습니다. 그럼에도 카카오 페이를 사용한 이유는 많은 플랫폼에서 카카오 페이를 채택하고 있었기 때문입니다. 추후 결제 시스템 도입이 필요할 때 도움이 되리라 판단했습니다.

### JWT

첫 로그인 시 해당 유저에 대해 AccessToken과 RefreshToken을 발행하고 Front에 전달합니다. Front는 토큰들을 Local Storage에 저장해두었다가, API 요청 시 header에 토큰을 함께 전달합니다. Backend에서는 그 토큰이 유효한지만 검증합니다. 이를 통해 DB로의 I/O 없이 유저인증을 할 수 있습니다.
