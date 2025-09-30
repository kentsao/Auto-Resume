# Auto Resume Generator

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
    A[GitHub API] -->|fetch repos| B[Backend Service]
    B --> C[Resume JSON Schema]
    C --> D[HTML Renderer]
    D --> E[PDF Exporter]
    C --> F[LLM Summarizer]
    E --> G[User]
    F --> D
    F --> E
