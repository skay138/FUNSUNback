
# FunSun: 즐거운 펀딩 플랫폼
![KakaoTalk_20230822_103135088](https://github.com/skay138/FUNSUNback/assets/102957619/ccfd29c5-6b32-410c-af4f-aee707bb2351)
FunSun은 상대방의 취향과 필요성을 고려하여 정말 받고싶은 선물을 받을 수 있도록 친구들이 함께 서포트하는 플랫폼입니다. 크라우드 펀딩의 개념을 도입하여 여러 사용자들이 함께 모여 선물을 구매하고 불필요한 비용을 줄이는 서비스를 제공합니다.

위 레파지토리는 FUNSUN 플랫폼(https://github.com/FUNFUNSUN/funsunfront) 의 BACKEND 서버입니다.

http://projectsekai.kro.kr:5000/swagger/ 에서 API를 확인할 수 있습니다.

## 🎞️ 시연 영상

  ### [https://youtu.be/yqIR-TgG6qE](https://youtu.be/yqIR-TgG6qE)


## 📖 상세 내용

![FUNSUN~1](https://github.com/skay138/FUNSUNback/assets/102957619/b18fe75e-3c27-49e1-a633-0ed02fb626e5)
![FunSun_포트폴리오-02](https://github.com/skay138/FUNSUNback/assets/102957619/429bc978-572b-4059-9b48-f5d8a2cd2727)
![FunSun_포트폴리오-03](https://github.com/skay138/FUNSUNback/assets/102957619/ed7e80f5-5bc8-4d94-b553-d2c9eaa9a727)
![FunSun_포트폴리오-04](https://github.com/skay138/FUNSUNback/assets/102957619/ddc91f0d-1f80-485d-bcbb-e9350152069a)
![FunSun_포트폴리오-05](https://github.com/skay138/FUNSUNback/assets/102957619/4d89c0d5-6c85-445e-bdc0-1ec8b8f37ce2)
![FunSun_포트폴리오-06](https://github.com/skay138/FUNSUNback/assets/102957619/6f41ee12-951f-4aea-baa0-7c971dbb3d3d)
![FunSun_포트폴리오-07](https://github.com/skay138/FUNSUNback/assets/102957619/04fadec1-1c5e-4970-a5d2-e4410efa3af4)
![FunSun_포트폴리오-08](https://github.com/skay138/FUNSUNback/assets/102957619/6e63bb26-0b65-4eb2-915c-3c6214a6bcdf)
![FunSun_포트폴리오-09](https://github.com/skay138/FUNSUNback/assets/102957619/ff8f2f11-f58b-430b-a78c-3424265d25c1)
![FunSun_포트폴리오-10](https://github.com/skay138/FUNSUNback/assets/102957619/f59e2856-4236-4c87-840e-0e9b9b37be8a)
![FunSun_포트폴리오-11](https://github.com/skay138/FUNSUNback/assets/102957619/36524371-4555-482d-a147-a26cd3a91f18)
![FunSun_포트폴리오-12](https://github.com/skay138/FUNSUNback/assets/102957619/04f8a056-d8bd-4a37-aae7-efa55f3e1e6f)
![FunSun_포트폴리오-13](https://github.com/skay138/FUNSUNback/assets/102957619/aec929b1-1fb7-4bda-a79a-85229058fe90)
![FunSun_포트폴리오-14](https://github.com/skay138/FUNSUNback/assets/102957619/0b5a9f1a-918f-4580-9627-bb72b73a14b2)
![FunSun_포트폴리오-15](https://github.com/skay138/FUNSUNback/assets/102957619/4d5e5cca-8774-4b03-93e4-da36e980fe00)
![FunSun_포트폴리오-16](https://github.com/skay138/FUNSUNback/assets/102957619/916e7166-62ab-41a7-a295-d9eed8f70526)
![FunSun_포트폴리오-17](https://github.com/skay138/FUNSUNback/assets/102957619/f38ce433-0de7-49c4-8374-d34649f8377b)
![FunSun_포트폴리오-18](https://github.com/skay138/FUNSUNback/assets/102957619/b32bb5b1-62b0-4c75-bd12-0dd5d318267e)
![FunSun_포트폴리오-19](https://github.com/skay138/FUNSUNback/assets/102957619/59ef8d89-5aad-4f03-b33f-52a76e567873)
![FunSun_포트폴리오-20](https://github.com/skay138/FUNSUNback/assets/102957619/398414c4-8f0e-4451-a8c7-85831d168380)

## 📝 메모

### JWT

첫 로그인 시 해당 유저에 대해 AccessToken과 RefreshToken을 발행하고 Front에 전달합니다. Front는 토큰들을 Local Storage에 저장해두었다가, API 요청 시 header에 토큰을 함께 전달합니다. Backend에서는 그 토큰이 유효한지만 검증합니다. 이를 통해 DB로의 I/O 없이 유저인증을 할 수 있습니다.
