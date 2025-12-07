# KTB Community Server (Backend)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

카카오테크부트캠프 커뮤니티 게시판 서버 - FastAPI 기반 RESTful API

## 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [API 명세](#-api-명세)
- [데이터베이스 스키마](#-데이터베이스-스키마)

## 프로젝트 소개

KTB Community Server는 FastAPI를 기반으로 구축된 커뮤니티 게시판 백엔드 서버입니다.
JWT 토큰 기반 인증, 게시글/댓글 CRUD, 좋아요 기능 등을 제공합니다.

## 주요 기능

### 회원 관리

- 회원가입 / 로그인 / 로그아웃
- JWT 기반 Access Token & Refresh Token 인증
- 프로필 조회 및 수정
- 비밀번호 변경
- 회원 탈퇴

### 게시글 관리

- 게시글 목록 조회 (페이지네이션)
- 게시글 상세 조회 (조회수 증가)
- 게시글 작성 / 수정 / 삭제
- 게시글 좋아요 토글
- 작성자 닉네임 포함 응답

### 댓글 관리

- 댓글 목록 조회
- 댓글 작성 / 수정 / 삭제
- 작성자 정보 포함 응답

### 파일 업로드

- 이미지 파일 업로드
- Static 파일 서빙

## 기술 스택

### Backend Framework

- **FastAPI** - 고성능 비동기 웹 프레임워크
- **Python 3.12** - 최신 Python 버전
- **Uvicorn** - ASGI 서버

### Database & ORM

- **MySQL** - 관계형 데이터베이스
- **SQLAlchemy** - Python ORM
- **PyMySQL** - MySQL 드라이버

### Authentication

- **JWT (JSON Web Tokens)** - 토큰 기반 인증
- **bcrypt** - 비밀번호 해싱

### Validation

- **Pydantic** - 데이터 검증 및 직렬화

## 📁 프로젝트 구조

```
KTB_community_server/
├── src/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── auth/                   # 인증 관련
│   │   ├── dependencies.py     # 인증 의존성
│   │   ├── model/              # RefreshToken 모델
│   │   ├── repository/         # 토큰 저장소
│   │   ├── service/            # 인증 서비스
│   │   └── utils/              # JWT, Cookie 유틸
│   ├── member/                 # 회원 관리
│   │   ├── api/                # 회원 API 엔드포인트
│   │   ├── model/              # Member 모델
│   │   ├── repository/         # 회원 저장소
│   │   ├── schema/             # 요청/응답 스키마
│   │   └── service/            # 회원 서비스
│   ├── posts/                  # 게시글 관리
│   │   ├── api/                # 게시글 API
│   │   ├── model/              # Post, PostLike 모델
│   │   ├── repository/         # 게시글 저장소
│   │   ├── schema/             # 스키마
│   │   └── service/            # 게시글 서비스
│   ├── comments/               # 댓글 관리
│   │   ├── api/                # 댓글 API
│   │   ├── model/              # Comment 모델
│   │   ├── repository/         # 댓글 저장소
│   │   ├── schema/             # 스키마
│   │   └── service/            # 댓글 서비스
│   ├── common/                 # 공통 모듈
│   │   ├── file_controller.py # 파일 업로드 API
│   │   └── file_service.py    # 파일 서비스
│   ├── database/               # DB 설정
│   │   ├── connection.py       # DB 연결
│   │   └── orm.py              # ORM Base
│   └── static/                 # 정적 파일
│       └── images/             # 업로드 이미지
├── init_db.py                  # DB 초기화 스크립트
└── README.md
```

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.12 이상
- MySQL 8.0 이상
- pip (Python 패키지 관리자)

### 2. 패키지 설치

```
pip install -r requirements.txt
```

주요 패키지:

```
fastapi
uvicorn
sqlalchemy
pymysql
pydantic
bcrypt
python-jose
python-multipart
```

### 3. 서버 실행

```

uvicorn src.main:app --reload


uvicorn src.main:app --reload --port 8000
```
