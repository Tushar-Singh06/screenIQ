# ScreenIQ — AI-Powered Candidate Screener

AI-powered recruitment intelligence platform built as a full-stack application using Django REST Framework, PostgreSQL, Next.js, TypeScript, and Groq LLM integration.

This project was developed for the ScreenIQ Full-Stack Developer Take-Home Assignment and focuses on scalable architecture, AI integration, security, performance, and premium SaaS-grade UI/UX.

---

# Overview

ScreenIQ is a lightweight internal HR tool that allows recruiters to:

- Paste a job description
- Upload or paste a candidate resume
- Receive an AI-generated screening score
- View concise AI reasoning
- Track and manage previous screenings

The application includes:

- Django REST API backend
- JWT authentication
- PostgreSQL database
- AI-powered candidate screening
- Premium AI SaaS frontend
- Enterprise-style analytics dashboard

---

# Tech Stack

## Backend

- Python
- Django 6
- Django REST Framework
- PostgreSQL
- JWT Authentication (`djangorestframework-simplejwt`)
- Groq API (Llama 3.3 70B)
- Python Dotenv

## Frontend

- Next.js App Router
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui
- Framer Motion
- Axios
- Zod
- React Hook Form
- Sonner Toasts
- pdfjs-dist

---

# Features

## Authentication

- JWT-based authentication
- Login-protected routes
- Persistent sessions
- Logout functionality
- Axios auth interceptor

## AI Screening

- Candidate screening form
- Job description input
- Resume input
- AI-powered candidate evaluation
- AI score generation
- AI reasoning generation
- Structured AI JSON parsing
- Score normalization handling

## PDF Upload Support

- Client-side PDF parsing
- Automatic text extraction
- Resume auto-fill
- Editable extracted content

## Dashboard Analytics

- Paginated applications dashboard
- Dynamic analytics cards
- AI score color coding
- Recent screenings table
- Detailed application view
- Responsive enterprise table

## Premium SaaS UI

- Dark AI SaaS theme
- Glassmorphism
- Background gradients
- Animated transitions
- Skeleton loaders
- Toast notifications
- Bento layouts
- Smooth Framer Motion interactions

---

# Project Architecture

## Backend Architecture

The backend follows a layered architecture:

```txt
screening/
├── models.py
├── serializers.py
├── views.py
├── services.py
├── prompts.py
├── utils.py
├── pagination.py
├── tests.py
└── urls.py
```

### Key Design Decisions

- `services.py`
  - Separates AI business logic from API views
  - Improves maintainability

- `prompts.py`
  - Centralized AI prompt management

- `utils.py`
  - Handles AI score normalization

- `serializers.py`
  - Input validation layer

- `pagination.py`
  - Reusable pagination abstraction

---

## Frontend Architecture

```txt
src/
├── app/
│   ├── dashboard/
│   ├── login/
│   ├── screen/
│   └── layout.tsx
│
├── components/
│   ├── ui/
│   ├── app-shell.tsx
│   ├── sidebar.tsx
│   ├── navbar.tsx
│   ├── screening-form.tsx
│   ├── ai-score-card.tsx
│   ├── dashboard-cards.tsx
│   ├── dashboard-table.tsx
│   ├── protected-route.tsx
│   └── loader.tsx
│
├── services/
│   ├── auth.service.ts
│   └── screening.service.ts
│
├── hooks/
├── utils/
├── lib/
├── styles/
└── types/
```

---

# Setup Instructions

# 1. Clone Repository

```bash
git clone https://github.com/Tushar-Singh06/screenIQ.git
cd screeniq
```

---

# 2. Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE screeniq;
```

---

## Configure Environment Variables

Create `.env`:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=screeniq
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

GROQ_API_KEY=your_groq_api_key
```

---

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Start Backend Server

```bash
python manage.py runserver
```

Backend runs at:

```txt
http://localhost:8000
```

---

# 3. Frontend Setup

```bash
cd frontend
```

---

## Install Dependencies

```bash
npm install
```

---

## Configure Environment Variables

