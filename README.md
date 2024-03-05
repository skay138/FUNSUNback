
# FunSun: 즐거운 펀딩 플랫폼
![KakaoTalk_20230822_103135088](https://github.com/skay138/FUNSUNback/assets/102957619/ccfd29c5-6b32-410c-af4f-aee707bb2351)
FunSun은 상대방의 취향과 필요성을 고려하여 정말 받고싶은 선물을 받을 수 있도록 친구들이 함께 서포트하는 플랫폼입니다. 크라우드 펀딩의 개념을 도입하여 여러 사용자들이 함께 모여 선물을 구매하고 불필요한 비용을 줄이는 서비스를 제공합니다.

위 레파지토리는 FUNSUN 플랫폼(https://github.com/FUNFUNSUN/funsunfront) 의 BACKEND 서버입니다.

http://projectsekai.kro.kr:5000/swagger/ 에서 API를 확인할 수 있습니다.

## 🎞️ 시연 영상

  ### [https://youtu.be/yqIR-TgG6qE](https://youtu.be/yqIR-TgG6qE)


## 📖 상세 내용

![포트폴리오_1-01](https://github.com/skay138/FUNSUNback/assets/102957619/9254f68e-4307-452d-ac70-45be0c301917)
![포트폴리오_1-02](https://github.com/skay138/FUNSUNback/assets/102957619/4b8f1861-ea35-4705-bfeb-df8f21555aea)
![포트폴리오_1-03](https://github.com/skay138/FUNSUNback/assets/102957619/089e534b-8de0-49eb-9976-73dca0ec775a)
![포트폴리오_1-04](https://github.com/skay138/FUNSUNback/assets/102957619/40df13fd-9b01-415c-8145-e75c29a59c18)
![포트폴리오_1-05](https://github.com/skay138/FUNSUNback/assets/102957619/0534e80a-7920-451b-acf3-cb38eeb5d115)
![포트폴리오_1-06](https://github.com/skay138/FUNSUNback/assets/102957619/8cdc0ea4-0bc3-4eff-918c-113f63efa098)
![포트폴리오_1-07](https://github.com/skay138/FUNSUNback/assets/102957619/58e004a8-b323-4399-9a73-8d57e189c8d7)
![포트폴리오_1-08](https://github.com/skay138/FUNSUNback/assets/102957619/238c927b-5567-4c9f-b69d-92fffbcf0b72)
![포트폴리오_1-09](https://github.com/skay138/FUNSUNback/assets/102957619/de36003a-8d0e-4b6c-9619-3a4b541f2d6b)
![포트폴리오_1-10](https://github.com/skay138/FUNSUNback/assets/102957619/b43520a2-5cac-47bf-b070-1cc117de7e73)
![포트폴리오_1-11](https://github.com/skay138/FUNSUNback/assets/102957619/870d9aaa-592e-4477-b802-2ba9f294f662)
![포트폴리오_1-12](https://github.com/skay138/FUNSUNback/assets/102957619/9a37ea03-e5b7-4584-8e71-30b55fe90f94)
![포트폴리오_1-13](https://github.com/skay138/FUNSUNback/assets/102957619/fb107e5d-4a02-4523-a5d8-ca2a218c6211)
![포트폴리오_1-14](https://github.com/skay138/FUNSUNback/assets/102957619/6a5d40cc-8f98-458d-b2f0-883b5cb735c5)
![포트폴리오_1-15](https://github.com/skay138/FUNSUNback/assets/102957619/6cd2817f-5d65-40a6-9470-c7c96068a5f8)
![포트폴리오_1-16](https://github.com/skay138/FUNSUNback/assets/102957619/e665b30e-7a5b-4f77-88b6-324a954a481e)
![포트폴리오_1-17](https://github.com/skay138/FUNSUNback/assets/102957619/e6f68ba0-404a-4e41-b33c-1c5b2c700e5b)
![포트폴리오_1-18](https://github.com/skay138/FUNSUNback/assets/102957619/833bc6e6-f001-4b80-8f2d-855e5bc0120b)
![포트폴리오_1-19](https://github.com/skay138/FUNSUNback/assets/102957619/5eafedfa-582f-4d02-8e92-ade346908eb2)
![포트폴리오_1-20](https://github.com/skay138/FUNSUNback/assets/102957619/7c0553d9-f6f6-4307-aca6-62e801dc3114)
![포트폴리오_1-21](https://github.com/skay138/FUNSUNback/assets/102957619/7af24917-a6da-406d-9747-91adfc8e9c59)
![포트폴리오_1-22](https://github.com/skay138/FUNSUNback/assets/102957619/43657128-40d7-45e7-8959-bb085247ed31)
![포트폴리오_1-23](https://github.com/skay138/FUNSUNback/assets/102957619/b2a1b027-b7c5-4d41-9296-f80e97c8be91)

## 📝 메모

### JWT

첫 로그인 시 해당 유저에 대해 AccessToken과 RefreshToken을 발행하고 Front에 전달합니다. Front는 토큰들을 Local Storage에 저장해두었다가, API 요청 시 header에 토큰을 함께 전달합니다. Backend에서는 그 토큰이 유효한지만 검증합니다. 이를 통해 DB로의 I/O 없이 유저인증을 할 수 있습니다.
