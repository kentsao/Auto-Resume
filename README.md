# GitHub Resume Generator

🚀 A system that connects to your GitHub profile, extracts key information, and automatically generates a professional resume in **HTML** and **PDF** formats. It also integrates with **LLM APIs** to summarize projects and bio.

---

## Features
- ✅ **GitHub Integration** – Connect via REST API to fetch repos, contributions, and user profiles
- ✅ **OAuth Authentication** – Secure GitHub OAuth2 flow for accessing private repositories
- ✅ **Multiple Output Formats**:
  - 📱 Interactive UI (real-time preview)
  - � Formal HTML (professional layout)
  - 📋 PDF export (download-ready)
- ✅ **LLM Summarization** – Optional AI-powered project and bio summarization using Google Gemini
- ✅ **Data Normalization** – Maps GitHub data to structured resume JSON schema
- ✅ **Comprehensive Testing** – 41+ unit tests with full async support
- ✅ **JWT Authentication** – Secure session management with JWT tokens
- 🚧 **Coming Soon**:
  - Cloud deployment (K8s/Terraform)
  - GraphQL support

---

## Architecture Diagram
```mermaid
flowchart TD
    A[GitHub API] --> B[Backend Service]
    B --> C[Resume JSON Schema]
    C --> D[HTML Renderer]
    C --> F[LLM Summarizer]
    D --> E[PDF Exporter]
    E --> G[User]
    F --> D
    F --> E
````

---

## 🚀 Project Roadmap & Timeline

Here’s the planned set of tasks and estimated days to finish each milestone for the GitHub Resume Generator project:

| #  | Task                      | Description                                                                               | Estimated Days |
| -- | ------------------------- | ----------------------------------------------------------------------------------------- | -------------- |
| 1  | Project Setup & Repo      | Create GitHub repo, directory skeleton, `README.md`, and initial Mermaid diagram          | 1 day          |
| 2  | Define Resume JSON Schema | Finalize hybrid resume schema (`basics`, `skills`, `projects`, `experience`, `education`) | 1 day          |
| 3  | GitHub Client (REST)      | Implement REST API client: fetch user profile, repos, languages; mock unit tests          | 2 days         |
| 4  | Data Normalization        | Map GitHub JSON → resume schema; implement `DataNormalizer`; unit tests                   | 2 days         |
| 5  | LLM Integration           | Integrate LLM API for summarizing projects and bio (mock first, later real API)           | 2 days         |
| 6  | HTML Renderer             | Design HTML template; generate resume from JSON; basic browser UI                         | 2 days         |
| 7  | PDF Export                | Implement PDF export from HTML (headless browser or WeasyPrint)                           | 2 days         |
| 8  | OAuth & Auth              | GitHub OAuth for private repos; token management & security                               | 2 days         |
| 9  | Cloud Deployment          | Deploy backend + renderer to Cloud Run / server; static hosting for HTML                  | 2 days         |
| 10 | Testing & CI/CD           | TDD for backend + normalization + renderer; schema validation; CI/CD setup                | 2 days         |
| 11 | Polish & UX               | Frontend tweaks, responsive design, final PDF styling, minor bug fixes                    | 2 days         |
| 12 | Documentation & Release   | Prepare demo, screenshots, and release version                                            | 1 day          |

**Total Estimated Time:** ~21 days (~3 weeks)

> Each completed milestone helps track progress and ensures modular, testable development.

---

## Tech Stack

* **Backend**: FastAPI + Python (async/await)
* **Authentication**: GitHub OAuth2 + JWT
* **Frontend**: React + Vite + Tailwind CSS
* **PDF Export**: WeasyPrint
* **LLM API**: Google Generativeai (Gemini)
* **Testing**: pytest + pytest-asyncio
* **Infrastructure**: Terraform + Kubernetes (planned)

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- GitHub account
- Google Gemini API key (optional, for LLM summarization)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/kentsao/Auto-Resume.git
cd Auto-Resume
```

2. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials:
# GITHUB_CLIENT_ID=...
# GITHUB_CLIENT_SECRET=...
# GEMINI_API_KEY=...
# SECRET_KEY=...
```

4. **Run the backend server**
```bash
uvicorn backend.app.main:app --reload
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

4. **Access the application**
- Open http://localhost:5173 in your browser.

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /auth/github/login` | Initiate GitHub OAuth flow |
| `GET /auth/github/callback` | OAuth callback handler |
| `GET /generate/{username}/ui` | Generate interactive UI resume |
| `GET /generate/{username}/formal` | Generate formal HTML resume |
| `GET /generate/{username}/pdf` | Generate PDF resume |
| `GET /generate/{username}/summarized` | Generate resume with LLM summarization |
| `GET /test/ui` | Test with sample data |

### Running Tests

```bash
# Run all tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_github_oauth.py

# Run with coverage
pytest --cov=backend backend/tests/
```

---

## Development Progress

| Task | Status |
|------|--------|
| GitHub REST API Client | ✅ Complete |
| Data Normalization | ✅ Complete |
| HTML/PDF Rendering | ✅ Complete |
| LLM Integration (Gemini) | ✅ Complete |
| GitHub OAuth2 | ✅ Complete |
| Unit Tests (41 tests) | ✅ Complete |
| JWT Session Management | ✅ Complete |
| Frontend (React + Vite) | ✅ Complete |
| Cloud Deployment | 🚧 Planned |

---

## Project Structure

```
Auto-Resume/
├── backend/
│   ├── app/
│   │   ├── auth/           # GitHub OAuth
│   │   ├── db/             # Database models (future)
│   │   ├── github_client/  # GitHub API client
│   │   ├── llm/            # LLM summarizer
│   │   ├── models/         # Resume schema
│   │   ├── normalizer/     # Data normalization
│   │   ├── render/         # HTML/PDF renderer
│   │   └── main.py         # FastAPI app
│   └── tests/              # Unit tests
├── requirements.txt
├── .env.example
└── README.md
```
