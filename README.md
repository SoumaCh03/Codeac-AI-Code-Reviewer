# Codeac AI Code Reviewer 🤖

![Codeac Dashboard](https://img.shields.io/badge/Codeac-Autonomous%20Review-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue?logo=docker)

Codeac is an autonomous AI-powered code review system designed to seamlessly integrate with GitHub. It automatically reviews pull requests for security vulnerabilities, performance bottlenecks, and code quality issues, using a combination of static analysis (Semgrep) and state-of-the-art LLMs.

## ✨ Features

- **Automated PR Reviews**: Instantly analyzes code changes as soon as a Pull Request is opened.
- **AI-Powered Insights**: Uses advanced LLMs (OpenAI, Anthropic, Gemini) via LangChain to provide deep architectural and logic reviews.
- **Static Analysis Integration**: Integrates directly with `semgrep` to catch known vulnerabilities (SQL Injection, XSS, Hardcoded Secrets) with zero false positives.
- **Beautiful Dashboard**: A Next.js frontend to monitor your organization's security posture and view recent PR findings.
- **Asynchronous Processing**: Uses Celery and Redis to handle heavy AI workloads in the background without slowing down the main API.

## 🏗️ Architecture

Codeac uses a decoupled microservices architecture:

- **Frontend**: Next.js (React 19, Tailwind CSS)
- **Backend API**: FastAPI (Python 3.12, SQLAlchemy, Pydantic)
- **Worker**: Celery (handles the actual AI processing)
- **Cache & Broker**: Redis
- **Database**: PostgreSQL
- **Infrastructure**: Docker & Docker Compose

## 🚀 Getting Started Locally

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- A GitHub App configured for Webhooks

### 1. Clone the repository

```bash
git clone https://github.com/SoumaCh03/Codeac-AI-Code-Reviewer.git
cd Codeac-AI-Code-Reviewer
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory and configure your GitHub App and AI provider keys:

```env
GITHUB_APP_ID=your_app_id
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n..."
OPENAI_API_KEY=sk-yourkey
ANTHROPIC_API_KEY=sk-ant-yourkey
```

### 3. Run with Docker Compose

Start the entire stack (Database, Redis, API, Worker, and Frontend) with a single command:

```bash
docker-compose up --build -d
```

### 4. Access the App

- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API Docs (Swagger)**: `http://localhost:8000/docs`

## 🛠️ Development

- The backend uses **Poetry** for dependency management.
- Database migrations are handled via **Alembic**. Run migrations using:
  ```bash
  docker exec codeac_backend alembic upgrade head
  ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to submit pull requests, report issues, and request features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
