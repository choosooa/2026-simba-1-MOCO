# 2026-simba-1--MOCO
# 🫧 MOCO

> **사고 싶은 물건을 모아두고, 모아컵으로 최종 선택까지 도와주는 소비 결정 서비스**

<br>

<div align="center">

![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Style-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

<br>

## 📌 프로젝트 소개

**MOCO**는 사용자가 사고 싶은 상품을 보관함에 저장하고,  
카테고리별로 상품을 정리한 뒤, **토너먼트 방식의 모아컵**을 통해  
가장 마음에 드는 상품을 고를 수 있도록 도와주는 웹 서비스입니다.

단순히 상품을 저장하는 것에서 끝나는 것이 아니라,  
여러 후보 중 어떤 상품을 선택할지 고민하는 과정을  
재미있는 월드컵 방식으로 풀어낸 서비스입니다.

<br>

## 🧊 주요 기능

### 👤 회원 기능

- 회원가입
- 로그인 / 로그아웃
- 약관 동의
- 마이페이지
- 닉네임 기반 사용자 인사

<br>

### 📦 아이템 보관함

- 상품 등록
- 상품 이미지 업로드
- 상품명, 가격, 상품 링크 저장
- 최근 저장 상품 조회
- 보관함 목록 조회
- 상품 검색
- 상품 상세 조회
- 상품 수정
- 상품 삭제
- 여러 상품 선택 삭제
- 스크랩 상품 관리

<br>

### 🗂 카테고리 관리

- 기본 카테고리 제공
- 사용자별 개인 카테고리 생성
- 중복 카테고리명 방지
- 카테고리 삭제
- 카테고리별 상품 필터링

<br>

### 🏆 모아컵

- 16강 / 32강 / 64강 토너먼트 생성
- 카테고리별 모아컵 진행
- 상품 랜덤 매칭
- 라운드별 승자 선택
- 최종 우승 상품 결정
- 모아컵 결과 조회
- 최근 모아컵 결과 마이페이지 표시
- 공유 링크 생성
- 비로그인 사용자 공유 모아컵 참여

<br>

## 🖼 화면 구성

| 화면 | 설명 |
|---|---|
| 로그인 | 사용자 로그인 화면 |
| 회원가입 | 아이디, 비밀번호, 닉네임 등록 |
| 메인 | 최근 저장 상품과 주요 이동 버튼 제공 |
| 보관함 | 등록한 상품 목록 확인 |
| 상품 등록 | 상품 이미지, 이름, 가격, 링크 입력 |
| 마이페이지 | 사용자 정보, 모아컵 결과, 계정 관리 |
| 모아컵 시작 | 카테고리와 N강 선택 |
| 모아컵 진행 | 두 상품 중 하나 선택 |
| 모아컵 결과 | 최종 우승 상품 확인 |
| 모아컵 기록 | 완료한 모아컵 결과 목록 확인 |

<br>

## 🛠 기술 스택

### Backend

- Python
- Django
- SQLite

### Frontend

- HTML
- CSS
- JavaScript

### Database

- SQLite3

### Library

- Pillow
- Django humanize

<br>

## 📁 프로젝트 구조

```bash
2026-simba-1-MOCO/
├── accounts/              # 회원가입, 로그인, 마이페이지
├── categories/            # 카테고리 생성 및 삭제
├── items/                 # 상품 등록, 보관함, 검색, 삭제
├── tournaments/           # 모아컵 생성, 진행, 결과, 공유
├── moa_cup/               # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── static/
├── templates/             # 공통 템플릿
├── media/                 # 업로드 이미지 저장
├── manage.py
├── requirements.txt
└── README.md