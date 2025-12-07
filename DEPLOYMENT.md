# Руководство по развертыванию проекта Глас

## Предварительные требования

- Docker и Docker Compose установлены
- Минимум 4GB RAM
- 20GB свободного места на диске

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd Voice
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Обязательно измените:
- `JWT_SECRET` - на случайную строку (минимум 32 символа)
- `OPENAI_API_KEY` - ваш ключ OpenAI API
- `MAP_API_KEY` - ключ для карт (опционально)

### 3. Запуск через Docker Compose

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL базу данных
- Redis
- Backend API (FastAPI)
- Frontend (Next.js)

### 4. Создание администратора

```bash
docker-compose exec backend python scripts/create_admin.py
```

По умолчанию создается администратор:
- Email: `admin@glas.ru`
- Password: `admin123`

**ВАЖНО:** Смените пароль после первого входа!

### 5. Доступ к приложению

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Документация: http://localhost:8000/docs

## Продакшн развертывание

### 1. Настройка доменов

Обновите `CORS_ORIGINS` и `ALLOWED_HOSTS` в `.env`:

```env
CORS_ORIGINS=["https://yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com"]
ENVIRONMENT=production
```

### 2. SSL сертификаты

Используйте nginx или другой reverse proxy с SSL:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. База данных

Для продакшна рекомендуется использовать управляемую БД (AWS RDS, Google Cloud SQL и т.д.).

Обновите `DATABASE_URL` в `.env`:

```env
DATABASE_URL=postgresql://user:password@db-host:5432/glas_db
```

### 4. Бэкапы

Настройте регулярные бэкапы PostgreSQL:

```bash
# Пример cron задачи для ежедневного бэкапа
0 2 * * * docker-compose exec -T postgres pg_dump -U glas_user glas_db > /backups/glas_$(date +\%Y\%m\%d).sql
```

### 5. Мониторинг

Рекомендуется настроить:
- Логирование (ELK Stack, Loki)
- Мониторинг (Prometheus, Grafana)
- Алерты (PagerDuty, Opsgenie)

## Масштабирование

### Горизонтальное масштабирование

Для увеличения производительности можно запустить несколько инстансов:

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
  frontend:
    deploy:
      replicas: 2
```

### Kubernetes

Конфигурации для Kubernetes находятся в директории `k8s/` (создайте при необходимости).

## Обновление

```bash
# Остановка
docker-compose down

# Обновление кода
git pull

# Пересборка
docker-compose build

# Запуск
docker-compose up -d

# Миграции БД (если есть)
docker-compose exec backend alembic upgrade head
```

## Устранение неполадок

### Проблемы с подключением к БД

```bash
# Проверка статуса
docker-compose ps

# Логи
docker-compose logs postgres
docker-compose logs backend
```

### Очистка данных

```bash
# Остановка и удаление контейнеров
docker-compose down -v
```

## Безопасность

1. **Всегда** меняйте дефолтные пароли
2. Используйте сильные JWT секреты
3. Настройте firewall
4. Регулярно обновляйте зависимости
5. Используйте HTTPS в продакшне
6. Настройте rate limiting
7. Регулярно делайте бэкапы

## Поддержка

При возникновении проблем создайте Issue в репозитории проекта.

