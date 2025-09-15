# apple-ios-purchased-old-legacy-available-compatible-appstore-catalog-hub-index-archive-list-db

Пошуковий, регулярно оновлюваний каталог усіх платних продуктів Apple Store (додатки, ігри, фільми, книги, підкасти, апаратні аксесуари) з інформацією про ціну, мінімальну iOS‑версію, жанр, продавця та багато іншого.

📖 Зміст
Огляд
Фічі
Технічний стек
Як розгорнути локально
Використання API
Джерела даних
Контроль якості та CI/CD
Внесок у проєкт (Contributing)
Ліцензія
📦 Огляд
ios-purchased-catalog-hub – це відкритий сервіc з REST‑API, який надає готовий до використання каталог усіх платних товарів, доступних в Apple App Store, iTunes Store, Apple Books та Apple Store.

Не прив’язаний до жодного Apple ID – дані формуються лише з публічних API Apple.
Щоденне оновлення: скрипт‑колектор збирає нові товари, оновлює існуючі та зберігає їх у базі.
Підтримка фільтрації за типом продукту, мінімальною iOS‑версією, діапазоном цін, жанром, сумісними пристроями тощо.
Проєкт створено, щоб швидко отримати актуальну базу для аналітики, рекомендаційних систем, пошуку або власних маркетплейс‑проєктів.

