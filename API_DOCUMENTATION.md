# API Документация Глас

## Базовый URL

```
http://localhost:8000/api/v1
```

## Аутентификация

Большинство endpoints требуют JWT токен в заголовке:

```
Authorization: Bearer <token>
```

## Endpoints

### Аутентификация

#### Регистрация
```
POST /auth/register
```

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Иван Иванов",
  "phone": "+79001234567"
}
```

**Ответ:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Иван Иванов",
  "role": "citizen",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Вход
```
POST /auth/login
```

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Ответ:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Иван Иванов"
  }
}
```

#### Получение текущего пользователя
```
GET /auth/me
```

**Требуется:** Аутентификация

**Ответ:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Иван Иванов",
  "role": "citizen"
}
```

### Обращения

#### Создание обращения
```
POST /appeals
```

**Требуется:** Аутентификация

**Тело запроса:**
```json
{
  "title": "Яма на дороге",
  "description": "Большая яма на улице Ленина, дом 10",
  "category": "roads",
  "latitude": 55.7558,
  "longitude": 37.6173,
  "address": "Москва, ул. Ленина, 10"
}
```

**Ответ:** `201 Created`
```json
{
  "id": 1,
  "title": "Яма на дороге",
  "description": "Большая яма на улице Ленина, дом 10",
  "category": "roads",
  "status": "pending",
  "priority": "medium",
  "latitude": 55.7558,
  "longitude": 37.6173,
  "address": "Москва, ул. Ленина, 10",
  "district": "Центральный",
  "ai_summary": "Проблема с дорожным покрытием",
  "ai_sentiment": "negative",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Получение списка обращений
```
GET /appeals?page=1&size=20&status=pending&category=roads
```

**Требуется:** Аутентификация

**Параметры запроса:**
- `page` (int, default: 1) - номер страницы
- `size` (int, default: 20) - размер страницы
- `status` (string, optional) - фильтр по статусу
- `category` (string, optional) - фильтр по категории

**Ответ:** `200 OK`
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

#### Получение обращения по ID
```
GET /appeals/{appeal_id}
```

**Требуется:** Аутентификация

**Ответ:** `200 OK`
```json
{
  "id": 1,
  "title": "Яма на дороге",
  ...
}
```

#### Обновление обращения
```
PATCH /appeals/{appeal_id}
```

**Требуется:** Аутентификация (только администраторы)

**Тело запроса:**
```json
{
  "status": "in_progress",
  "priority": "high",
  "department_id": 1
}
```

### Департаменты

#### Получение списка департаментов
```
GET /departments
```

**Ответ:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Департамент дорожного хозяйства",
    "description": "Ответственен за дороги",
    "email": "roads@city.ru",
    "phone": "+79001234567"
  }
]
```

### Аналитика

#### Получение статистики дашборда
```
GET /analytics/dashboard?days=30
```

**Требуется:** Аутентификация (только администраторы)

**Параметры запроса:**
- `days` (int, default: 30) - период в днях

**Ответ:** `200 OK`
```json
{
  "total_appeals": 1000,
  "appeals_by_status": {
    "pending": 50,
    "in_progress": 30,
    "resolved": 900,
    "rejected": 20
  },
  "appeals_by_category": {
    "roads": 300,
    "lighting": 200,
    ...
  },
  "average_resolution_time": 24.5,
  "resolution_rate": 90.0,
  "appeals_timeline": [...],
  "top_districts": [...],
  "sentiment_distribution": {
    "positive": 100,
    "negative": 800,
    "neutral": 100
  }
}
```

## Коды статусов

- `200 OK` - Успешный запрос
- `201 Created` - Ресурс создан
- `400 Bad Request` - Неверный запрос
- `401 Unauthorized` - Требуется аутентификация
- `403 Forbidden` - Недостаточно прав
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Ошибка сервера

## Ошибки

Все ошибки возвращаются в формате:

```json
{
  "detail": "Описание ошибки"
}
```

## Интерактивная документация

После запуска проекта доступна интерактивная документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

