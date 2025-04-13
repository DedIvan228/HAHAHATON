# Демо-проект к хакатону МШП 2025. Трек WEB (Django)

- Команда: ... # вставьте название своей команды
- Участники: ... # вставьте имена участников

---

## Установка и запуск

1. Сделайте форк этого репозитория

2. Клонируйте репозиторий на свой компьютер:
```bash
git clone https://gitlab.informatics.ru/<...>/tg_start_project.git
cd tg_start_project
```
3. Создайте и активируйте виртуальное окружение:
```bash
# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate 

# Windows
python -m venv .venv
.\.venv\Scripts\activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. Подготовьте базу данных к работе
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Запустите сервер
```bash
python manage.py runserver
```

---

## Полезные ресурсы

- [Документация Django](https://docs.djangoproject.com/en/5.1/)

- [Документация Django REST framework (если используется)](https://www.django-rest-framework.org/)

- [Документация Python](https://docs.python.org/3/)

- [Документация по шаблонам Django](https://docs.djangoproject.com/en/5.1/topics/templates/)

## Проблемы

> Что делать, если `Port is already used`?

```bash
fuser -k 8000/tcp
```

> Не работают static файлы

1. Проверьте в `settings.py` наличие `STATIC_DIRS` и `STATIC_URL`
2. Проверьте путь до папки
3. В шаблоне необходимо прописать `{% load static %}`
4. В пути изображения испольуется функция `{% static 'path/to/img' %}`

> Создать суперпользователя

```bash
python manage.py createsuperuser
```

> Server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none

На уровне системы
```bash
git config --global http.sslverify false
```

На уровне терминала
```bash
export GIT_SSL_NO_VERIFY=1
```

## Проверка качества кода

```bash
pip install pylint
pylint --disable=C0114,R0903,C0116,C0115,R0901 **/*.py
```