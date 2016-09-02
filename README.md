# django-todo-rest
[![Build Status](https://travis-ci.org/ad-lebedev/django-todo-rest.svg?branch=master)](https://travis-ci.org/ad-lebedev/django-todo-rest)
[![Coverage Status](https://coveralls.io/repos/github/ad-lebedev/django-todo-rest/badge.svg?branch=master)](https://coveralls.io/github/ad-lebedev/django-todo-rest?branch=master)
  
Web API сервер, реализующий базовый backend для приложений типа todomvc.  

Сервер поддерживает 2 механизма аутентификации:
* аутентификация на основе токенов [см. документацию по DRF](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
* двухфакторная аутентификация на основе [TOTP](https://ru.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) через Google Authenticator

### API endpoints
#### Служебные
```api-auth/``` - endpoint встроенной авторизации для Django REST Framework   
```auth-token/``` - endpoint для Token-based авторизации  
```auth-totp/register/``` - endpoint для регистрации двухфакторной аутентификации пользователя  
```auth-totp/login/``` - endpoint для двухфакторной авторизации  

#### Основные
```todo/``` - endpoint приложения TODO  
Полное описание API endpoint приложения - [API.md](API.md)