Create `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Start Frontend

```bash
npm run dev
```

Frontend runs at:

```txt
http://localhost:3000
```

---

# API Endpoints

## Authentication

### Login

```http
POST /api/token/
```

---

## AI Screening

### Screen Candidate

```http
POST /api/screen/
```

---

## Applications

### Get Applications

```http
GET /api/applications/
```

### Get Single Application

```http
GET /api/applications/<id>/
```

---

# Bugs Fixed (Task A-1)

The provided starter code contained several architectural and security issues.

## 1. Missing Authentication Protection

### Problem

The starter API allowed unauthenticated access.

### Fix

Added:

```python
permission_classes = [IsAuthenticated]
```

### Why

Prevents unauthorized users from accessing protected endpoints.

---

## 2. Unsafe Request Data Access

### Problem

Used direct dictionary access:

```python
request.data['resume']
```

This can raise `KeyError`.

### Fix

Added serializer validation layer.

### Why

Improves validation, maintainability, and error handling.

---

## 3. No Input Validation

### Problem

Job descriptions and resumes could be empty or invalid.

### Fix

Added serializer validation methods.

### Why

Ensures valid AI input and prevents malformed requests.

---

## 4. AI Logic Inside View

### Problem

Business logic tightly coupled to API view.

### Fix

Moved AI logic into `services.py`.

### Why

Improves separation of concerns and scalability.

---

## 5. Insecure OpenAI Integration

### Problem

API configuration was hardcoded and outdated.

### Fix

Integrated Groq client using environment variables.

### Why

Improves security and maintainability.

---

## 6. Missing Error Handling

### Problem

AI failures could crash the API.

### Fix

Added try/catch exception handling.

### Why

Prevents server crashes and returns proper API responses.

---

## 7. No Pagination

### Problem

Returning all applications would not scale.

### Fix

Implemented reusable pagination.

### Why

Supports large datasets efficiently.

---

# Security Vulnerability Fix (Task A-3)

## Original Vulnerability

The original implementation exposed all applications:

```python
Application.objects.all()
```

This created an authorization vulnerability where any authenticated user could access every candidate record.

---

## Fix

Applications are now filtered by the authenticated user:

```python
Application.objects.filter(created_by=request.user)
```

---

## Why This Matters

This ensures:

- User-level data isolation
- Proper authorization
- Candidate privacy protection
- Multi-user safety

This was the primary security vulnerability identified in the assignment.

---

# AI Prompt Design (Task A-2)

The original prompt was too simplistic and unreliable.

I redesigned the prompt to:

- Use both the job description and resume
- Generate a score between 1–10
- Return concise reasoning
- Produce structured JSON output
- Reduce hallucinations

---

## Prompt Design Goals

- Consistent structured responses
- Easier backend parsing
- Better recruiter usefulness
- Reduced ambiguity
- Improved scoring reliability

---

## Example AI Output

```json
{
  "score": 8.5,
  "reasons": [
    "Strong backend experience",
    "Good PostgreSQL knowledge",
    "Relevant full-stack project work"
  ]
}
```

---

# AI Score Normalization (Task B-3)

The assignment specified inconsistent AI outputs such as:

- `"7.3"`
- `"Seven"`
- `"Eight out of ten"`

Normalization is handled in the backend.

---

## Why Backend Normalization?

- Consistent API contract
- Centralized validation
- Cleaner frontend rendering
- Easier multi-client support

The frontend always receives numeric scores.

---

# State Management Decision

The frontend uses local React state and hooks instead of Redux or Zustand.

## Why?

The application scope is relatively contained and state is mostly page-local.

This approach:

- Reduces unnecessary complexity
- Improves maintainability
- Speeds up development
- Keeps architecture lightweight

Global state management would be more appropriate for:

- Real-time collaboration
- Shared caching
- Complex module synchronization

---

# Dashboard Performance Strategy (Task B-2)

The dashboard uses server-side pagination.

## Why Server-Side Pagination?

Advantages:

- Better scalability
- Lower frontend memory usage
- Faster rendering
- Efficient handling of 500+ rows

Tradeoff:

- Additional API requests

This is the preferred enterprise approach for analytics dashboards.

---

# PDF Upload Architecture

The frontend supports PDF uploads using `pdfjs-dist`.

## Workflow

```txt
PDF Upload
    ↓
