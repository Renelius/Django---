# Доска объявлений на django

## О проекте

Доска объявлений выполненная на django версии 3.0, python 3.8. С bootstrap4 для фронта и Postgresql.
Основной проекта является приложение bboard, имеющего следующий функционал:

- Возможность просматривать все объявления пользователей, поиск по объявлениям;
- создавать свои объявления, редактировать, удалять, добавлять изображения, оставлять комментарии;
- система регистации с последующей проверкой почты, посредством отправки письма с сылкой для активации;
- возможность авторизации с помощью социальных сетей, гугл капча, возможность смены пароля в профиле;

Так же существует приложение api, написанное с помощью djangorestframework, которое предоставляет
програмный интерфейс для работы сторонних программ. Имеет следущий функционал:

- Возможность просматривать все объявления, редактировать их, создавать и удалять;
- Возможность просматривать все рубрики, редактировать их, создавать и удалять;
- Возможность просматривать и добавлять комментарии;


## Установка

В виртуальном окружении (virtualenv) выполнить данную команду:
```
pip install -r requirements.txt
```
Далее запустить сервер командой:
```
python manage.py runserver
```
или
```
./manage.py runserver
```


## Автор

* **Толстых Кирилл**