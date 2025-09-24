## 🚀 DRF Starter Project

A production-ready Django REST Framework (DRF) starter project that includes user registration, authentication (JWT), password reset flow, profile management, Docker support, and 12-factor best practices.

## ✅ Features
- [] 🔐 User Registration & JWT Authentication (via djangorestframework-simplejwt)
- [] 👤 Profile Management with extendable user model
- [] 🔁 Password Reset Flow (Email-based reset)
- [] ⚙️ 12-Factor Configuration using django-environ
- [] 📦 Containerized Setup with Docker & Docker Compose
- [] 🌐 CORS Support via django-cors-headers
- [] 🧾 API Documentation using drf-spectacular
- [] ☁️ Storage Ready using django-storages for S3 and others
- [] 🧪 Ready for unit testing & CI/CD integration

## 🛠️ Tech Stack
- [] Django

- [] Django REST Framework
- [] Simple JWT
- [] drf-spectacular
- [] django-environ
- [] django-cors-headers
- [] django-storages
- [] Docker & Docker Compose

## 🐳 Quickstart (Dockerized)

```bash
# Clone the repo
git clone https://github.com/your-username/drf-startproject.git
cd drf-startproject

# Copy and configure environment variables
cp .env.example .env

# Build and run containers
docker-compose up --build

```