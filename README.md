# URL Shortener API 🚀

A simple and efficient URL Shortener service built with **FastAPI** and backed by **PostgreSQL**. This service allows users to shorten long URLs, manage them, and redirect to the original URLs using short codes.

---

## 🛠 Features

- 🔗 Generate short URLs from long ones
- 📥 Redirect short URLs to original long URLs
- 📊 Track URL metadata (optional)
- 🧪 Fully testable with `pytest`
- 🐳 Containerized using Docker
- 📦 PostgreSQL integration for persistent storage

---

## 📁 Project Structure

url_shortener_api/
├── app/
│ ├── main.py # FastAPI entry point
│ ├── models.py # Pydantic and DB models
│ ├── database.py # PostgreSQL DB connection
│ ├── crud.py # Business logic functions
│ ├── routes.py # API route handlers
│ └── utils.py # Helper utilities
├── tests/
│ ├── unit/ # Unit tests with pytest
│ └── ...
├── Dockerfile
├── requirements.txt
├── .env
└── README.md


---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/url-shortener-api.git
cd url-shortener-api

2. Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set up your .env file
DATABASE_URL=postgresql://user:password@localhost:5432/url_shortener

5. Run the app
uvicorn app.main:app --reload

🐳 Docker Setup
Build and run with Docker:
docker build -t url-shortener .
docker run -d -p 8000:8000 --env-file .env url-shortener

🧪 Running Tests
pytest --cov=app tests/

| Method | Endpoint        | Description              |
| ------ | --------------- | ------------------------ |
| POST   | `/shorten`      | Create a short URL       |
| GET    | `/{short_code}` | Redirect to original URL |




