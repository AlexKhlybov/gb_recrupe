# RECRUPE - работа есть всегда!

### Установка и запуск проекта

Клонируем репозиторий и переходим в корень проекта
```
git clone https://github.com/AlexKhlybov/gb_recrupe.git
cd ./gb_recrupe
```

Устанавливаем окружение
```
python3 -m venv venv
```

Активируем окружение
```
source ./venv/bin/activate  # MacOs, Linux
venv\Scripts\activate  #Windows
```

Устанавливаем зависимости
```
pip install -r requirements.txt
```

Выполнение миграций
```
python.exe manage.py migrate
```

Заполнение БД тестовыми данными (у всех созданных пользователей пароль - 1)
```
python.exe manage.py dbinit
```

Запускаем проект и радуемся
```
python manage.py runserver
```