✨ Фічі
№	Функція	Опис
1️⃣	Повний каталог	Понад 2 млн записів: iOS‑додатки, iPad‑додатки, Apple TV‑програми, iOS‑ігри, фільми, серіали, книги, підкасти, аксесуари.
2️⃣	Фільтрація	product_type, min_ios, price_max, genre, device (iPhone, iPad, Apple TV, Watch).
3️⃣	REST‑API	FastAPI‑сумісний, автоматичний Swagger UI (/docs).
4️⃣	CSV/JSON експорт	Параметр format=csv повертає файл готовий до імпорту в Excel, Google Sheets, BI‑системи.
5️⃣	Детальна мета‑інформація	price, currency, release_date, seller, supported_devices, raw_json (повний відповідь iTunes API).
6️⃣	Контейнеризація	Docker‑образ apple/ios‑purchased‑catalog‑hub (використовує Alpine + Python 3.12).
7️⃣	CI/CD	GitHub Actions: тестування, lint, автоматичне оновлення бази та пересборка образу щодня.
8️⃣	Документація	Auto‑генерована OpenAPI‑специфікація, а також розгорнутий README та API.md.
9️⃣	Локальна інсталяція	Один‑командний скрипт make run (Docker або без Docker).
🛠️ Технічний стек
Шар	Технологія
Мова	Python 3.12
Веб‑фреймворк	FastAPI (Starlette, Pydantic)
База даних	SQLite (для демо) / PostgreSQL (production)
ORM	SQLAlchemy 2.x
Збір даних	httpx + iTunes Search API (https://itunes.apple.com/search)
Контейнер	Docker (Alpine‑based)
CI	GitHub Actions (test, lint, build, deploy)
Документація API	Swagger UI (/docs) + ReDoc (/redoc)
Тестування	pytest (unit + integration)
Лінтинг	ruff + mypy
🚀 Як розгорнути локально
1️⃣ Клонувати репозиторій
git clone https://github.com/<your‑username>/ios-purchased-catalog-hub.git
cd ios-purchased-catalog-hub
2️⃣ (Опціонально) Підготувати віртуальне середовище
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Запустити скрипт‑колектор (один раз, щоб створити базу)
python -m collector.run   # створює/оновлює catalog.db
За замовчуванням колектор збирає усі платні товари (max 200 записів за запит, перебираючи алфавіт). На швидкості з’єднання процес займає ~5‑10 хв.

4️⃣ Запустити API‑сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Тепер відкрийте у браузері: http://localhost:8000/docs – інтерфейс Swagger.

5️⃣ (Альтернатива) Запуск через Docker
docker compose up --build -d    # запускає collector + API в одному контейнері
Контейнер відкриває порт 8000. Перевірте: http://localhost:8000/docs.

📡 Використання API
Основний endpoint
GET /catalog
Параметри (query)
Параметр	Тип	Приклад	Опис
product_type	str	software	software, movie, ebook, podcast, hardware
min_ios	str	14.0	Мінімальна iOS‑версія (включно).
price_max	float	9.99	Максимальна ціна у валюті currency.
genre	str	Games	Фільтр за жанром (можна вказати кілька, розділяючи комами).
device	str	iPhone	iPhone, iPad, AppleTV, Watch.
format	str	csv	Якщо csv – повертає файл CSV, інакше – JSON.
limit	int	100	Кількість записів у відповіді (максимум 1000).
offset	int	200	Для пост‑пагінації.
Приклад запиту
GET https://api.example.com/catalog?product_type=software&min_ios=13.0&price_max=5&genre=Games,Education&device=iPhone&format=json
Приклад відповіді (JSON)
[
  {
    "id": 284910350,
    "product_type": "software",
    "name": "Minecraft",
    "seller": "Mojang",
    "price": 6.99,
    "currency": "USD",
    "min_ios": "10.0",
    "genres": ["Games","Adventure","Sandbox"],
    "release_date": "2011-11-17T00:00:00Z"
  },
  {
    "id": 123456789,
    "product_type": "movie",
    "name": "Inception",
    "seller": "Warner Bros.",
    "price": 3.99,
    "currency": "USD",
    "min_ios": null,
    "genres": ["Science Fiction","Thriller"],
    "release_date": "2010-07-16T00:00:00Z"
  }
]
CSV‑вихід
Якщо вказати format=csv, відповідь містить заголовок і дані, які можна зберегти у файл catalog.csv.

Отримання інформації про один продукт
GET /catalog/{product_id}
Параметр: product_id – номер trackId/productId у iTunes. Повертає повний запис, включно з полем raw_json.

📚 Джерела даних
Джерело	Опис	Публічний API
iTunes Search API	Головне джерело для додатків, ігор, фільмів, книг, підкастів, апаратури. Повертає JSON‑об’єкти із minimumOsVersion, price, currency, supportedDevices тощо.	https://itunes.apple.com/search?term=&country=US&entity=software&limit=200
App Store RSS feeds	Топ‑500/Топ‑100 новинок – корисно для швидких «отримай останні» кеш‑запитів.	https://rss.applemarketingtools.com/api/v2/us/apps/top-paid/200/apps.json
Apple Books Search API	Пошук та отримання метаданих ebook‑у.	https://books.apple.com/search?term=&entity=ebook&country=US
Apple Hardware Catalog (частина iTunes API)	Інформація про Apple Pencil, Magic Keyboard, Apple Watch‑strap тощо.	entity=hardware у iTunes Search API
Усі запити виконуються без авторизації, тому їх можна робити з будь‑якого серверу або локального комп’ютера.

🛡️ Контроль якості та CI/CD
Шаг	GitHub Action	Опис
Lint	ruff + black	Перевірка стилю PEP‑8, авто‑форматування.
Типи	mypy	Перевірка типізації (Pydantic‑моделі, SQLAlchemy).
Тести	pytest	Юніт‑тести для колектора, моделей, API‑ендпоінтів (coverage > 90 %).
Build Docker	docker/build-push-action	Створює образ ghcr.io/<user>/ios-purchased-catalog-hub:latest.
Scheduled update	schedule: cron('0 3 * * *')	Щоденний запуск collector.run у dedicated‑job, оновлює базу та пушить новий Docker‑образ.
Deploy (optional)	ssh + docker compose	Автоматичне розгортання на VPS після успішного білду.
Усі workflow‑файли знаходяться у .github/workflows/.

🤝 Внесок у проєкт (Contributing)
Fork репозиторій.
Створіть branch з назвою типу feature/… або bugfix/….
Пишіть код, додавайте/оновлюйте тести.
Переконайтесь, що всі CI‑степи проходять (make lint && make test).
Створіть Pull Request з коротким описом змін.
Керівництво для нових учасників
Тема	Файл/директорія
Запуск колектора	collector/run.py
Опис API‑моделей	app/models.py
Маршрути FastAPI	app/main.py
Docker‑конфігурація	Dockerfile, docker-compose.yml
Тести	tests/
CI‑скрипти	.github/workflows/
📄 Ліцензія
Цей проєкт випущений під MIT License – ви можете вільно копіювати, змінювати та розповсюджувати код, навіть у комерційних цілях, за умови збереження копії ліцензії у вашій копії.

MIT License

Copyright (c) 2024 <your‑name>

Permission is hereby granted, free of charge, to any person obtaining a copy...
Повний текст ліцензії — у файлі LICENSE.

🎉 Підтримка проекту
Star репозиторій, якщо проєкт корисний.
Якщо у вас є питання, відкривайте Issue — ми швидко відповімо.
Для великих змін або фінансової підтримки — напишіть в README або у CONTRIBUTING.md.
