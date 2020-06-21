### 6.6 소셜 로그인 기능 추가
- 가상환경에 django-allauth 설치
```SHELL {.line-numbers}
$ conda install django-allauth
```
- config/settings.py 파일에 앱 등록
```PYTHON {.line-numbers}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'shop',
    'django.contrib.sites',						# allauth 사이트 활용을 위해서
    'allauth',									# allauth 앱
    'allauth.account',							# 계정관리
    'allauth.socialaccount',					# 소셜 계정 관리
    'allauth.socialaccount.providers.naver',	# 네이버 계정 연동
]
# ...
# 파일 맨 끝에 추가
# 장고 인증은 사용자 이름을 쓰지만, allauth 인증은 이메일을 사용
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',			# 장고 방식 인증
    'allauth.account.auth_backends.AuthenticationBackend',	# allauth 인증
)
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
```
- config/urls.py 파일에 로그인 접속 경로 추가
```PYTHON {.line-numbers}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # !!!
    path('', include('shop.urls'))
]
```
- 추가한 앱을 위하여 DB 현행화 하면,
  - onlineshop DB에 'account_~' 및 'socialaccount_~' 테이블 다수 추가됨
  - 현재 상태에서도 기본 로그인/로그아웃은 작동함
```SHELL {.line-numbers}
$ python manage.py migrate
```
- templates/base.html 파일에서 '카트 요약 정보' 직전에 '로그인/로그아웃 메뉴' 추가
```HTML {.line-numbers}
<!-- 로그인/로그아웃 -->
<li class="nav-item">
{% if user.is_authenticated %}
	<a class="nav-link" href="{% url 'account_logout' %}">Logout</a> <!-- allauth 앱의 경로 이름 -->
{% else %}
	<a class="nav-link" href="{% url 'account_login' %}">Login</a>   <!-- allauth 앱의 경로 이름 -->
{% endif %}
</li>
<!-- 카트 요약 정보 -->
```
<그림> http://localhost:8000/accounts/logout/ 접속 화면
![ch06_53_logout](https://user-images.githubusercontent.com/10287629/82188142-60ccd680-9928-11ea-8a50-81b7982a99ee.png)
<그림> http://localhost:8000/accounts/login/ 접속 화면
![ch06_54_login](https://user-images.githubusercontent.com/10287629/82188318-ab4e5300-9928-11ea-9e49-c131d997f2a1.png)
<그림> http://localhost:8000/accounts/signup/ 접속 화면
![ch06_55_signup](https://user-images.githubusercontent.com/10287629/82188514-f4060c00-9928-11ea-91f5-2b24212b0816.png)
- 네이버 아이디로 로그인 기능 추가
  - [네이버 개발자 사이트](https://developers.naver.com/products/login/api) 접속

<그림 > 네이버 개발자 사이트에서 '오픈 API 이용 신청' 클릭
![ch06_90_naver](https://user-images.githubusercontent.com/10287629/82216289-b8346c00-9953-11ea-878f-9281a3c93e47.png)

<그림 > 애플리케이션 등록 (API 이용 신청)
![ch06_91_request_api](https://user-images.githubusercontent.com/10287629/82216883-8d96e300-9954-11ea-9280-8572c32b5141.png)
- 애플리케이션 이름: '장고 온라인 쇼핑몰'
- 사용 API에서 '선택하세요' 부분은 무시하고, '네아로 (네이버 아이디로 로그인)' 부분에서
  회원이름 및 이메일 필수 부분에 체크
- '로그인 오픈 API 서비스 환경' 부분에서 '환경추가' 선택 박스에서 'PC 웹' 선택하고, 다음 URL 입력
	- 서비스 URL: http://127.0.0.1:8000
	- Callback URL: http://127.0.0.1:8000/accounts/naver/login/callback/
	- Callback URL 끝에 '/' 포함됨에 유의
- '등록하기' 버튼 클릭하면 나타나는 페이지에서 다음 두 항목 값을 메모장 등에 복사해 두기
	- Client ID
	- Client Secret

- <그림> 네이버 개발자 페이지에서 '네이버 아이디로 로그인' 작업 완료 상태 확인
  - 네이버 개발자 페이지에서 '내 애플리케이션' 메뉴를 클릭하여 등록된 '내 애플리케이션'을 확인
  - 현재 두 개 애플리케이션이 등록된 상태이고, 
    각각 '애플리케이션 명', 'Client ID' 및 'Client Secret' 값이 다르게 등록되어 있음

![ch06_30_nv_myapp](https://user-images.githubusercontent.com/10287629/82853026-7309ce80-9f3f-11ea-83ed-5ec0cd97a64e.png)

- 관리자 페이지에서 소셜 로그인 관련 작업을 진행
 
<그림> 관리자 화면에서 '소셜 어플리케이션' 항목의 '+ 추가' 버튼 클릭
![ch06_93_s_app](https://user-images.githubusercontent.com/10287629/82218741-4f4ef300-9957-11ea-8ee7-72cf2de49bc2.png)

<그림> 나타나는 '소셜 어플리케이션 추가' 화면에서 다음과 같이 입력
![ch06_94_add_s_app](https://user-images.githubusercontent.com/10287629/82219964-fd0ed180-9958-11ea-9cec-6d23db21a51f.png)
- 제공자: Naver
- 이름: 네이버 로그인
- 클라이언트 아이디: <네이버 API에서 발급받은 Client ID>
- 비밀 키: <네이버 API에서 발급받은 Client Secret>
- Sites 부분에서 '이용 가능한 sites' 부분에 보이는 'example.com' 항목을 '선택된 sites' 부분으로 옮기고,
- '저장' 단추 클릭

<그림> 관리자 화면에서 '소셜 어플리케이션' 클릭하여 등록된 '네이버 로그인' 확인
![ch06_94_added_s_app](https://user-images.githubusercontent.com/10287629/82289258-5a4d6600-99df-11ea-85ec-13c3701016a3.png)
- 지금 단계에서 관리자 화면의 상황
    - 소셜 어플리케이션 할목에는 직전 화면과 같이 '네이버 로그인'이 등록되어 있음
    - 소셜 계정 및 소셜 어플리케이션 토큰 항목에는 등록된 행이 없음
    - 아래 작업을 완료한 후 다시 확인하면, 
      소셜 계정 및 소셜 어플리케이션 토큰 항목에 등록된 행이 존재함
      
<그림> 우리 앱의 로그인 화면에서 'Naver' 링크 클릭하여 이용 동의하는 화면
![ch06_95_login](https://user-images.githubusercontent.com/10287629/82224565-f420fe80-995e-11ea-94da-d769e785f329.png)
- 일단 [로그아웃](http://127.0.0.1:8000/accounts/logout/)하고,
- 다시 [로그인](http://127.0.0.1:8000/accounts/login/) 화면에 접속하면 보이는 'Naver' 링크를 클릭하면
- '장고 온라인 쇼핑몰'에서 네이버 로그인 사용에 '동의하기' 단추 클릭 (최초 한 번만)

<그림> 로그인 직후, 메인 화면의 모습
![ch06_96_loggedin](https://user-images.githubusercontent.com/10287629/82289813-8c12fc80-99e0-11ea-82a7-d7b8b8256620.png)

<그림> 로그인 직후, 관리자 화면에서 사용자 조회하여 소셜 로그인으로 등록한 계정을 확인하는 화면
![ch06_97_loggedin_user](https://user-images.githubusercontent.com/10287629/82290002-deecb400-99e0-11ea-9e35-d82ee30e8187.png)
- logis: 장고 로그인 사용자
- logistex: 소셜 로그인 사용자

### 6.7 cart 앱 생성
#### 6.7.1 앱 생성
```SHELL {.line-numbers}
$ python manage.py startapp cart
```
- `settings.INSTALLED_APPS += 'cart',`
#### 6.7.2 카트 클래스 정의
- 상품 주문을 위해 일시적으로 저장하는 역할
  - DB에 저장하는 방식
  - 세션 기능을 활용하여 저장하는 방식
- cart/cart.py 작성
```PYTHON {.line-numbers}
from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self, request):
        # 장바구니 초기화 메소드 (request.session 변수에 저장)
        self.session = request.session
        cart = self.session.get(settings.CART_ID)  # CART_ID 변수는 settings.py 파일에서 정의
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart

    def __len__(self):
        # 장바구니의 상품별 수량에 대한 총계
        return sum(
            item['quantity'] for item in self.cart.values()
        )

    def __iter__(self):
        # 장바구니에 담긴 상품의 가격과 금액을 iterable 상태로 제공하는 메소드
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item  # https://tech.ssut.me/what-does-the-yield-keyword-do-in-python/

    def add(self, product, quantity=1, is_update=False):
        # 장바구니에 상품 추가
        product_id = str(product.id)
        if product_id not in self.cart:
            # 일단 수량을 0으로 초기화
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if is_update:  # 지정한 수량으로 수정
            self.cart[product_id]['quantity'] = quantity
        else:          # 지정한 만큼 수량 증가
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # 장바구니에 담긴 상품을 세션 변수로 저장
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        # 장바구니에서 특정 상품을 삭제
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()

    def clear(self):
        # 장바구니를 비우는 기능, 주문 완료 경우에도 사용
        self.session[settings.CART_ID] = {}
        # self.session['coupon_id'] = None
        self.session.modified = True

    def get_product_total(self):
        # 장바구니에 담긴 상품의 총 가격을 계산
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )
```
- config/settings.py 파일 끝에 변수 추가
```PYTHON {.line-numbers}
CART_ID = 'cart_in_session'
```
- cart/forms.py 카트에 상품을 추가하기 위한 폼 작성
  - 상품 상세 페이지에서는 지정한 수량만큼 증가되도록 is_update 값을 False로 설정
  - 장바구니 페이지에서는 지정한 수량으로 설정되도록 is_update 값을 True로 설정
```PYTHON {.line-numbers}
from django import forms

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False,
                                   widget=forms.HiddenInput)
```
- cart/views.py 파일
```PYTHON {.line-numbers}
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .forms import AddProductForm
from .cart import Cart


@require_POST
def add(request, product_id):  # 장바구니에 상품을 추가하는 뷰
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')


def remove(request, product_id):  # 장바구니에서 지정한 상품을 삭제하는 뷰
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def detail(request):  # 장바구니 페이지 뷰
    cart = Cart(request)
    for product in cart:  # 장바구니에 담긴 상품마다 (수량 수정 가능하도록) AddProductForm 생성
        product['quantity_form'] = AddProductForm(
            initial={'quantity': product['quantity'], 'is_update': True}
        )
    return render(request, 'cart/detail.html', {'cart': cart})
```
#### 6.7.4 접속경로 정의
- cart/urls.py 생성
```PYTHON {.line-numbers}
from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', detail, name='detail'),
    path('add/<int:product_id>', add, name='product_add'),
    path('remove/<int:product_id>', remove, name='product_remove'),
]
```
- config/urls.py 한 줄 추가
```PYTHON {.line-numbers}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('cart/', include('cart.urls')),  		# !!!
    path('', include('shop.urls')),
]
```
### 6.7.4 템플릿 정의
- cart/templates/cart/detail.html
```HTML {.line-numbers}
{% extends "base.html" %}
{% load static %}   <!--load 명령은 extends 보다는 뒤에!!!-->
{% load humanize %} <!--load 명령은 extends 보다는 뒤에!!!-->

{% block title %}
    Shopping cart
{% endblock %}

{% block content %}
    <h3>Shopping cart</h3>
    <table class="table table-striped">
        <thead>
            <tr>
                <th scope="col" style="width: 25%;">Image</th>
                <th scope="col">Product</th>
                <th scope="col">Quantity</th>
                <th scope="col">Remove</th>
                <th scope="col">Unit price</th>
                <th scope="col">Price</th>
            </tr>
        </thead>
        <tbody>
        {% for item in cart %}
            {% with product=item.product %}<!--with 명령-->
            <tr>
                <th scope="row">
                    <a href="{{ product.get_absolute_url }}">
                        <img src="{{ product.image.url }}" class="img-thumbnail" style="max-height: 90%; max-width: 90%">
                    </a>
                </th>
                <td>{{ product.name }}</td>
                <td>
                    <form action="{% url 'cart:product_add' product.id %}" method="post">
                        {% csrf_token %}
                        {{ item.quantity_form.quantity }}
                        {{ item.quantity_form.is_update }}
                        <div class="row-fluid">
                            <input type="submit" class="btn btn-primary pull-right form-control" value="Update">
                        </div>
                    </form>
                </td>
                <td><a href="{% url 'cart:product_remove' product.id %}">Remove</a></td>
                <td class="num">&#8361;{{item.price | floatformat:'0' | intcomma}}</td>
                <td class="num">&#8361;{{item.total_price | floatformat:'0' | intcomma}}</td>
            </tr>
            {% endwith %}
        {% endfor %}

            <tr class="total">
                <td>Total</td>
                <td colspan="4"></td>
                <td class="num">&#8361;{{cart.get_product_total | floatformat:'0' | intcomma}}</td>
            </tr>
        </tbody>
    </table>

    <p class="text-right">
        <a href='{% url "shop:product_all" %}' class="btn btn-secondary">Continue shopping</a>
    </p>
{% endblock %}
```
#### 6.7.5 상품 상세 페이지 수정
- shop.views.product_detail 함수 뷰에 장바구니에 담기 기능을 추가
```PYTHON {.line-numbers}
from cart.forms import AddProductForm                                       # !!!

def product_detail(request, id, product_slug=None):
    # 지정된 상품 객체를 상세 화면으로 전달
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})                   # !!!
    return render(request, 'shop/detail.html', {'product': product,
                                                'add_to_cart': add_to_cart})# !!!
```
- shop/templates/shop/detail.html 템플릿에 장바구니에 담기 기능을 추가
  - add_to_cart 내용을 출력
  - form의 action 속성을 'cart:product_add' 접속 경로로 지정
```HTML {.line-numbers}
<form action="{% url 'cart:product_add' product.id %}" method="post">  <!-- !!! -->
	{{add_to_cart}}                                                    <!-- !!! -->
	{% csrf_token %}
	<input type="submit" class="btn btn-primary btn-sm" value="Add to Cart">
</form>
```
- templates/base.html 템플릿의 메인 메뉴에 있는 카트 링크를 'cart:detail' 접속 경로로 연결
```HTML {.line-numbers}
<!-- 카트 요약 정보 -->
<li class="nav-item active">
	<a class="nav-link btn btn-outline-success" href="{% url 'cart:detail' %}">Cart:
		{% if cart|length > 0 %}
			&#8361;{{ cart.get_product_total | floatformat:'0' | intcomma }} ({{cart|length}} items)
		{% else %}
			Empty
		{% endif %}
	</a>
</li>
```
<그림> 장바구니 페이지의 모습
![ch06_98_cart](https://user-images.githubusercontent.com/10287629/82321199-710bb100-9a0f-11ea-9454-6f8ddbce39f7.png)

- 카트 요약 정보 개선
  - (cart.views.detail() 뷰가 cart 맥락변수를 전달한) cart/detail.html에서는
  	카트 요약 정보가 정확하게 표시됨
  - (cart 맥락변수를 전달받지 못한) shop/list.html 및 shop/detail.html에서는
    카트 요약 정보가 정확하지 않게 표시됨
  - shop/views.py 파일의 두 뷰에서 각 템플릿으로 cart 맥락 정보를 전달하도록 수정
```PYTHON {.line-numbers}
# ...
from cart.cart import Cart  # ***

def product_in_category(request, category_slug=None):
	# ...
    cart = Cart(request)
#	return render(request, 'shop/list.html', {...,
                                               'cart': cart})

def product_detail(request, id, product_slug=None):
	# ...
	cart = Cart(request)
#	return render(request, 'shop/detail.html', {...,
											'cart': cart})
```
### 6.8 쿠폰 앱 생성
#### 6.8.1 앱 생성
```SHELL {.line-numbers}
$ python manage.py startapp coupon
```
- `settings.INSTALLED_APPS += 'coupon',`
#### 6.8.2 모델 정의
- coupon/models.py
```PYTHON {.line-numbers}
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  # 쿠폰 사용할 때 입력할 코드
    use_from = models.DateTimeField()                    # 쿠폰 사용 시작 시점
    use_to = models.DateTimeField()                      # 쿠폰 사용 종료 시점
    amount = models.IntegerField(                        # 할인 금액 (최대/최소 제약)
        validators=[MinValueValidator(0), MaxValueValidator(100000)])
    active = models.BooleanField()						 # True인 쿠폰만 유효함

    def __str__(self):
        return self.code
```
- 모델 DB 현행화
```SHELL {.line-numbers}
$ python manage.py makemigrations coupon
$ python manage.py migrate coupon
```
#### 6.8.3 뷰 정의
- coupon/forms.py
```PYTHON {.line-numbers}
from django import forms


class AddCouponForm(forms.Form):  # 쿠폰 번호 입력하는 폼
    code = forms.CharField(label='Your Coupon Code')
```
- coupon/views.py
```PYTHON {.line-numbers}
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm


@require_POST
def add_coupon(request):  # 입력받은 쿠폰 코드로 쿠폰을 조회
    now = timezone.now()
    form = AddCouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(  # iexact로 대소문자 구분 없이
                code__iexact=code,        # use_from <= now <= use_to
                use_from__lte=now, use_to__gte=now, active=True)  # active=True
            request.session['coupon_id'] = coupon.id  # 쿠폰 id를 세션 변수로 저장
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:detail')  # 장바구니 보기로 리다이렉트
```
#### 6.8.4 접속 경로 정의
- coupon/urls.py
```PYTHON {.line-numbers}
from django.urls import path
from .views import add_coupon

app_name='coupon'

urlpatterns = [
    path('add/', add_coupon, name='add'),  # 쿠폰 추가
]
```
- config/urls.py 코드에 한 줄 추가
```PYTHON {.line-numbers}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('cart/', include('cart.urls')),
    path('coupon/', include('coupon.urls')),  # !!!
    path('', include('shop.urls')),
]
```
#### 6.8.5 카트 코드 수정
- cart/cart.py
```PYTHON {.line-numbers}
# ...
from coupon.models import Coupon


class Cart(object):
    def __init__(self, request):
        # 장바구니 초기화 메소드 (request.session 변수에 저장)
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')  # 카트에 쿠폰 id 변수 추가


# ...
def clear(self):
	# 장바구니를 비우는 기능, 주문 완료 경우에도 사용
	self.session[settings.CART_ID] = {}
	self.session['coupon_id'] = None  # 장바구니 비울 때, 쿠폰 정보도 삭제
	self.session.modified = True

# ...
@property  # 클래스 메소드를 클래스 속성 변수로 만들기 위하여
def coupon(self):
	if self.coupon_id:
		return Coupon.objects.get(id=self.coupon_id)
	return None

def get_discount_total(self):
	if self.coupon:
		if self.get_product_total() >= self.coupon.amount:
			return self.coupon.amount
	return Decimal(0)  # (구매총액 < 쿠폰금액)이면 할인금액은 0

def get_total_price(self):  # 할인 적용된 촘 금액 반환
	return self.get_product_total() - self.get_discount_total()
```
- cart/views.py
```PYTHON {.line-numbers}
# ...
from coupon.forms import AddCouponForm  # !!!
# ...

def detail(request):  # 장바구니 페이지 뷰
    cart = Cart(request)
    add_coupon = AddCouponForm()  # !!! AddCouponForm
    for product in cart:
        product['quantity_form'] = AddProductForm(
            initial={'quantity': product['quantity'], 'is_update': True}
        )
    return render(request, 'cart/detail.html', 				 # 폼을 템플릿에 전달하여 출력
                  {'cart': cart, 'add_coupon': add_coupon})  # !!! AddCouponForm
```
- cart/templates/cart/detail.html 코드에 2 블럭 추가
```HTML {.line-numbers}
<!-- ... -->
<!-- tbody 내부에서 for 반복 끝나는 지점 밑에, 할인 전 총액과 쿠폰 관련 서브 토탈 행을 추가-->
	{% if cart.coupon %}  <!-- 카트에 쿠폰이 있을 경우에만 쿠폰 관련 할인 정보를 출력 -->
		<tr class="subtotal">
			<td>Subtotal</td>
			<td colspan="4"></td>
			<td >&#8361;{{cart.get_product_total | floatformat:'0' | intcomma}}</td>
		</tr>
		<tr>
			<td colspan="5">"{{ cart.coupon.code }}" coupon (&#8361;{{cart.coupon.amount | floatformat:'0' | intcomma}}) discounted</td>
			<td>&#8361;{{cart.get_discount_total | floatformat:'0' | intcomma}}</td>
    	</tr>
	{% endif %}
		<tr class="total">
			<td>Total</td>
			<td colspan="4"></td>
			<td class="num">&#8361;{{cart.get_total_price | floatformat:'0' | intcomma}}</td>
		</tr>
	</tbody>
</table>
<!-- table 닫는 태그 직후, 쿠폰 입력 폼을 추가-->
<p>
	Add Coupon:
</p>
<form action='{% url "coupon:add" %}' method="post">
	{{ add_coupon }}
	<input type="submit" value="Add">
	{% csrf_token %}
</form>
<!-- ... -->
```
#### 6.8.6 관리자 페이지에 모델 등록
- coupon/admin.py
```PYTHON {.line-numbers}
from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','use_from','use_to','amount', 'active']
    list_filter = ['active','use_from','use_to']
    search_fields = ['code']


admin.site.register(Coupon,CouponAdmin)
```
- 서버 실행 후, 관리자 페이지에서 쿠폰 등록하고, 장바구니 페이지에서 적용
<그림 > 장바구니 페이지에서 쿠폰을 활용하여 할인이 적용된 모습
![ch06_99_coupon](https://user-images.githubusercontent.com/10287629/82332572-876e3880-9a20-11ea-90e3-7ca8aba4ea6a.png)
- 쿠폰 할인의 효과가 화면 상단의 쿠폰 요약 정보에도 반영되도록, base.html에서
  `{{cart.get_product_total}}`을 `{{cart.get_total_price}}`로 수정

### 6.9 order 앱 작성
#### 6.9.1 앱 생성
```SHELL {.line-numbers}
$ python manage.py startapp order
```
- `settings.INSTALLED_APPS += 'order',`
#### 6.9.2 모델 정의
- iamport 서비스로 결제 연동하기 위해서,
  - iamport 서비스 API를 사용하기 위한 함수를 미리 작성
  - 이를 위해 iamport 서비스에 가입
    - https://www.iamport.kr/ 접속하여, 우측 상단의 '대시보드' 버튼 클릭
    - 로그인 화면이 나오면, 우측 하단의 '회원 가입' 버튼 클릭
    - 회원 가입 창에서 관련 정보 입력하고 '등록하기' 버튼 클릭
  - 등록하면 관리자 페이지가 뜨는데, 여기서 '시스템 설정' 탭을 클릭
    - 'PG설정(일반결제 및 정기결제)' 탭을 클릭
    - '기본 PG사'의 'PG사'에 'KT이니시스(웹표준결제창)'을 선택하고,
      '테스트모드(Sandbox)'가 'ON'으로 된 상태에서,
      '전체 저장' 버튼을 클릭
  - '재 정보' 탭을 클릭하여 보이는 다음 정보를 메모장 등에 보관하고, settings.py에 입력
    - REST API 키
    - REST API secret:
- config/settings.py 파일에 import 정보 입력
```PYTHON {.line-numbers}
IAMPORT_KEY = '당신의-API-key'
IAMPORT_SECRET = '당신의-secret-key'
```
- order/iamport.py 파일에 아임포트 API 통신용 메소드 작성
```PYTHON {.line-numbers}
import requests
from django.conf import settings

def get_token():
    # iamport 서버와 통신하기 위한 토큰을 받아오는 함수
    access_data = {
        'imp_key': settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET,
    }
    url = "https://api.iamport.kr/users/getToken"
    # requests : 특정 서버와 http 통신을 하게 해주는 모듈
    req = requests.post(url, data=access_data)
    access_res = req.json()
    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None

def payments_prepare(order_id, amount, *args, **kwargs):
    # 결제를 준비하는 함수 - iamport에 주문번호와 금액을 미리 전송
    access_token = get_token()
    if access_token:
        access_data = {
            'merchant_uid': order_id,
            'amount': amount,
        }
        url = "https://api.iamport.kr/payments/prepare"
        headers = {'Authorization': access_token, }
        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()
        if res['code'] is not 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")

def find_transaction(order_id,*args,**kwargs):
    # 결제 완료를 확인해주는 함수 - 실 결제 정보를 iamport에서 가져옴
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/"+order_id
        headers = {'Authorization':access_token, }
        req = requests.post(url, headers=headers)
        res = req.json()
        if res['code'] is 0:
            context = {
                'imp_id': res['response']['imp_uid'],
                'merchant_order_id': res['response']['merchant_uid'],
                'amount': res['response']['amount'],
                'status': res['response']['status'],
                'type': res['response']['pay_method'],
                'receipt_url': res['response']['receipt_url'],
            }
            return context
        else:
            return None
    else:
        raise ValueError("토큰 오류")
```
- API 통신에서 사용하는 requests 패키지를 현재의 shop 가상환경에 설치
```SHELL {.line-numbers}
$ conda install requests
```
#### 6.9.3 모델 정의
- order/models.py
```PYTHON {.line-numbers}
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import hashlib
from .iamport import payments_prepare, find_transaction
from django.db.models.signals import post_save

from coupon.models import Coupon
from shop.models import Product


class Order(models.Model):  # Order:OrderItem = 일:다
    # 주문 정보를 저장하는 모델 (회원 정보를 외래키로 연결하지 않고, 저장하는 방식)
    first_name = models.CharField(max_length=50)        # 주문자 정보
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)          # 주소
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)   # 일시
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)           # 결제 여부
    coupon = models.ForeignKey(Coupon,                  # 쿠폰 정보
                               on_delete=models.PROTECT,
                               related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0,           # 할인 정보
                                   validators=[MinValueValidator(0),MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_product(self):  # (할인 전) 주문 총액(=단가*수량)
        return sum(
            item.get_item_price() for item in self.items.all())  # 자식 테이블에서 지정한 related_name

    def get_total_price(self):  # (할인 후) 주문 총액
        total_product = self.get_total_product()
        return total_product - self.discount


class OrderItem(models.Model):  # Order:OrderItem = 일:다, OrderItem:Product = 다:일
    # 주문 내역 정보
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 상품 테이블 단가와 별도로 저장
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_item_price(self):
        return self.price * self.quantity


class OrderTransactionManager(models.Manager):
    # OrderTransaction 모델의 관리자 클래스, 기본 관리자 클래스 objects 대신 사용
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 오류")
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        email_hash = str(order.email).split("@")[0]
        final_hash = hashlib.sha1((order_hash  + email_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = "%s"%(final_hash)  # 아임포트에 결제 요청할 때 고유한 주문번호가 요구됨
        payments_prepare(merchant_order_id,amount)
        tranasction = self.model(order=order, merchant_order_id=merchant_order_id, amount=amount)
        if success is not None:
            tranasction.success = success
            tranasction.transaction_status = transaction_status
        try:
            tranasction.save()
        except Exception as e:
            print("save error",e)
        return tranasction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None


class OrderTransaction(models.Model):
    # 결제 정보를 저장하는 모델
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)  # 정산 문제 확인 및 환불 처리 용도
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True,blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = OrderTransactionManager()  # 기본 관리자 클래스를 자작 관리자 클래스로 지정

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']


def order_payment_validation(sender, instance, created, *args, **kwargs):
    # (특정 기능의 수행을 장고 앱 전체에 알리는) 시그널을 활용한 결제 검증 함수
    if instance.transaction_id:
        import_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)
        merchant_order_id = import_transaction['merchant_order_id']
        imp_id = import_transaction['imp_id']
        amount = import_transaction['amount']
        local_transaction = OrderTransaction.objects.filter(
            merchant_order_id=merchant_order_id, transaction_id= imp_id, amount=amount).exists()
        if not import_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")

# 결제 정보가 생성된 후에 호출할 함수를 연결해준다.
post_save.connect(order_payment_validation, sender=OrderTransaction)
```
- DB 현행화
```SHELL {.line-numbers}
$ python manage.py makemigrations order
$ python manage.py migrate order
```
#### 6.9.4 뷰 정의
- order/forms.py 파일에 주문 정보 입력 폼 작성
```PYTHON {.line-numbers}
from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
```
- order/views.py 파일에 주문 생성 뷰 작성
```PYTHON {.line-numbers}
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View  # 결제를 위한 임포트
from django.http import JsonResponse        # 결제를 위한 임포트

from .models import *
from cart.cart import Cart
from .forms import *


def order_create(request):
    # 주문 입력 뷰, 결제 진행 후 주문 정보를 저장,
    # ajax 기능으로 주문서 처리하므로 주문서 입력용 폼 출력하는 경우를 제외하면,
    # 자바스크립트가 동작하지 않는 환경에서만 입력 정보를 처리하는 뷰
    cart = Cart(request)
    if request.method == 'POST':  # 서버로 정보가 전달되면
        form = OrderCreateForm(request.POST)  # 주문서 입력 폼 저장
        if form.is_valid():
            order = form.save()  # 폼을 저장
            if cart.coupon:  # 카트에 쿠폰이 있으면, 주문에 적용
                order.coupon = cart.coupon
                order.discount = cart.coupon.amount
                order.save()
            for item in cart:  # 카트의 모든 상품을 주문내역으로 생성
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()  # 카트 비우기
            return render(request, 'order/created.html', {'order': order})  # 저장된 주문 정보를 맥락 정보로 전달
    else:  # 사용자가 정보를 서버로 전달하지 않은 상태라면
        form = OrderCreateForm()  # 주문서 입력 폼 생성하고, 카트 및 폼을 템플릿으로 전달
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


# from django.contrib.admin.views.decorators import staff_member_required
# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'order/admin/detail.html', {'order':order})
#
# # pdf를 위한 임포트
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint
#
# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('order/admin/pdf.html', {'order':order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
#     return response


def order_complete(request):
    # ajax로 결제 후에 보여줄 결제 완료 화면
    order_id = request.GET.get('order_id')  # 서버로부터 주문번호를 얻어와서
    order = Order.objects.get(id=order_id)  # 이 주문번호를 이용해서 주문 완료 화면을 출력
    return render(request, 'order/created.html', {'order': order})


class OrderCreateAjaxView(View):  # Ajax 뷰
    # 입력된 주문 정보를 서버에 저장하고, 카트 상품을 OrderItem 객체에 저장하고, 카트 비우기
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 인증되지 않은 사용자라면 403 상태 반환
            return JsonResponse({"authenticated": False}, status=403)
        cart = Cart(request)                    # 카트 정보 획득
        form = OrderCreateForm(request.POST)    # 입력된 주문 정보 획득
        if form.is_valid():  # 폼이 정당하면
            order = form.save(commit=False)  # 폼을 메모리에서 저장
            if cart.coupon:                  # 쿠폰 정보 처리
                order.coupon = cart.coupon
                order.discount = cart.coupon.amount
            order = form.save()             # 폼 저장
            for item in cart:               # 카트를 OrderItem으로 저장
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()                    # 카트 비우기
            data = {"order_id": order.id}
            return JsonResponse(data)       # 주문번호를 반환
        else:   # 폼이 정당하지 않으면 401 상태 반환
            return JsonResponse({}, status=401)


class OrderCheckoutAjaxView(View):  # 결제 정보 OrderTransaction 객체 생성
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 인증되지 않은 사용자이면 403 상태 반환
            return JsonResponse({"authenticated":False}, status=403)
        order_id = request.POST.get('order_id')  # 입력된 주문번호 획득하여 주문 검색
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')      # 입력된 금액 획득
        try:  # 결제용 id 생성을 시도
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order, amount=amount)
        except:  # 결제용 id 생성 실패한 경우
            merchant_order_id = None
        if merchant_order_id is not None:  # 결제용 id 생성이 성공한 경우
            data = {"works": True, "merchant_id": merchant_order_id}
            return JsonResponse(data)
        else:  # 결제용 id 생성이 실패한 경우 401 상태 반환
            return JsonResponse({}, status=401)


class OrderImpAjaxView(View):  # 실제 결제 여부 확인
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 사용자 인증 실패이면 403 반환
            return JsonResponse({"authenticated": False}, status=403)
        order_id = request.POST.get('order_id')  # 주문번호 획득
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')  # 결제번호 획득
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')
        try:  # 결제 객체 검색 시도
            trans = OrderTransaction.objects.get(
                order=order, merchant_order_id=merchant_id, amount=amount)
        except:
            trans = None
        if trans is not None:  # 결제 객체 검색 성공이면
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            order.paid = True
            order.save()
            data = {"works": True}
            return JsonResponse(data)
        else:  # 결제 객체 검색 실패하면 401 반환
            return JsonResponse({}, status=401)
```
#### 6.9.5 접속 경로 정의
```PYTHON {.line-numbers}

```


```HTML {.line-numbers}
```

```HTML {.line-numbers}
```

```PYTHON {.line-numbers}
```


```PYTHON {.line-numbers}

```
```PYTHON {.line-numbers}
```
```PYTHON {.line-numbers}
```
