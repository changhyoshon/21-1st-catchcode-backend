## CATCH FABRIC 프로젝트 Front-end/Back-end 소개

- 국내 최대 포털 사이트 [캐치패션](https://www.catchfashion.com/) 클론 프로젝트

- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론하였으며, 저희의 아이디어가 담기도록 원단 판매 사이트로 변경하였습니다.

- 개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.

### 개발 인원 및 기간

- 개발기간 : 2021/6/7 ~ 2021/6/18
- 개발 인원
  - 프론트엔드
    - 정유정
    - 황윤성
  - 백엔드
    - 유병건
    - 범승원
    - 손창효
- GitHub
  - [프론트엔드 GitHub URL](https://github.com/wecode-bootcamp-korea/21-1st-catchcode-frontend)
  - [백엔드 GitHub URL](https://github.com/wecode-bootcamp-korea/21-1st-catchcode-backend)

### 프로젝트 선정이유

- 캐치패션의 기술스택이 저희 프론트엔드의 기술스택과 겹치는 부분이 있어 선택하였습니다.
- 사이트의 기능적으로도 이중화 카테고리, 게시물 필터기능, 장바구니 등등 기본에 충실한 사이트라고 생각이 되어 선택하였습니다.

### 데모 영상

## 적용 기술 및 구현 기능

### 적용 기술

> - Front-End : React.js, sass, html, JavaScript, 
> - Back-End : Python, Django web framework, Bcrypt, JWT, My SQL
> - Common : AWS(EC2), RESTful API

### 협업 Tool
> trello, slack

### 구현 기능
#### 메인페이지
 - 메인 슬라이드(without API)

#### 회원가입 / 로그인
 - 정규식을 이용한 유효성 검사

#### 상품 리스트 페이지
 - 토글을 통한 필터링
 - query parameter로 필터 값 받아오기

#### 상품 상세 페이지
 - 상품의 사이즈별 가격 및 재고 정보 표기

## Reference

- 이 프로젝트는 [캐치패션](https://www.catchfashion.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
