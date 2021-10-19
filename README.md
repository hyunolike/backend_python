# 백엔드 프리온보딩 선발 과제
> Django

## 목차
1. [구현 방법](#1-구현-방법)
2. [실행 방법](#2-실행-방법)
3. [API 명세](#3-API-명세)


## 1 구현 방법
### 1-1. 환경 및 구조
- 파이썬 `Django`를 사용해 API 개발
- 데이터베이스 sqlit3 구현

### 1-2. 코드 구현
#### 1. 공통
  - CRUD 게시판 개발
  
#### 2. 테이블 구현하기
  - `crud\models.py` 테이블 생성
  - 장고 셸을 통해 임시 데이터 삽입
  
#### 3. 게시판 목록 읽기 구현하기
  - `Board.objects.order_by('-create_date')` 코드로 역순 조회 가능하도록 구현
  - 미리 개발된 템플릿 화면을 통해 테스트 진행

#### 4. 게시판 내용 읽기 구현하기
  - `board\urls.py` URL 매핑하기 >> path('<int:board_id>/', views.detail, name='detail')
  - `board\views.py` detail 함수 추가
  - 템플릿 화면에서 board 객체 매칭을 통한 {{ board.subject }} 내용 출력하기

#### 5. 게시판 생성 구현하기
  - `board\urls.py` URL 매핑하기 >> path('board/create/', views.board_create, name='board_create)
  - `board\views.py` board_create 함수 추가
  - 장고 폼(forms.ModelForm)을 사용해 모델과 연결시켜 데이터 저장하는 방식으로 구현
  - GET 방식일 경우, 입력값 없이 객체 생성 / POST 방식일 경우, 화면에 전달받은 데이터로 폼의 값이 채워지도록 객체 생성
  - is_valid()함수로 POST 요청으로 받은 form이 유효한지 검사
  - board = form.save(commit=False) 코드로 모델 데이터 저장

#### 6. 게시판 페이징 구현하기
  - `board\urls.py` 의 index 함수에서 추가적으로 구현
  - page = request.GET.get('page','1') 코드로 첫번째 화면 나오도록 구현
  - Paginator 클래스로 페이징 10개씩 나오도록 구현
  - 템플릿 화면 if문 처리로 기능 구현
  ```python
  <!-- 페이징처리 -->
  {% if board_list.has_previous %}
  <a href="?page={{board_list.previous_page_number}}">이전으로</a>
  {% endif %}
  <span>{{board_list.number}}</span>
  <span>/</span>
  <span>{{board_list.paginator.num_pages}}</span>
  {% if board_list.has_next %}
  <a href="?page={{board_list.next_page_number}}">다음으로</a>
  {% endif %}
  ```

#### 7. 로그인, 로그아웃 구현 준비
  - 기존 `django.contrib.auth` 앱을 통해 구현
  - 기능을 종속시키지 않기위해 새롭게 common 앱 생성

#### 8. 로그인 구현하기
  - `commom\urls.py` URL 매핑하기 >> path('login/', auth_views.LoginView.as_view(), name='login')
  - LoginView가 common 디렉토리의 화면을 참조할 수 있도록 template_name = 'common/login.html' 코드 추가 
  >> `최종 코드` path('login/', auth_views.LoginView.as_view(template_name = 'common/login.html'), name='login')
  - 로그인 화면 개발과 동시에 필드, 넌필드 오류 출력 패이지 또한 개발 
  - 로그인 성공 시 이동할 페이지를 `config\settings.py` 에 LOGIN_REDIRECT_URL = '/' 추가
  - 이후, `config\urls.py` 파일에 해당 URL 추가
  
#### 9. 로그아웃 구현하기
  - `commom\urls.py` URL 매핑하기 >> path('logout/', auth_views.LoginView.as_view(), name='logout')
  - 로그아웃 성공 시 이동할 페이지 위와 동일하게 설정

#### 10. 유저생성 구현하기
  - `commom\urls.py` URL 매핑하기 >> path('signup/', views.signup, name='signup')
  - signup 함수 추가 
  - POST 방식일 경우, 입력한 데이터로 새로운 유저 생성 / GET 방식일 경우, 회원가입 화면으로 이동하기
  - 회원가입 이후, 자동로그인이 되도록 authenticate(), login() 사용

#### 11. 게시판 유저권한 구현하기
  - @login_required 애너테이션을 통해 로그인 되었는지 우선 검사 및 사용자와 작성자가 동일한 경우에 버튼 나타나도록 구현

#### 12. 게시판 수정 구현하기
  - 템플릿 화면 수정 버튼 추가
  - 수정 버튼 URL 매핑하기 >> path('board/modify/<int:board_id>/', views.board_modify, name='board_modify')
  - board_modify 함수 추가 
  - 수정권한 메시지 발생시키기 위해 message 모듈 사용

#### 13. 게시판 삭제 구현하기
  - 삭제 버튼 추가
  - a태그 주소 `{% url 'crud:board_delete' board_id %}` url 설정해 클릭 시 삭제 가능하도록 구현
  - board_delete 함수 추가
  
  
## 2 실행 방법


## 3 API 명세
> 게시판 CRUD

### CREATE (게시판 생성)
```python
POST board/create/
```
- 요청
```
author : 작성자
subject : 제목 
content : 내용
create_date : 작성 시간 
```
- 응답
```
index 페이지 이동
```

### UPDATE (게시판 수정)
```python
POST board/modify/<int:board_id>/ 
```
- 요청
```
author : 작성자
subject : 제목
content : 내용
modify_date : 수정 시간
```
- 응답
```
게시판 목록 페이지 이동
```

### READ (게시판 읽기)
```python
GET <int:board_id>/
```
- 요청
```
board_id
```
- 응답
```
게시판 페이지 이동
```

### DELETE (게시판 삭제)
```python
POST board/delete/<int:board_id>/
```
- 요청
```
board_id
```
- 응답
```
index 페이지 이동
```
