# YaTube - социальная сеть, блог
--------------------------------
## Описание проекта
```
Социальная сеть с формой авторизации по электронной почте. 
Постам можно присвоить категорию (группу).
Присутствует возможность подписки на понравившихся авторов

```
## Технологии

```
- Python
- Django framework
- HTML
- CSS (Bootstrap 3)
```

## Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/viserdi/hw05_final.git
```

```
cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
