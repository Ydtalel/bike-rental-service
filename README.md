# Bike Rental Service

## Описание
Bike Rental Service - это приложение для аренды велосипедов, разработанное с    
использованием Django и Django Rest Framework. 

## Инструкции по развертыванию и локальному запуску проекта

### Предварительные требования
Убедитесь, что у вас установлен Docker


### Шаги для развертывания

1. Клонируйте репозиторий проекта:
    ```
    git clone https://github.com/Ydtalel/bike-rental-service.git
    ```
   `cd bike-rental-service`

2. Постройте и запустите контейнеры:
    ```
    make build
    ```

3. Примените миграции базы данных:
    ```
    make migrate
    ```

4. Остановите все запущенные контейнеры:
    ```
    make stop
    ```
5. Запуск тестов
   ```
   make tests
   ```

### Шаги для локального запуска

1. Клонируйте репозиторий проекта:
    ```
    git clone https://github.com/Ydtalel/bike-rental-service.git
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```
    python -m venv .venv
    source .venv/bin/activate  # Для Windows используйте ".venv\Scripts\activate"
    ```

3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

4. Примените миграции базы данных:
    ```
    python manage.py migrate
    ```

5. Запустите сервер разработки:
    ```
    python manage.py runserver
    ```

6. Откройте браузер и перейдите по адресу `http://localhost:8000/swagger/` для доступа к приложению.

## Примеры запросов для тестирования API
### Cоздать пользователя  
POST   
http://localhost:8000/api/accounts/register/   
BODY
```
{
  "username": "foo",
  "email": "foo@example.com",
  "password": "bar"
}
```
ОТВЕТ CODE 201
```
{
    "id": 1,
    "email": "foo@example.com",
    "username": "foo"
}
```

### Вход в систему
POST    
http://localhost:8000/api/accounts/login/   
```
{
    "email": "foo@example.com",
    "password": "bar"
}
```
ОТВЕТ  CODE 200
```
{
    "email": "foo@example.com",
    "tokens": {
        "refresh": "refreshtoken",
        "access": "accesstoken"
    }
}
```
### Далее полученный токен следует использовать при запросах
### Получить список всех пользователей
GET  
http://localhost/api/rentals/users/  
Ответ CODE 200  
```
[
    {
        "id": 1,
        "email": "admin@example.com",
        "username": "admin"
    }
]
```
### Получить список всех велосипедов
GET  
http://localhost/api/rentals/bicycles/  
Ответ CODE 200  
```
[
    {
        "id": 1,
        "name": "Bike",
        "is_available": true
    },
    {
        "id": 2,
        "name": "Bike-2",
        "is_available": true
    }
]
```

### Получить информацию о конкретном велосипеде
GET   
http://localhost/api/rentals/bicycles/{id}  
Ответ CODE 200  

```
{
    "id": 1,
    "name": "Bike",
    "is_available": true
}
```
### Создать новый заказ аренды
POST   
http://localhost/api/rentals/rentals/   
BODY   

```
{
    "bicycle": 1,
    "start_time": "2024-07-04T04:54:28.269082Z",
    "end_time": null
}
```
Ответ CODE 201   

```
{
    "id": 1,
    "user": 1,
    "bicycle": 1,
    "start_time": "2024-07-06T10:16:30.487893Z",
    "end_time": null,
    "cost": null
}
```
### Завершить аренду
PUT  
http://localhost:8000/api/rentals/rentals/{id}/   
Ответ CODE 200  

```
{
    "id": 1,
    "user": 1,
    "bicycle": 1,
    "start_time": "2024-07-06T10:16:30.487893Z",
    "end_time": "2024-07-06T10:19:10.605714Z",
    "cost": "100.00"
}
```
### Получить список всех заказов аренды
GET  
http://localhost/api/rentals/rentals/  
Ответ CODE 200  

```
[
    {
        "id": 1,
        "user": 1,
        "bicycle": 1,
        "start_time": "2024-07-06T10:16:30.487893Z",
        "end_time": null,
        "cost": null
    }
]
```

### Полный список эндпоинтов и подробное описание аргументов доступно тут http://localhost:8000/swagger/