Client-side text extraction
    ↓
Auto-fill textareas
    ↓
Editable by user
    ↓
Sent to AI backend
```

## Why Client-Side Extraction?

Advantages:

- Lower backend CPU usage
- Faster UX
- No file storage layer required
- Lightweight architecture

Tradeoffs:

- OCR unsupported
- Scanned PDFs may fail
- Formatting loss possible

---

# UI/UX Design Decisions

The frontend was intentionally designed as a premium AI SaaS product rather than a simple CRUD dashboard.

## Design Inspirations

- Linear
- Vercel
- Notion AI
- Perplexity

## Key Design Elements

- Dark modern AI theme
- Soft gradients
- Glassmorphism
- Smooth animations
- AI-inspired interactions
- Enterprise dashboard aesthetics

---

# Framer Motion Usage

Animations include:

- Page transitions
- Fade-in sections
- Hover effects
- Animated score cards
- Smooth modal transitions
- Skeleton loading states

Purpose:

- Improve perceived performance
- Increase UI polish
- Create premium SaaS feel

---

# Accessibility

Implemented:

- Semantic HTML
- Keyboard accessibility
- Responsive layouts
- Accessible forms
- Proper contrast ratios

---

# Tests

The project includes critical backend tests.

## Tests Implemented

### 1. Unauthorized Access Protection

Ensures protected routes reject unauthenticated users.

### 2. User Data Isolation

Ensures users can only access their own applications.

### 3. AI Score Normalization

Ensures inconsistent AI outputs normalize correctly.

---

# Bias & Fairness (Task C-2)

AI hiring systems may unintentionally introduce bias based on names, universities, gender indicators, or geographic locations rather than actual qualifications.

To detect bias, I would create controlled evaluation datasets where resumes remain identical while demographic indicators are changed. By comparing AI scores across these variations, statistical inconsistencies could reveal bias patterns. Metrics such as score deviation, false rejection rates, and demographic parity could help quantify fairness issues.

To reduce bias, I would:

- Remove personally identifiable information before scoring
- Focus prompts strictly on skills and experience
- Add prompt constraints discouraging demographic reasoning
- Introduce human review checkpoints
- Continuously audit AI outputs over time

Bias mitigation should be treated as an ongoing monitoring process rather than a one-time fix.

---

# Challenges Faced

## 1. pdfjs-dist Worker Issues

### Issue

Next.js SSR conflicts with browser-only PDF APIs.

### Fix

Used dynamic imports and browser-only execution.

---

## 2. Tailwind CSS v4 Migration

### Issue

Some utility classes behaved differently in Tailwind v4.

### Fix

Updated utility usage and global styles structure.

---

## 3. Dynamic Dashboard Analytics

### Issue

Analytics were initially static.

### Fix

Computed analytics dynamically from API responses.

---

# Future Improvements

- Real-time AI streaming
- WebSocket support
- OCR support
- Resume preview modal
- AI confidence visualization
- Candidate filtering
- Export reports
- Role-based access control
- Secure cookie authentication
- Monitoring and logging
- Dark/light mode toggle

---

# Environment Variables

## Backend

```env
SECRET_KEY=
DEBUG=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

GROQ_API_KEY=
```

## Frontend

```env
NEXT_PUBLIC_API_URL=
```

---

# Production Considerations

For production deployment:

- Use HTTPS
- Configure strict CORS
- Store secrets securely
- Add rate limiting
- Enable monitoring/logging
- Use secure cookies
- Add CI/CD pipelines

---

# Final Notes

This project was intentionally designed as a modern AI SaaS platform rather than a minimal assignment submission.

Primary focus areas included:

- Scalable architecture
- Security
- Clean code organization
- AI integration reliability
- Premium UI/UX
- Maintainability
- Real-world engineering practices

The goal was to build a product experience that feels production-oriented while satisfying all assignment requirements.
