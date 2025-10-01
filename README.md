# GitHub Resume Generator

🚀 A system that connects to your GitHub profile, extracts key information, and automatically generates a professional resume in **HTML** and **PDF** formats. It also integrates with **LLM APIs** to summarize projects and bio.

---

## Features (Planned)
- 🔗 Connect to GitHub (REST + GraphQL support in future)
- 📊 Extract repositories, contributions, and activities
- 📝 Store resume data in JSON schema
- 🌐 Generate **HTML resume** for browser display
- 📄 Export **PDF resume** for sharing
- 🤖 Summarize projects & bio with **LLM API**
- ☁️ Deployment to cloud platforms

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

* **Backend**: FastAPI + Python
* **Database**: SQLite (for prototyping)
* **Frontend/Render**: Jinja2 / HTML templates
* **PDF Export**: WeasyPrint / ReportLab
* **LLM API**: OpenAI / Anthropic / others
