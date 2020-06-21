# ch04. 북마크(bookmark)

## 4.1 사이트 기능 살펴보기

### 4.1.1 목록 페이지
- 북마크 목록을 페이지 구분 처리하여 출력

![ch04_list](https://user-images.githubusercontent.com/10287629/77892280-563d7b80-72ad-11ea-8cf5-a63ed464728e.png)

- 북마크 목록 다음 페이지 보기

![ch04_list2](https://user-images.githubusercontent.com/10287629/77892494-a61c4280-72ad-11ea-876d-ce40d3a3d25b.png)
- `Previous`, `Next` 및 현재 페이지 번호 버튼 색상의 반전에 주목
  (장고 page 객체와 CSS로 구현)
- 페이지 우상단의 (햄버거) 메뉴 바
  - 사이트의 모든 페이지에 공통적으로 표시
  - 부트스트랩(Bootstrap)이라는 CSS 프레임워크로 구현
### 4.1.2 북마크 추가
![ch04_03_add](https://user-images.githubusercontent.com/10287629/77893292-b4b72980-72ae-11ea-8238-07eaac013bff.png)
### 4.1.3 북마크 상세
![ch04_04_detail](https://user-images.githubusercontent.com/10287629/77893480-ee883000-72ae-11ea-8a3f-ec02ca5f7661.png)
### 4.1.4 북마크 수정
![ch04_05_update](https://user-images.githubusercontent.com/10287629/77893622-1bd4de00-72af-11ea-95cb-3c2613d55680.png)
### 4.1.5 북마크 삭제
![ch04_06_delete](https://user-images.githubusercontent.com/10287629/77893801-5fc7e300-72af-11ea-82ac-2fe74d4d0fea.png)
### 4.1.6 관리자 페이지
![ch04_07_admin](https://user-images.githubusercontent.com/10287629/77894189-e7aded00-72af-11ea-89a9-d8b911e27840.png)

## 4.2 북마크 앱 만들기
### 4.2.1 프로젝트 만들기
- 파이참 Pure Python 프로젝트 생성
  - Location: C:\work\ch04_bookmark
  - Project Interpreter: Python 3.8 (vnv_dj)
- 장고 프로젝트 생성 및 초기 작업
```SHELL {.line-numbers}
(vnv_dj) C:\work\ch04_bookmark>django-admin startproject config .  # 마지막 . 주의
(vnv_dj) C:\work\ch04_bookmark>python manage.py migrate
(vnv_dj) C:\work\ch04_bookmark>python manage.py createsuperuser
```
- 한글 언어 설정 및 테스트 런
`settings.LANGUAGE_CODE = 'ko'`
### 4.2.2 bookmark 앱 생성하기
- 앱 생성
```SHELL {.line-numbers}
(vnv_dj) C:\work\ch04_bookmark>python manage.py startapp bookmark
```

### 4.2.3 모델 만들기
- 웹 사이트 제작 과정에서 DB에 저장할 사항을 정의
  - `models.Model`을 상속받아서 `Bookmark` 클래스(테이블) 정의
  - 클래스 내부에는 변수(필드) 두 개 정의
  - `url` 필드는 `models.URLField` 형으로 지정
```PYTHON {.line-numbers}
# bookmark/models.py
from django.db import models


class Bookmark(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField('Site URL')
```
- settings.INSTALLED_APPS += 'bookmark'
- DB 현행화 작업
```SHELL {.line-numbers}
(vnv_dj) C:\work\ch04_bookmark>python manage.py makemigrations bookmark
(vnv_dj) C:\work\ch04_bookmark>python manage.py migrate bookmark
```

### 4.2.4 관리자 페이지에 모델 등록
- `from .models import Bookmark` 구문을 통하여,
  현재 폴더의 models.py 파일에서 Bookmark 모델을 임포트
- 이렇게 임포트한 모델을 `admin.site.register(Bookmark)` 구문으로 관리자 페이지에 등록
```PYTHON {.line-numbers}
# bookmark/admin.py
from django.contrib import admin

from .models import Bookmark

admin.site.register(Bookmark)
```
- 서버 기동하여 테스트 런
  - 사이트 몇 개 등록
  - 'Bookmark object(1)' 형식으로 출력되어, 북마크 내용을 짐작하기 어려움

### 4.2.5 모델에 `__str__` 메서드 추가
- 파이썬의 [매직 메서드 또는 던더(Double UNDERscore) 메서드](https://corikachu.github.io/articles/python/python-magic-method)
- 북마크 모델에 `__str__()` 메서드 추가
  - 당연한 말이지만,
    `__str__()` 메서드는 항상 문자열을 반환해야 함
```PYTHON {.line-numbers}
# bookmark/models.py
from django.db import models


class Bookmark(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField('Site URL')

    def __str__(self):                   # 객체를 출력할 때 나타날 값 !!!
        return "이름 : " + self.site_name + ", 주소 : " + self.url # !!!
```
- 이제 다시 서버 기동하여 테스트 런 (객체 내용이 출력됨을 확인)

### 4.2.6 목록 뷰 만들기
- 관리자 페이지에서 북마크 관리가 가능하지만, 일반 사용자를 위해서 뷰를 작성해야 함
- 목록 뷰에 해당하는 BookmarkListView 작성
```PYTHON {.line-numbers}
# bookmark/views.py
from django.views.generic.list import ListView

from .models import Bookmark


class BookmarkListView(ListView):
    model = Bookmark
```
- 뷰에는 함수 기반 뷰(FBV)와 클래스 기반 뷰(CBV)가 있는데,
  - 우리는 CBV로 작성했음
  - ListView를 상속받아서 BookmarkListView 클래스를 정의
  - model을 Bookmark로 지정

### 4.2.7 URL 연결하기
- 방금 작성한 BookmarkListView를 위한 접속경로 정의
  - `config/urls.py`와 `bookmark/urls.py`로 분리하여 작성하는 이유는
    앱의 재사용성을 높이기 위함
  - 'http://127.0.0.1:8000/bookmark/' 형태의 경로로 접속하면,
    - 서버 주소에 해당하는 'http://127.0.0.1:8000/' 부분을 제외한
    - 'bookmark/' 부분이 `config/urls.py`에 전달되고,
    - 'bookmark/' 패턴과 일치하므로, `include('bookmark.urls')` 구문에 의하여
    - `bookmark/urls.py`로 전달되는데,
    - 이때, 이미 매칭된 부분을 제거하고 나머지 '' 부분만 전달되어
    - '' 패턴과 일치하므로 BookmarkListView.as_view()에 의하여 처리됨
```PYTHON {.line-numbers}
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bookmark/', include('bookmark.urls')),
    path('admin/', admin.site.urls),
]
```
```PYTHON {.line-numbers}
# bookmark/urls.py
from django.urls import path
from .views import BookmarkListView

urlpatterns = [
    path('', BookmarkListView.as_view(), name='list'),
]
```
- `BookmarkListView.as_view()` 구문에서 BookmarkListView가 CBV이므로,
  `.as_view()`를 반드시 지정해야 클래스에 대한 진입점으로 해석됨
- 지금 테스트 런 하면,
  CBV와 접속 경로는 정의했지만,
  아직 템플릿 작성이 안된 상태라서,
  TemplateDoesNotExist 오류가 발생함

### 4.2.8 bookmark_list.html
- 템플릿은 장고에서 데이터를 끼워 넣을 양식에 해당하는 파일
- 템플릿 파일은 `bookmark/templates/bookmark/` 폴더 내부에 저장함
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_list.html #}
<div class="btn-group">
    <a href="#" class="btn btn-info">Add Bookmark</a>
</div>
<p></p>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Site</th>
            <th scope="col">URL</th>
            <th scope="col">Modify</th>
            <th scope="col">Delete</th>
        </tr>
    </thead>
    <tbody>
        {% for bookmark in object_list %}
            <tr>
                <td>
                    {{ forloop.counter }}
                </td>
                <td>
                    <a href="#">{{bookmark.site_name}}</a>
                </td>
                <td>
                    <a href="{{bookmark.url}}" target="_blank">{{bookmark.url}}</a>
                </td>
                <td><a href="#" class="btn btn-success btn-sm">Modify</a></td>
                <td><a href="#" class="btn btn-danger btn-sm">Delete</a></td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```
- tbody 태그 내부에서 반복 루프를 처리할 때,
  `object_list`라는 맥락 변수에 주목
  - `object_list`는 CBV에서 맥락 변수에 대한 디폴트 이름으로 사용됨
  - 우리가 작성했던 CBV에는 `model = Bookmark`라는 한 줄만 존재했었음
- 북마크 한 건마다 tr 태그로 처리
- `{{ forloop.counter }}`는 반복 번호에 해당함
- 테스트 런 확인
  - 아직까지 'Modify', 'Delete' 및 'Add Bookmark' 단추 기능은 구현하지 못한 상태임
  - 버튼 등에 부트스트랩 적용 못한 상태임

### 4.2.9 북마크 등록 기능 구현
- 북마크 추가를 위한 BookmarkCreateView를 CBV로 작성
  - CreateView를 상속받아 구현
  - model 변수 지정
  - fields 변수에 북마크 추가를 위해 입력받을 필드 지정
  - success_url 변수에 북마크 추가 성공할 경우,
    - 이동할 리다이렉트 경로를 reverse_lazy('list')로 지정
    - 'list'는 북마크 목록 보여주는 접속 경로에 부여한 이름
  - template_name_suffix 변수에 사용할 템플릿의 접미사만 지정
    - 디폴트 값으로 모델명_xxx = bookmark_create(.html)이 적용됨
```PYTHON {.line-numbers}
# bookmark/views.py
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('list')  # 글쓰기를 완료했을 때 이동할 페이지
    template_name_suffix = '_create'
```
- 접속 경로 연결
```PYTHON {.line-numbers}
# bookmark/urls.py
from django.urls import path
from .views import BookmarkListView, BookmarkCreateView

urlpatterns = [
    path('', BookmarkListView.as_view(), name='list'),
    path('add/', BookmarkCreateView.as_view(), name='add'),
]
```
- 템플릿 작성
  - form 태그 활용
    - 템플릿에 입력된 데이터를 서버로 전달하기 위해 `method="post"` 지정
    - 현재 페이지로 전달하기 위해 `action=""` 지정
    - 사이트 간 요청 변조를 방지하기 위해 `{% csrf_token %}` 지정
    - CBV에서 지정한 fields 변수를 문단 구분형 폼으로 처리하기 위해 `{{form.as_p}}` 지정
    - 전송 버튼
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_create.html #}
<form action="" method="post">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Add" class="btn btn-info btn-sm">
</form>
```
- 테스트 런
  - 네이버 사이트 등록
  - 등록 성공하면 리스트 뷰로 이동함을 확인
- 리스트 뷰 좌상단에 'Add Bookmark' 링크 구현
  - 이름이 'add'인 접속 경로로 연결
  - 테스트 런하여 다음 사이트 등록 및 리스트 뷰로 리다이렉트 확인
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_list.html #}
<div class="btn-group">
    <a href="{% url 'add' %}" class="btn btn-info">Add Bookmark</a>
</div>
{# ... #}
```

### 4.2.10 북마크 확인(상세보기) 기능 구현
- 확인 뷰 구현
```PYTHON {.line-numbers}
# bookmark/views.py
from django.views.generic.detail import DetailView

class BookmarkDetailView(DetailView):
    model = Bookmark
```
- 접속 경로 구현
  - 'detail/<int:pk>/' 패턴에서 (컨버터가) 정수형(으로 지정된) 기본키를
  - pk라는 변수로 포착
```PYTHON {.line-numbers}
# bookmark/urls.py
from django.urls import path
from .views import *          # !!!

urlpatterns = [
    path('', BookmarkListView.as_view(), name='list'),
    path('add/', BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', BookmarkDetailView.as_view(), name='detail'),
]
```
- 기본적으로 제공되는 컨버터
  - str: 공백 아닌 문자열과 매칭, 단 '/'는 제외, 특정 컨버터가 지정되지 않을 경우 디폴트 컨버터
  - int: 0을 포함한 양의 정수와 매칭
  - slug: 숫자, 하이픈, 언더스코어를 포함한 아스키 문자로서 슬러그 문자열과 매칭
  - uuid: UUID와 매칭, 같은 페이지에 여러 URL이 연결되는 현상을 방지하려고 사용
  - path: 기본적으로 str과 같은 기능이나, '/'도 포함, URL 전체에 대한 매칭을 시도할 때 사용
- 템플릿 구현
  - 확인(상세보기) 뷰에 대한 디폴트 템플릿은 '모델명_detail.html'임
  - 확인(상세보기) 템플릿에서는 디폴트로 'object' 맥락변수가 전달되며,
    이 객체는 접속 경로 패턴에서 포착한 pk 값을 가지는 객체로 자동 설정됨
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_detail.html #}
{{object.site_name}}<br/>
{{object.url}}
```
- 목록 보기 템플릿에서 확인 뷰로 연결하는 링크를 구현
  - bookmark_list.html에서
  - `<a href="#">{{bookmark.site_name}}</a>` 부분을
  - `<a href="{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a>`로 수정
  - 즉, url('detail', pk=bookmark.id)로 연결하는 방식임
- 테스트 런 하여,
  - 리스트 보기 페이지에서 사이트 이름 링크를 클릭하면,
  - 사이트 확인(상세보기) 페이지로 연결됨을 확인
- 컨버터 관련 보충 내용(원문은 [여기](https://suwoni-codelab.com/django/2018/03/24/Django-Url-function/) 참조)
  - 접속 경로에서 특정 값을 포착하여 뷰에 전달할 때, 값의 자료형을 제한하는 방법
  - <컨버터:전달할키워드인자명>  형태로 입력하면 입력받는 데이터의 자료형을 제한할 수 있음
  - 컨버터의 종류와 역할
    - str : 경로 구분자를 제외한 비어 있지 않은 문자열
    - path: 경로 구분자를 포함한 비어 있지 않은 문자열
    - int : 0 또는 임의의 양의 정수
    - slug : 문자 또는 숫자와 하이픈 및 밑줄 문자로 구성된 슬러그 문자열
             예를 들어, SHOW-ME-THE-MONEY
  - 커스텀 컨버터 작성법
      https://docs.djangoproject.com/ko/2.0/topics/http/urls/#registering-custom-path-converters
  - [여기](https://suwoni-codelab.com/django/2018/03/24/Django-Url-function/)에서 예제 참고
  - URL 경로 설정에 사용되는 함수
    - include()
    - path()
    - re_path()
    - url()

### 4.2.11 북마크 수정 기능 구현
- 제네릭 뷰로 수정 기능을 구현하면,
  - 추가 기능과 비슷하지만,
  - (빈 데이터가 아니라,) 기존 데이터 편집 상태로 처리됨
```PYTHON {.line-numbers}
# bookmark/views.py
from django.views.generic.edit import CreateView, UpdateView

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['site_name', 'url']
    template_name_suffix = '_update'  # 따라서 bookmark_update.html이어야 함
```
- 접속 경로 연결
```PYTHON {.line-numbers}
# bookmark/urls.py
from django.urls import path
from .views import *          # !!!

urlpatterns = [
    path('', BookmarkListView.as_view(), name='list'),
    path('add/', BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', BookmarkDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BookmarkUpdateView.as_view(), name='update'),
]
```
- 템플릿 구현
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_update.html #}
<form action="" method="post">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Update" class="btn btn-info btn-sm">
</form>
```
- 리스트 템플릿에서도 Modify 링크 연결
  - bookmark_list.html에서
  - `<a href="#" class="btn btn-success btn-sm">Modify</a>` 부분을
  - `<a href="{% url 'update' pk=bookmark.id %}" class="btn btn-success btn-sm">Modify</a>`로 수정
- 테스트 런 수행하면, 'No URL to redirect to.' 오류 발생
  - 리다이렉트 지정 누락이 원인
  - (앞서 BookmarkCreateView와 같이) 리다이렉트를 지정하거나,
  - get_absolute_url() 메서드를 지정해야 함
- models.py 내부에 get_absolute_url() 메서드 정의
  - 객체의 상세 화면 주소를 반환하는 메서드
  - reverse() 함수로 반환
  - args 인자를 리스트 `[str(self.id)]`로 지정
  - args 인자는 항상 문자형이어야 하므로, str() 함수로 형 변환 처리함
```PYTHON {.line-numbers}
# bookmark/models.py
from django.db import models
from django.urls import reverse  # !!!

class Bookmark(models.Model):
    # ...
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])
```
- 다시 테스트 런 수행
  - 리스트 화면에서 특정 사이트 수정하면, 상세보기 화면으로 이동함
  - 사실 이런 방식보다는 뷰에서 success_url을 지정하는 방식이 더 나은 듯...

### 4.2.12 북마크 삭제 기능 구현
- 제네릭 뷰를 상속받아 구현
```PYTHON {.line-numbers}
# bookmark/views.py
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('list')
```
- 접속 경로 구현
```PYTHON {.line-numbers}
# bookmark/urls.py
from django.urls import path
from .views import *          # !!!

urlpatterns = [
    path('', BookmarkListView.as_view(), name='list'),
    path('add/', BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', BookmarkDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BookmarkUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookmarkDeleteView.as_view(), name='delete'),
]
```
- (템플릿 구현에 앞서서, 먼저) 리스트 템플릿에서 Delete 링크 구현
  - bookmark_list.html에서
  - `<a href="#" class="btn btn-danger btn-sm">Delete</a>` 부분을
  - `<a href="{% url 'delete' pk=bookmark.id %}" class="btn btn-danger btn-sm">Delete</a>`로 수정
- 테스트 런 수행하여, 오류 확인
  - 템플릿 없다는 오류 발생
  - 템플릿 이름이 'bookmark_confirm_delete.html'로 지정되었음을 확인
- 템플릿 구현
  - 삭제 경우에는 확인이 필요함
  - 확인 여부에 관한 데이터를 서버로 전달하기 위하여 form 태그를 사용함
  - `{{object}}`는 뷰가 전달해주는 맥락 변수
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_confirm_delete.html #}
<form action="" method="post">
    {% csrf_token %}
    <div class="alert alert-danger">Do you want to delete Bookmark "{{object}}"?</div>
    <input type="submit" value="Delete" class="btn btn-danger">
</form>
```
- 테스트 런 수행하여, 삭제 확인 버튼을 클릭하여 삭제하면 리스트 페이지로 이동함을 확인
- 지금까지, 북마크 앱의 모든 기능 구현을 완료
- 이제부터, 북마크 앱의 디자인을 입혀볼 예정

## 4.3 디자인 입히기
- "공대생 디자인 같은데..."라는 소리를 듣지 않기 위해서
### 4.3.1 템플릿 확장하기
- 단일 웹 사이트에서 모든 페이지 디자인의 통일성
- 현재 우리가 작성한 5개 페이지에 동일한 메뉴바를 추가하려면?
    - 목록/상세 보기
    - 등록/수정/삭제
- 템플릿 (상속) 확장 방법
    - 공통적 요소는 부모 템플릿으로 작성
    - 부모 템플릿을 상속받아 자식 템플릿을 작성
    - 특정 자식 템플릿에 추가적인 요소만 확장
- 부모 템플릿 작성
    - 프로젝트 루트 폴더에 부모 템플릿을 위한 templates 폴더 생성
      결국, ch04_bookmark\templates\base.html 템플릿 작성
```SHELL {.line-numbers}
# 현재의 settings.TEMPLATES[0]['DIRS'] 확인
(vnv_dj) C:\work\ch04_bookmark>python manage.py shell
>>> from django.conf import settings
>>> settings.TEMPLATES[0]['DIRS']
[]
```
```PYTHON {.line-numbers}
# config/settings.py  # settings.TEMPLATES[0]['DIRS'] 변경
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],                   # !!!
        # 템플릿을 검색할 때, 우선적으로 확인할 폴더를 지정한 것임
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
```SHELL {.line-numbers}
# 변경된 settings.TEMPLATES[0]['DIRS'] 확인
(vnv_dj) C:\work\ch04_bookmark>python manage.py shell
>>> from django.conf import settings
>>> settings.TEMPLATES[0]['DIRS']
['C:\\work\\ch04_bookmark\\templates']
>>> settings.BASE_DIR
'C:\\work\\ch04_bookmark'
```
```HTML {.line-numbers}
{# ch04_bookmark/templates/base.html 부모 템플릿 작성 #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}   {# 제목 블럭 #}

        {% endblock %}
    </title>
</head>
<body>
    {% block content %}     {# 내용 블럭 #}

    {% endblock %}
</body>
</html>
```
- bookmark_confirm_delete.html 코드
    - 상속을 위한 extends 태그 추가
    - 제목 블럭 지정
    - 내용 블럭 지정(원래 코드를 블럭 내부로 이동)
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_confirm_delete.html #}
{% extends 'base.html' %}

{% block title %}Confirm Delete{% endblock %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        <div class="alert alert-danger">Do you want to delete Bookmark "{{object}}"?</div>
        <input type="submit" value="Delete" class="btn btn-danger">
    </form>
{% endblock %}
```
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_create.html #}
{% extends 'base.html' %}

{% block title %}Bookmark Add{% endblock %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Add" class="btn btn-info btn-sm">
    </form>
{% endblock %}
```
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_detail.html #}
{% extends 'base.html' %}

{% block title %}Detail{% endblock %}

{% block content %}
    {{object.site_name}}<br/>
    {{object.url}}
{% endblock %}
```
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_list.html #}
{% extends 'base.html' %}

{% block title %}Bookmark List{% endblock %}

{% block content %}
    <div class="btn-group">
        <a href="{% url 'add' %}" class="btn btn-info">Add Bookmark</a>
    </div>
    <p></p>
    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Site</th>
                <th scope="col">URL</th>
                <th scope="col">Modify</th>
                <th scope="col">Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for bookmark in object_list %}
            <tr>
                <td>{{forloop.counter}}</td>
                <td><a href="{% url 'detail' bookmark.id %}">{{bookmark.site_name}}</a></td>
                <td><a href="{{bookmark.url}}" target="_blank">{{bookmark.url}}</a></td>
                <td><a href="{% url 'update' bookmark.id %}" class="btn btn-success btn-sm">Modify</a></td>
                <td><a href="{% url 'delete' bookmark.id %}" class="btn btn-danger btn-sm">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
```
```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_update.html #}
{% extends 'base.html' %}

{% block title %}Bookmark Update{% endblock %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Update" class="btn btn-info btn-sm">
    </form>
{% endblock %}
```
- 이상 부모-자식 템플릿 상속 작업 완성
  - 부모 템플릿 작성
  - 자식 템플릿 작성
    - 상속 선언
    - 제목 블럭
    - 내용 블럭
- 디자인은 전혀 변화 없음
### 4.3.2 부트스트랩 적용하기
- [부트스트랩](http://bootstrapk.com)
    - [CSS 프레임워크](https://catswhocode.com/css-frameworks/)의 일종
    - HTML 태그에 class 속성을 추가하는 방식만으로 다양한 CSS 기능을 활용
    - 부트스트랩 적용을 위하여 base.html 수정
    - [부트스트랩 Document](https://getbootstrap.com/docs/4.4/getting-started/introduction/)
- CSS 부트스트랩 4.4.1 (교재는 4.1.3)
```HTML {.line-numbers}
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
```
- JS
  - jquery 3.4.1 (교재는 3.3.1)
  - popper.js 1.16.0 (교재는 1.14.3)
  - bootstrap.min.js 4.4.1 (교재는 4.1.3)
```HTML {.line-numbers}
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
```
- CSS 1개, JS 3개를 base.html에 적용
```HTML {.line-numbers}
{# ch04_bookmark/templates/base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    {# <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"> #}
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    {% comment %}
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    {% endcomment %}
</head>
<body>
    {% block content %}

    {% endblock %}
</body>
</html>
```
- 목록 보기 페이지를 브라우즈하여 부트스트랩 효과 확인
  - 부트스트랩은 HTML 태그에 지정된 class 속성을 활용하여 디자인을 적용함
  - 이미 작성했던 템플릿에는 HTML 태그에 대한 class 속성이 적절하게 지정되어 있었음
- base.html body 태그 내부에 메뉴바 작성
```HTML {.line-numbers}
{# ch04_bookmark/templates/base.html #}
{# ... #}
<body>
<div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Django Bookmark</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                </li>
            </ul>
        </div>
    </nav>
    <p></p>
    <div class="row">
        <div class="col">
            {% block content %}
            {% endblock %}

            {% block pagination %}
            {% endblock %}
        </div>
    </div>
</div>
</body>
```
- 목록 보기 페이지를 브라우즈하여 메뉴바 확인
- pagination 블럭도 추가하였으니, 페이징 기능 구현 시도

### 4.3.3 페이징 기능 만들기
- 페이징 기능
  - 게시판 형태 웹 페이지에 필수적인 기능
  - 함수형 뷰에서는 페이징 기능 구현이 복잡하지만, 클래스형 뷰에서는 간단함
```PYTHON {.line-numbers}
# bookmark/views.py
class BookmarkListView(ListView):
    model = Bookmark
    paginate_by = 5  # 페이징 기능
```
- 페이지 당 5 건으로 지정했으므로, 북마크가 5개 넘도록 추가 등록하고, 목록 페이지 확인
  - 페이지에 5 건만 출력됨을 확인
  - 목록 페이지의 pagination 블럭에서 페이지 목록이 출력되도록 추가 작업
![ch04_list](https://user-images.githubusercontent.com/10287629/77892280-563d7b80-72ad-11ea-8cf5-a63ed464728e.png)

```HTML {.line-numbers}
{# bookmark/templates/bookmark/bookmark_list.html #}
{# ... #}
{% block pagination %}
    {% if is_paginated %}
    <ul class="pagination justify-content-center pagination-sm">
        {% if page_obj.has_previous %}
            <li class="page-item">
              <a class="page-link" href="{% url 'list' %}?page={{ page_obj.previous_page_number }}" tabindex="-1">Previous</a>
            </li>
        {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" tabindex="-1">Previous</a>
            </li>
        {% endif %}

        {% for object in page_obj.paginator.page_range %}
            <li class="page-item {% if page_obj.number == forloop.counter %}disabled{% endif %}">
                <a class="page-link" href="{{ request.path }}?page={{ forloop.counter }}">{{ forloop.counter }}</a>
            </li>
        {% endfor %}

        {% if page_obj.has_next %}
            <li class="page-item">
              <a class="page-link" href="{% url 'list' %}?page={{ page_obj.next_page_number }}">Next</a>
            </li>
        {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#">Next</a>
            </li>
        {% endif %}
    </ul>
    {% endif %}
{% endblock %}
```
- 페이징 기능
  - `page_obj.has_previous`가 참이면,
    "page-link" class로 지정된 'Previous' 버튼을 `{% url 'list' %}?page={{ page_obj.previous_page_number }}` 경로로 연결
  - `page_obj.has_next `가 참이면,
    "page-link" class로 지정된 'Next' 버튼을 `page-link" href="{% url 'list' %}?page={{ page_obj.next_page_number }}` 경로로 연결
  - `page_obj.paginator.page_range` 내부의 `object`에 대하여 반복
    - "page-link" class로 지정된 `forloop.counter`를 출력하고,
    - `{{ request.path }}?page={{ forloop.counter }}` 경로로 연결
- 부트스트랩을 CDN을 통하여 적용하였지만, 로컬 서버에 있는 정적 파일을 적용하는 방식을 배워야 함

### 4.3.4 정적(static) 파일 사용하기
- 정적 파일
  - 로컬 서버에 저장되어 있는 CSS, JS 또는 이미지 파일
  - 정적 파일을 저장하는 위치가 정해져 있음
    - 각 앱 폴더 하위의 static 폴더
      이 방법은 3장 투표 앱 튜토리얼의 15절에서 학습했음
    - 변경하려면 settings.py 파일에서 설정
        - 프로젝트 루트 밑의 static 폴더를 사용하는 방법을 학습할 예정
        - settings.STATICFILES_DIRS 변수 추가
        - 프로젝트 루트 밑의 static 폴더에 style.css 파일 추가
        - base.html에 style.css 적용
```PYTHON {.line-numbers}
# config/settings.py  # settings.STATICFILES_DIRS 변수 추가
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
```
```CSS {.line-numbers}
/* static/style.css */
body {
    width:100%;
}
```
```HTML {.line-numbers}
{# templates/base.html #}
{# 부트스트랩 CSS 적용한 라인 바로 밑에 #}
{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">
```
- 정적 파일이 잘 적용되었는지 확인
  - 목록 페이지를 브라우징하고, 페이지를 우측 마우스로 `검사` 메뉴 클릭하여 개발자 도구 표시
  - 개발자 도구에서 `Sources` 탭을 클릭하고,
    Page 부분에서 `static/style.css`파일을 클릭해서 내용이 표시되면 성공
  - 'Refused to apply style from 'http://127.0.0.1:8000/static/style.css' because its MIME type ('text/html') is not a supported stylesheet MIME type, and strict MIME checking is enabled.' 오류가 나면 실패
  - [예제로 배우는 파이썬 프로그래밍](http://pythonstudy.xyz/) 사이트의 [static](http://pythonstudy.xyz/python/article/314-Static-%ED%8C%8C%EC%9D%BC)

## 4.4 배포하기 - Pythonanywhere
- 웹 서비스를 제공할 수 있는 서버에 업로드하는 배포
### 4.4.1 깃허브 가입하기
- [깃허브 사이트](https://github.com/)에 무료 서비스 회원 가입
- 'bookmark' repository 생성
### 4.4.2 깃 설치 및 소스코드
- [Git SCM](https://git-scm.com)에서 'Download 2.26.0 for Windows' 클릭
- 다운로드된 설치 파일을 실행(교재 참조)
- 파이참 터미널에서 `git --version` 실행
- 로컬 서버의 work\ch04_bookmark 폴더에서 git 저장소 초기화
```bash {.line-numbers}
(vnv_dj) C:\work\ch04_bookmark>ls		# 깃 설치한 이후 유닉스 명령 사용 가능함
bookmark  config  db.sqlite3  manage.py
(vnv_dj) C:\work\ch04_bookmark>git init		# .git 폴더 생성됨
(vnv_dj) C:\work\ch04_bookmark>git config --global user.name <아이디>
(vnv_dj) C:\work\ch04_bookmark>git config --global user.email "<이메일>"
```
- .gitignore 파일(git 작업에서 배제할 파일/폴더)을 work\ch04_bookmark 폴더에서 수정
  - 만일 .gitignore 파일이 없다면 새로 생성
  - 깃으로 동기화할 작업에서 제외할 항목을 나열하면 됨
  - db.sqlite3를 동기화 작업에서 배제하는 이유는 뭘까?
  - db.sqlite3를 동기화 작업에서 배제하지 않으면 개발용 DB가 서버로 복제됨
```bash {.line-numbers}
*.pyc
*~
__pycache__
*.zip
.DS_Store
.idea
```
- 참고: 수업 영상을 녹화하던 시점에서는 `/static` 항목이 .ignore 파일에 포함되어 있었으나, 이를 삭제하였음

- settings.py 옵션 변경
```PYTHON {.line-numbers}
# config/settings.py
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False       # 이 부분은 True로 설정해도 배포 가능함

ALLOWED_HOSTS = ['*']  # 이 부분은 반드시 지정해야 배포 가능함!!!
```

- remote origin에 최초 push
```bash {.line-numbers}
(venv) C:\work>git status       		# 빨간 목록 출력
(venv) C:\work>git add --all .
(venv) C:\work>git status       		# 초록 목록 출력
(venv) C:\work>git commit -m "200414 Bookmark Service"
(venv) C:\work>git remote add origin https://github.com/<아이디>/bookmark.git
(venv) C:\work>git push -u origin master
```
### 4.4.3 파이썬 애니웨어 가입 및 배포
#### 4.4.3.1 파이썬 애니웨어 가입하기
- [파이썬 애니웨어](https://www.Pythonanywhere.com)에서 Beginner account 가입
#### 4.4.3.2 콘솔에서 배포 설정
- 콘솔에서 코드 복제, 가상환경 준비
```BASH {.line-numbers}
$ pwd                                                   # 현행 디렉토리 확인
/home/logistex20
$ git clone https://github.com/<userid>/bookmark.git    # 깃허브에서 복제
$ ls                                                    # 리스트 확인
README.txt  bookmark
$ cd bookmark                                           # 폴더 이동
~/bookmark $ virtualenv venv --python=python3.8  # 파이썬 3.8 지정한 가상환경 venv 생성
~/bookmark $ source venv/bin/activate            # 가상환경 venv 활성화
~/bookmark $ pip install django==3.0             # 가상환경 venv에 장고 3.0 설치
~/bookmark $ python --version               # 파이썬 버전 확인
Python 3.8.0
~/bookmark $ django-admin.py version        # 장고 버전 확인
3.0
# db.sqlite3 파일이 이미 복제되었으므로 아래 두 작업은 생략
# ~/bookmark $ python manage.py migrate
# ~/bookmark (master)$ python manage.py createsuperuser
```
#### 4.4.3.3 웹 앱 설정
- 콘솔 화면의 햄버거 메뉴에서 web을 선택하여 웹 탭으로 이동
- 웹 탭에서 `Add a new web app` 버튼 클릭하고,
- 'Your web app's domain name'에서 Next 버튼 클릭하고,
- 'Select a Python Web framework'에서 'Manual configuarion (including virtualenvs)' 클릭하고,
- 'Select a Python version'에서 'Python 3.8' 클릭하고,
- 'Manual Configuration'에서 Next 버튼 클릭하고,
- WSGI 설정을 위해서, 'WSGI configuration file:/var/www/<id>_pythonanywhere_com_wsgi.py' 링크 클릭하여
- `/var/www/<id>_pythonanywhere_com_wsgi.py` 편집창에 다음 WSGI 코드를 입력하고 save
```PYTHON {.line-numbers}
import os
import sys
path = "/home/<id>/bookmark"     # 본인 <id>로 수정
if path not in sys.path:
    sys.path.append(path)

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = StaticFilesHandler(get_wsgi_application())

```

- 가상환경 연결
  - 웹 탭의 `Virtualenv:` 섹션에서
      `Enter path to a virtualenv, if desired` 링크 클릭하고,
      `/home/<id>/bookmark/venv` 입력하고 체크 버튼 클릭
  - 웹 탭에서 `Reload <id>.Pythonanywhere.com` 버튼 클릭
  - <id>.Pythonanywhere.com/bookmark 브라우징 및 테스트

- 파이썬 애니웨어 서버에서는
  - settings.ALLOWED_HOSTS 변수를
    `ALLOWED_HOSTS = ['*']`로 반드시 지정해야 오류를 피할 수 있음
  - 파이썬 애니웨어 Files 메뉴에서
    bookmark/config/settings.py 파일을 직접 수정해도 무방함

### 4.4.4 마무리
- 정적 파일 처리와 관련한 사항
  - 파이썬 애니웨어 서버에서 WSGI 파일 설정할 때, StaticFilesHandler를 사용했음
  - 장고 배포 상황에서는 정적 파일 핸들러를 사용하지 않기를 권장함
  - STATIC_ROOT 변수로 설정한 경로에 정적 파일을 모아 두고, 서비스하는 방식을 권장함
  - settings.STATIC_ROOT 추가
```PYTHON {.line-numbers}
# config/settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
```
- 로컬에서 깃허브로 보내기
```bash {.line-numbers}
(venv) C:\work>git status
(venv) C:\work>git add --all .               # 1. 추가 (명령줄 끝에 ".")
(venv) C:\work>git status
(venv) C:\work>git commit -m "add static_root"   # 2. 커밋
(venv) C:\work>git push                          # 3. 푸쉬 ()
```
- 깃허브에서 PythonAnywhere 서버로 pull
- 정적 파일 모으기 작업 수행
- 참고: 수업 녹화 당시에 이 내용이 없었으나 추가함
  - .ignore 파일에 `/static` 항목이 있는 상태에서는 해당 폴더의 내용이 깃 허브
    동기화 작업에서 배제됨
  - 따라서 아래와 같이 collectstatic 작업을 수행하면
    'FileNotFoundError: [Errno 2] No such file or directory' 오류가 발생함
  - .ignore 파일에서 `/static` 항목을 삭제하고 다시 깃 허브 동기화 작업을 수행하면 해결됨

```bash {.line-numbers}
(venv) ~ $ cd bookmark
(venv) ~/bookmark (master)$ git pull
(venv) ~/bookmark (master)$ python manage.py collectstatic
```
- 참고: 아래 내용은 파이썬 애니웨어 콘솔에서 `git pull` 작업 수행 도중 10번 행과 같은 오류가 발생하여, `git stash` 작업 등을 통하여 이를 해결하는 과정을 보여주기 위하여 참고로 제시함
```bash {.line-numbers}
(venv) 13:20 ~/bookmark (master)$ git pull
remote: Enumerating objects: 13, done.
remote: Counting objects: 100% (13/13), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 9 (delta 4), reused 9 (delta 4), pack-reused 0
Unpacking objects: 100% (9/9), done.
From https://github.com/logistex/bookmark
   653ed40..4cb81ea  master     -> origin/master
Updating 40c4752..4cb81ea
error: Your local changes to the following files would be overwritten by merge:
        config/settings.py
Please, commit your changes or stash them before you can merge.
Aborting
(venv) 13:31 ~/bookmark (master)$ git pull https://github.com/logistex/bookmark.git
From https://github.com/logistex/bookmark
 * branch            HEAD       -> FETCH_HEAD
Updating 40c4752..4cb81ea
error: Your local changes to the following files would be overwritten by merge:
        config/settings.py
Please, commit your changes or stash them before you can merge.
Aborting
(venv) 13:33 ~/bookmark (master)$ git stash
*** Please tell me who you are.
Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
to set your account's default identity.
Omit --global to set the identity only in this repository.
fatal: empty ident name (for <logistex2020@8e86bfb0e784>) not allowed
Cannot save the current index state
(venv) 13:33 ~/bookmark (master)$ git config --global user.email "logistex@naver.com"
(venv) 13:33 ~/bookmark (master)$ git config --global user.name "logistex"
(venv) 13:34 ~/bookmark (master)$ git stash
Saved working directory and index state WIP on master: 40c4752 200414 Bookmark Service
HEAD is now at 40c4752 200414 Bookmark Service
(venv) 13:34 ~/bookmark (master)$ git pull
Updating 40c4752..4cb81ea
Fast-forward
 .gitignore         | 1 -
 config/settings.py | 4 ++--
 config/urls.py     | 2 ++
 static/style.css   | 4 ++++
 4 files changed, 8 insertions(+), 3 deletions(-)
 create mode 100644 static/style.css
(venv) 13:34 ~/bookmark (master)$ python manage.py collectstatic
131 static files copied to '/home/logistex2020/bookmark/static_files'.
(venv) 13:35 ~/bookmark (master)$
```

- PythonAnywhere 서버 웹 탭의 Static files 섹션에서
  - URL을 '/static/'으로
  - Directory를 `home/<id>/bookmark/static_files/`로 입력
- PythonAnywhere 서버 웹 탭의 WSGI 파일도 수정
  - StaticFilesHandler 임포트 문장 삭제
  - StaticFileHandler() 호출 부분 삭제
```PYTHON {.line-numbers}
import os
import sys
path = "/home/<id>/bookmark"     # 본인 <id>로 수정
if path not in sys.path:
  sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.setiings")
application = get_wsgi_application()
```
- 웹 앱 새로고침 버튼을 클릭해서 테스트
- [배포 완성된 결과](http://logistex2020.pythonanywhere.com/)

- 보고서 과제 (10점)
    - (2점) 파이썬 애니웨어 서버로 북마크 앱 배포
        - 파이썬 애니웨어 서버에 배포된 북마트 목록 보기 페이지 제시
        - 브라우저 주소 창에서 파이썬 애니웨어 주소 확인 가능해야 함
    - (2점)북마크 목록 보기 페이지에서 페이징 기능의 작동 증빙
        - 목록 보기 첫 페이지의 모습을 제시하고(, 다음 페이지 보기 단추를 눌러 나타난)
        - 목록 보기 다음 페이지의 모습을 제시하고(, 이전 페이지 보기 단추를 눌러 나타난)
        - 목록 보기 이전 페이지의 모습을 제시
    - (1점)북마크 상세 보기 페이지
        - 목록 보기 페이지에서 특정 북마크 링크를 클릭하여 나타난
        - 상세 보기 페이지 모습을 제시
    - (1점)북마크 등록 기능의 작동 증빙
        - 등록 전 목록 보기 페이지에서 등록 버튼을 클릭하여
        - 목록 보기 페이지에 추가된 모습을 제시
    - (1점)북마크 수정 기능의 작동 증빙
        - 수정 전 목록 보기 페이지에서 수정 버튼을 클릭하여
        - 목록 보기 페이지에 수정된 모습을 제시
    - (1점)북마크 삭제 기능의 작동 증빙
        - 삭제 전 목록 보기 페이지에서 삭제 버튼을 클릭하여
        - 목록 보기 페이지에 삭제된 모습을 제시
    - (2점)웹 사이트 루트 페이지 연결
        - `http://127.0.0.1:8000` 경로로 접속해도 북마크 목록 페이지가 보이도록 수정
        - 수정된 config/urls.py 파일을 제시
        - 힌트: config/urls.py 파일에 두 행을 추가하면 된다.

![](https://user-images.githubusercontent.com/10287629/77262285-47b4fa00-6cd8-11ea-8848-35043d1cf46d.png)
