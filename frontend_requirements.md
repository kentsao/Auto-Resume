# Frontend Requirements & Architecture

## Overview
The frontend for Auto-Resume will be a Single Page Application (SPA) that allows users to connect their GitHub account, preview their generated resume, and download it in various formats.

## Tech Stack
- **Framework**: React (Create React App or Vite)
- **Styling**: Tailwind CSS
- **State Management**: React Context or Redux Toolkit (if needed)
- **Routing**: React Router
- **HTTP Client**: Axios

## Authentication Flow
1. **Login**: User clicks "Login with GitHub".
2. **Redirect**: App redirects to `http://localhost:8000/auth/github/login`.
3. **Callback**: GitHub redirects back to backend callback URL.
4. **Token Exchange**: Backend processes code, creates user, and returns JWT.
5. **Frontend Session**: Frontend receives JWT (via URL param or cookie) and stores it (localStorage/cookie).
6. **Authenticated Requests**: Frontend attaches `Authorization: Bearer <token>` to subsequent API calls.

## Core Features
1. **Landing Page**: Introduction and "Connect GitHub" button.
2. **Dashboard/Preview**:
   - Real-time preview of the resume (HTML/UI mode).
   - Toggle between "Formal" and "Creative" templates.
   - "Summarize with AI" button.
3. **Export**:
   - Download as PDF.
   - Download as HTML.

## UI Components
- `Layout`: Main wrapper with Navigation bar.
- `GitHubConnect`: Button component to initiate OAuth flow.
- `ResumePreview`: Iframe or HTML renderer for the resume content.
- `Controls`: Toolbar for actions (Summarize, Change Template, Download).
- `LoadingSpinner`: Visual feedback during API calls.

## API Integration Points

### Authentication
- `GET /auth/github/login`: Initiates login.
- `GET /auth/github/callback`: Handles callback (Backend handles this, frontend might need to handle the final redirect with token).

### Resume Generation
- `GET /generate/{username}/ui`: Fetches HTML for UI preview.
- `GET /generate/{username}/formal`: Fetches HTML for formal template.
- `GET /generate/{username}/pdf`: Triggers PDF download.
- `GET /generate/{username}/summarized`: Fetches AI-summarized resume HTML.

## Data Flow
1. User logs in -> Token stored.
2. User navigates to Dashboard -> Fetch Resume Data (or HTML).
3. User clicks "Summarize" -> Call `/summarized` endpoint -> Update Preview.
4. User clicks "Download PDF" -> Call `/pdf` endpoint -> Trigger file download.
