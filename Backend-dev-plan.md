
# Backend Development Plan — FinSense AI

---

## 1️⃣ Executive Summary

**What Will Be Built:**  
A FastAPI backend for FinSense AI — an AI-powered financial management platform for small businesses. The backend will support user authentication, transaction management with AI categorization, financial analytics, and an AI assistant chatbot.

**Key Constraints:**
- **Backend:** FastAPI (Python 3.13, async)
- **Database:** MongoDB Atlas using Motor (async) and Pydantic v2 models
- **No Docker** — local development only
- **Manual testing** required after every task via frontend UI
- **Git workflow:** single branch `main` only
- **API base path:** `/api/v1/*`
- **Background tasks:** synchronous by default; use `BackgroundTasks` only if strictly necessary

**Sprint Structure:**  
Dynamic sprints (S0 → Sn) covering all frontend-visible features. Each sprint includes task-level manual testing before pushing to `main`.

---

## 2️⃣ In-Scope & Success Criteria

**In-Scope Features:**
- User authentication (signup, login, logout, profile management)
- Transaction CRUD operations with AI categorization
- Transaction review workflow (approve, change category)
- Financial dashboard data (revenue, expenses, profit, cash balance)
- Transaction filtering and search
- Category management
- AI assistant chat interface
- User profile and business information management
- Account connection simulation (Square, Stripe, Bank)
- Trial subscription management

**Success Criteria:**
- All frontend features functional end-to-end
- All task-level tests pass via UI
- Each sprint's code pushed to `main` after verification
- AI categorization returns confidence scores and explanations
- Dashboard displays accurate financial metrics
- Transaction review workflow allows category changes

---

## 3️⃣ API Design

**Base Path:** `/api/v1`

**Error Envelope:** `{ "error": "message" }`

### Authentication Endpoints

**POST /api/v1/auth/signup**
- **Purpose:** Register new user account
- **Request:** `{ "email": "string", "password": "string", "firstName": "string", "lastName": "string", "businessName": "string" }`
- **Response:** `{ "user": { "id": "string", "email": "string", "firstName": "string", "lastName": "string", "businessName": "string" }, "token": "string" }`
- **Validation:** Email format, password min 6 chars, all fields required

**POST /api/v1/auth/login**
- **Purpose:** Authenticate existing user
- **Request:** `{ "email": "string", "password": "string" }`
- **Response:** `{ "user": { "id": "string", "email": "string", "firstName": "string", "lastName": "string", "businessName": "string" }, "token": "string" }`
- **Validation:** Email format, password required

**POST /api/v1/auth/logout**
- **Purpose:** Invalidate user session
- **Request:** None (uses Authorization header)
- **Response:** `{ "message": "Logged out successfully" }`
- **Validation:** Valid JWT required

**GET /api/v1/auth/me**
- **Purpose:** Get current user profile
- **Request:** None (uses Authorization header)
- **Response:** `{ "id": "string", "email": "string", "firstName": "string", "lastName": "string", "businessName": "string", "phone": "string", "industry": "string", "employees": "number", "monthlyRevenue": "number" }`
- **Validation:** Valid JWT required

**PUT /api/v1/auth/profile**
- **Purpose:** Update user profile
- **Request:** `{ "firstName": "string", "lastName": "string", "businessName": "string", "phone": "string", "industry": "string", "employees": "number", "monthlyRevenue": "number" }`
- **Response:** `{ "user": { ... } }`
- **Validation:** Valid JWT required

**DELETE /api/v1/auth/account**
- **Purpose:** Delete user account
- **Request:** None (uses Authorization header)
- **Response:** `{ "message": "Account deleted successfully" }`
- **Validation:** Valid JWT required

### Transaction Endpoints

**GET /api/v1/transactions**
- **Purpose:** List all user transactions with optional filters
- **Query Params:** `status` (all|auto-approved|needs-review|manual), `search` (vendor or category)
- **Response:** `{ "transactions": [ { "id": "string", "date": "string", "vendor": "string", "amount": "number", "category": "string", "confidence": "number", "status": "string", "explanation": "string", "paymentMethod": "string" } ] }`
- **Validation:** Valid JWT required

**GET /api/v1/transactions/:id**
- **Purpose:** Get single transaction details
- **Response:** `{ "id": "string", "date": "string", "vendor": "string", "amount": "number", "category": "string", "confidence": "number", "status": "string", "explanation": "string", "paymentMethod": "string" }`
- **Validation:** Valid JWT required, transaction belongs to user

**PUT /api/v1/transactions/:id**
- **Purpose:** Update transaction (change category or status)
- **Request:** `{ "category": "string", "status": "string" }`
- **Response:** `{ "transaction": { ... } }`
- **Validation:** Valid JWT required, transaction belongs to user

**POST /api/v1/transactions/sync**
- **Purpose:** Simulate syncing transactions from connected account
- **Request:** `{ "source": "square|stripe|bank" }`
- **Response:** `{ "message": "Sync completed", "count": "number" }`
- **Validation:** Valid JWT required

### Dashboard Endpoints

**GET /api/v1/dashboard/stats**
- **Purpose:** Get financial overview statistics
- **Response:** `{ "monthlyRevenue": "number", "netProfit": "number", "totalExpenses": "number", "cashBalance": "number", "revenueChange": "number", "profitChange": "number", "expensesChange": "number", "cashChange": "number" }`
- **Validation:** Valid JWT required

**GET /api/v1/dashboard/revenue-trend**
- **Purpose:** Get revenue vs expenses trend (last 7 days)
- **Response:** `{ "data": [ { "date": "string", "revenue": "number", "expenses": "number" } ] }`
- **Validation:** Valid JWT required

**GET /api/v1/dashboard/expense-breakdown**
- **Purpose:** Get expense breakdown by category
- **Response:** `{ "data": [ { "category": "string", "amount": "number", "percentage": "number", "color": "string" } ] }`
- **Validation:** Valid JWT required

**GET /api/v1/dashboard/recent-transactions**
- **Purpose:** Get 5 most recent transactions
- **Response:** `{ "transactions": [ { ... } ] }`
- **Validation:** Valid JWT required

**GET /api/v1/dashboard/alerts**
- **Purpose:** Get financial alerts and notifications
- **Response:** `{ "alerts": [ { "id": "string", "type": "warning|info|success", "title": "string", "message": "string", "date": "string", "actionable": "boolean" } ] }`
- **Validation:** Valid JWT required

### Category Endpoints

**GET /api/v1/categories**
- **Purpose:** List all available transaction categories
- **Response:** `{ "categories": [ { "id": "string", "name": "string", "type": "expense|revenue|cogs", "color": "string" } ] }`
- **Validation:** Valid JWT required

### FinSense AI Endpoints

**POST /api/v1/ai/chat**
- **Purpose:** Send message to AI assistant
- **Request:** `{ "message": "string", "conversationId": "string" }`
- **Response:** `{ "response": "string", "conversationId": "string" }`
- **Validation:** Valid JWT required

### Subscription Endpoints

**GET /api/v1/subscription/status**
- **Purpose:** Get user subscription status
- **Response:** `{ "hasAccess": "boolean", "isTrialActive": "boolean", "trialEndsAt": "string", "plan": "string" }`
- **Validation:** Valid JWT required

**POST /api/v1/subscription/start-trial**
- **Purpose:** Start 14-day free trial
- **Request:** None
- **Response:** `{ "message": "Trial started", "trialEndsAt": "string" }`
- **Validation:** Valid JWT required

### Account Connection Endpoints

**GET /api/v1/accounts/connected**
- **Purpose:** List connected accounts
- **Response:** `{ "accounts": [ { "id": "string", "source": "square|stripe|bank", "name": "string", "connectedAt": "string" } ] }`
- **Validation:** Valid JWT required

**POST /api/v1/accounts/connect**
- **Purpose:** Simulate connecting an account
- **Request:** `{ "source": "square|stripe|bank", "name": "string" }`
- **Response:** `{ "account": { "id": "string", "source": "string", "name": "string", "connectedAt": "string" } }`
- **Validation:** Valid JWT required

**DELETE /api/v1/accounts/:id**
- **Purpose:** Disconnect an account
- **Request:** None
- **Response:** `{ "message": "Account disconnected" }`
- **Validation:** Valid JWT required

### Health Check

**GET /healthz**
- **Purpose:** Health check with DB connection status
- **Response:** `{ "status": "healthy", "database": "connected", "timestamp": "string" }`
- **Validation:** None

---

## 4️⃣ Data Model (MongoDB Atlas)

### users Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `email`: string (required, unique, indexed)
- `password_hash`: string (required, Argon2 hashed)
- `first_name`: string (required)
- `last_name`: string (required)
- `business_name`: string (required)
- `phone`: string (optional, default: null)
- `industry`: string (optional, default: null)
- `employees`: int (optional, default: null)
- `monthly_revenue`: float (optional, default: null)
- `created_at`: datetime (required, default: now)
- `updated_at`: datetime (required, default: now)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "maria@example.com",
  "password_hash": "$argon2id$v=19$m=65536...",
  "first_name": "Maria",
  "last_name": "Rodriguez",
  "business_name": "Maria's Coffee Shop",
  "phone": "+1 (555) 123-4567",
  "industry": "Restaurant - Coffee Shop",
  "employees": 5,
  "monthly_revenue": 35000.0,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### transactions Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `user_id`: ObjectId (required, references users)
- `date`: datetime (required)
- `vendor`: string (required)
- `amount`: float (required, negative for revenue)
- `category`: string (required)
- `confidence`: float (required, 0.0-1.0)
- `status`: string (required, enum: auto-approved|needs-review|manual)
- `explanation`: string (required, AI reasoning)
- `payment_method`: string (required)
- `original_description`: string (optional)
- `created_at`: datetime (required, default: now)
- `updated_at`: datetime (required, default: now)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "date": "2025-01-15T00:00:00Z",
  "vendor": "Sysco Boston",
  "amount": 342.50,
  "category": "Inventory - Food & Supplies",
  "confidence": 0.95,
  "status": "auto-approved",
  "explanation": "Categorized as Inventory because Sysco is your regular food distributor, and the $342 amount matches your typical Tuesday morning delivery.",
  "payment_method": "Business Debit",
  "original_description": "SYSCO BOSTON MA",
  "created_at": "2025-01-15T08:30:00Z",
  "updated_at": "2025-01-15T08:30:00Z"
}
```

### categories Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `name`: string (required, unique)
- `type`: string (required, enum: expense|revenue|cogs)
- `color`: string (required, hex color)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439013",
  "name": "Inventory - Food & Supplies",
  "type": "cogs",
  "color": "#3b82f6"
}
```

### subscriptions Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `user_id`: ObjectId (required, references users, unique)
- `is_trial_active`: boolean (required, default: false)
- `trial_started_at`: datetime (optional)
- `trial_ends_at`: datetime (optional)
- `plan`: string (optional, enum: free|premium)
- `created_at`: datetime (required, default: now)
- `updated_at`: datetime (required, default: now)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439014",
  "user_id": "507f1f77bcf86cd799439011",
  "is_trial_active": true,
  "trial_started_at": "2025-01-01T00:00:00Z",
  "trial_ends_at": "2025-01-15T00:00:00Z",
  "plan": "free",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### connected_accounts Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `user_id`: ObjectId (required, references users)
- `source`: string (required, enum: square|stripe|bank)
- `name`: string (required)
- `connected_at`: datetime (required, default: now)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439015",
  "user_id": "507f1f77bcf86cd799439011",
  "source": "square",
  "name": "Square POS",
  "connected_at": "2025-01-01T00:00:00Z"
}
```

### ai_conversations Collection

**Fields:**
- `_id`: ObjectId (auto-generated)
- `user_id`: ObjectId (required, references users)
- `conversation_id`: string (required, UUID)
- `messages`: array of objects (required)
  - `role`: string (enum: user|assistant)
  - `content`: string
  - `timestamp`: datetime
- `created_at`: datetime (required, default: now)
- `updated_at`: datetime (required, default: now)

**Example Document:**
```json
{
  "_id": "507f1f77bcf86cd799439016",
  "user_id": "507f1f77bcf86cd799439011",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "How much did I spend on supplies last month?",
      "timestamp": "2025-01-15T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "You spent $3,847 on supplies last month...",
      "timestamp": "2025-01-15T10:00:01Z"
    }
  ],
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:01Z"
}
```

---

## 5️⃣ Frontend Audit & Feature Map

### Landing Page (/)
- **Purpose:** Marketing landing page
- **Data Needed:** None
- **Backend Endpoints:** None
- **Auth Required:** No

### Sign Up (/signup)
- **Purpose:** User registration
- **Data Needed:** User input (email, password, name, business name)
- **Backend Endpoints:** `POST /api/v1/auth/signup`
- **Models:** users, subscriptions
- **Auth Required:** No

### Sign In (/signin)
- **Purpose:** User authentication
- **Data Needed:** User credentials
- **Backend Endpoints:** `POST /api/v1/auth/login`
- **Models:** users
- **Auth Required:** No

### Connect Accounts (/connect-accounts)
- **Purpose:** Connect financial data sources
- **Data Needed:** Available sources, connection status
- **Backend Endpoints:** `GET /api/v1/accounts/connected`, `POST /api/v1/accounts/connect`
- **Models:** connected_accounts
- **Auth Required:** Yes

### Sync Progress (/sync-progress)
- **Purpose:** Show transaction sync progress
- **Data Needed:** Sync status
- **Backend Endpoints:** `POST /api/v1/transactions/sync`
- **Models:** transactions
- **Auth Required:** Yes

### Transaction Review (/transaction-review)
- **Purpose:** Review and approve AI-categorized transactions
- **Data Needed:** Transactions needing review, categories
- **Backend Endpoints:** `GET /api/v1/transactions?status=needs-review`, `PUT /api/v1/transactions/:id`, `GET /api/v1/categories`
- **Models:** transactions, categories
- **Auth Required:** Yes

### Dashboard (/dashboard)
- **Purpose:** Financial overview and metrics
- **Data Needed:** Stats, charts, recent transactions, alerts
- **Backend Endpoints:** `GET /api/v1/dashboard/stats`, `GET /api/v1/dashboard/revenue-trend`, `GET /api/v1/dashboard/expense-breakdown`, `GET /api/v1/dashboard/recent-transactions`, `GET /api/v1/dashboard/alerts`
- **Models:** transactions, users
- **Auth Required:** Yes

### Transactions (/transactions)
- **Purpose:** View and manage all transactions
- **Data Needed:** All transactions with filtering
- **Backend Endpoints:** `GET /api/v1/transactions`, `PUT /api/v1/transactions/:id`, `GET /api/v1/categories`
- **Models:** transactions, categories
- **Auth Required:** Yes

### FinSense AI (/ai-assistant)
- **Purpose:** Chat with AI for financial insights
- **Data Needed:** Conversation history, user financial data
- **Backend Endpoints:** `POST /api/v1/ai/chat`
- **Models:** ai_conversations, transactions
- **Auth Required:** Yes

### Profile (/profile)
- **Purpose:** Manage user profile and business info
- **Data Needed:** User profile, subscription status
- **Backend Endpoints:** `GET /api/v1/auth/me`, `PUT /api/v1/auth/profile`, `DELETE /api/v1/auth/account`, `GET /api/v1/subscription/status`
- **Models:** users, subscriptions
- **Auth Required:** Yes

### Settings (/settings)
- **Purpose:** App settings and preferences
- **Data Needed:** User settings
- **Backend Endpoints:** `GET /api/v1/auth/me`, `PUT /api/v1/auth/profile`
- **Models:** users
- **Auth Required:** Yes

### Pricing (/pricing)
- **Purpose:** View subscription plans
- **Data Needed:** Plan details, current subscription
- **Backend Endpoints:** `GET /api/v1/subscription/status`, `POST /api/v1/subscription/start-trial`
- **Models:** subscriptions
- **Auth Required:** Optional

---

## 6️⃣ Configuration & ENV Vars

**Required Environment Variables:**

- `APP_ENV` — environment (development, production)
- `PORT` — HTTP port (default: 8000)
- `MONGODB_URI` — MongoDB Atlas connection string (required)
- `JWT_SECRET` — token signing key (required, min 32 chars)
- `JWT_EXPIRES_IN` — seconds before JWT expiry (default: 86400 = 24 hours)
- `CORS_ORIGINS` — allowed frontend URL(s) (comma-separated, default: http://localhost:5173)

**Example .env file:**
```
APP_ENV=development
PORT=8000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/finsense?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-jwt-key-min-32-characters-long
JWT_EXPIRES_IN=86400
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 7️⃣ Background Work

**Transaction Sync (if required):**
- **Trigger:** User clicks "Sync" or connects new account
- **Purpose:** Fetch transactions from external source and categorize with AI
- **Implementation:** Use FastAPI `BackgroundTasks` for async processing
- **Idempotency:** Check for duplicate transactions by vendor + amount + date
- **UI Feedback:** Frontend polls `GET /api/v1/transactions/sync-status` endpoint

**AI Categorization:**
- **Trigger:** New transaction created
- **Purpose:** Assign category with confidence score and explanation
- **Implementation:** Synchronous function using mock AI logic (pattern matching)
- **UI Feedback:** Transaction includes confidence score and explanation immediately

---

## 8️⃣ Integrations

**No Real Integrations Required for MVP**

All account connections (Square, Stripe, Bank) are simulated. The backend will generate mock transaction data when user "connects" an account.

**Mock Data Generation:**
- When user connects Square: Generate 20-30 transactions with revenue and expenses
- When user connects Stripe: Generate 15-20 payment transactions
- When user connects Bank: Generate 30-40 mixed transactions
- All transactions include realistic vendors, amounts, dates, and AI categorization

---

## 9️⃣ Testing Strategy (Manual via Frontend)

**Validation Method:** Manual testing through frontend UI only

**Test Requirements:**
- Every task must include a **Manual Test Step** (exact UI action + expected result)
- Every task must include a **User Test Prompt** (concise instruction text)
- After all tasks in a sprint pass → commit and push to `main`
- If any test fails → fix and retest before pushing

**Test Documentation Format:**
```
Manual Test Step: [Exact UI action] → [Expected result]
User Test Prompt: "[Copy-paste friendly instruction]"
```

---

## 🔟 Dynamic Sprint Plan & Backlog

---

## 🧱 S0 – Environment Setup & Frontend Connection

**Objectives:**
- Create FastAPI skeleton with `/api/v1` and `/healthz`
- Connect to MongoDB Atlas using `MONGODB_URI`
- `/healthz` performs DB ping and returns JSON status
- Enable CORS for frontend
- Replace dummy API URLs in frontend with real backend URLs
- Initialize Git only once at root, set default branch to `main`, and push to GitHub
- Create a single `.gitignore` file at root (ignore `__pycache__`, `.env`, `*.pyc`, etc.)

**User Stories:**
- As a developer, I need a working FastAPI server so I can build endpoints
- As a developer, I need MongoDB Atlas connection so I can store data
- As a developer, I need CORS enabled so frontend can call backend
- As a developer, I need Git initialized so I can track changes

**Tasks:**

### Task S0.1: Initialize FastAPI Project Structure
- Create `backend/` directory at project root
- Create `backend/main.py` with FastAPI app instance
- Create `backend/requirements.txt` with dependencies: `fastapi`, `uvicorn[standard]`, `motor`, `pydantic`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[argon2]`, `python-multipart`
- Create `backend/.env.example` with all required env vars
- Create `backend/config.py` for environment variable loading using Pydantic Settings
- Manual Test Step: Run `pip install -r requirements.txt` → All packages install successfully
- User Test Prompt: "Install backend dependencies and verify no errors"

### Task S0.2: Create Health Check Endpoint
- Implement `GET /healthz` endpoint in `backend/main.py`
- Add MongoDB Atlas connection using Motor
- Health check pings database and returns `{ "status": "healthy", "database": "connected", "timestamp": "..." }`
- Manual Test Step: Start backend with `uvicorn main:app --reload`, visit `http://localhost:8000/healthz` → Returns 200 OK with DB status
- User Test Prompt: "Start the backend and visit /healthz endpoint. Confirm database shows 'connected'"

### Task S0.3: Enable CORS for Frontend
- Add CORS middleware to FastAPI app
- Configure allowed origins from `CORS_ORIGINS` env var
- Allow credentials, all methods, and all headers
- Manual Test Step: Start backend, open frontend, check browser console → No CORS errors
- User Test Prompt: "Start both backend and frontend. Open browser console and verify no CORS errors appear"

### Task S0.4: Initialize Git Repository
- Run `git init` at project root (only once)
- Create `.gitignore` at root with: `__pycache__/`, `.env`, `*.pyc`, `.venv/`, `venv/`, `.DS_Store`, `node_modules/`
- Set default branch to `main`: `git branch -M main`
- Create initial commit with project structure
- Create GitHub repository and push
- Manual Test Step: Run `git status` → Shows clean working tree, `git log` shows initial commit
- User Test Prompt: "Verify Git is initialized, .gitignore is working, and code is pushed to GitHub main branch"

**Definition of Done:**
- Backend runs locally on port 8000
- `/healthz` returns success with MongoDB Atlas connection status
- Frontend can make requests to backend without CORS errors
- Git repository initialized with `.gitignore` and pushed to GitHub `main`

**Post-Sprint:** Commit and push to `main`

---

## 🧩 S1 – Basic Auth (Signup / Login / Logout)

**Objectives:**
- Implement JWT-based signup, login, and logout
- Store users in MongoDB with Argon2 password hashing
- Protect one backend route + one frontend page

**User Stories:**
- As a user, I can sign up with email and password
- As a user, I can log in and receive a JWT token
- As a user, I can log out and invalidate my session
- As a user, I can access protected routes only when authenticated

**Tasks:**

### Task S1.1: Create User Model and Database Schema
- Create `backend/models/user.py` with Pydantic User model
- Fields: `id`, `email`, `password_hash`, `first_name`, `last_name`, `business_name`, `created_at`, `updated_at`
- Create `backend/database.py` with Motor async MongoDB client
- Create users collection with email unique index
- Manual Test Step: Start backend, check MongoDB Atlas → `users` collection exists
- User Test Prompt: "Verify users collection is created in MongoDB Atlas"

### Task S1.2: Implement Signup Endpoint
- Create `backend/routers/auth.py` with auth router
- Implement `POST /api/v1/auth/signup`
- Validate email format, password min 6 chars, all fields required
- Hash password with Argon2 using `passlib`
- Store user in MongoDB
- Return user object (without password) and JWT token
- Manual Test Step: Open frontend signup page, fill form, submit → Success message, redirected to connect-accounts
- User Test Prompt: "Create a new account via signup page and verify you're redirected to connect accounts"

### Task S1.3: Implement Login Endpoint
- Implement `POST /api/v1/auth/login` in `backend/routers/auth.py`
- Validate email and password
- Verify password hash with Argon2
- Generate JWT token with user ID and expiration
- Return user object and token
- Manual Test Step: Open frontend login page, enter credentials, submit → Success, redirected to dashboard
- User Test Prompt: "Log in with your account and verify redirection to dashboard"

### Task S1.4: Implement JWT Authentication Middleware
- Create `backend/auth/jwt.py` with JWT token creation and verification
- Create `backend/auth/dependencies.py` with `get_current_user` dependency
- Use `python-jose` for JWT handling
- Verify token signature and expiration
- Return user object from database
- Manual Test Step: Try accessing `/api/v1/auth/me` without token → 401 Unauthorized
- User Test Prompt: "Try accessing a protected endpoint without logging in. Verify you get 401 error"

### Task S1.5: Implement Logout Endpoint
- Implement `POST /api/v1/auth/logout` in `backend/routers/auth.py`
- Clear token on client side (frontend handles this)
- Return success message
- Manual Test Step: Log in, then click logout → Token cleared, redirected to signin, protected pages blocked
- User Test Prompt: "After logout, try refreshing dashboard page. Verify you're redirected to login"

### Task S1.6: Implement Get Current User Endpoint
- Implement `GET /api/v1/auth/me` in `backend/routers/auth.py`
- Require authentication via `get_current_user` dependency
- Return current user profile
- Manual Test Step: Log in, open browser DevTools Network tab, check `/api/v1/auth/me` request → Returns user data
- User Test Prompt: "Log in and check Network tab. Verify /api/v1/auth/me returns your user data"

**Definition of Done:**
- Users can sign up via frontend form
- Users can log in and receive JWT token
- Users can log out and token is cleared
- Protected routes require valid JWT token
- Auth flow works end-to-end in frontend

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S2 – User Profile Management

**Objectives:**
- Implement profile viewing and updating
- Support account deletion
- Add phone, industry, employees, and revenue fields

**User Stories:**
- As a user, I can view my profile information
- As a user, I can update my profile details
- As a user, I can delete my account

**Tasks:**

### Task S2.1: Update User Model with Additional Fields
- Add fields to User model: `phone`, `industry`, `employees`, `monthly_revenue`
- Update database schema
- Manual Test Step: Check MongoDB Atlas → User documents have new fields
- User Test Prompt: "Verify user collection schema includes phone, industry, employees, and monthly_revenue fields"

### Task S2.2: Implement Update Profile Endpoint
- Implement `PUT /api/v1/auth/profile` in `backend/routers/auth.py`
- Accept partial updates (only provided fields)
- Update `updated_at` timestamp
- Return updated user object
- Manual Test Step: Open profile page, change name, save → Success toast, name updated
- User Test Prompt: "Update your profile information and verify changes are saved"

### Task S2.3: Implement Delete Account Endpoint
- Implement `DELETE /api/v1/auth/account` in `backend/routers/auth.py`
- Delete user from database
- Delete all related data (transactions, subscriptions, etc.)
- Return success message
- Manual Test Step: Click "Delete Account", confirm → Account deleted, redirected to signin
- User Test Prompt: "Delete your account and verify you're logged out and redirected to signin"

**Definition of Done:**
- Users can view their profile
- Users can update profile fields
- Users can delete their account
- All related data is cleaned up on deletion

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S3 – Subscription Management

**Objectives:**
- Implement trial subscription tracking
- Support trial activation
- Return subscription status to frontend

**User Stories:**
- As a user, I can start a 14-day free trial
- As a user, I can see my subscription status

**Tasks:**

### Task S3.1: Create Subscription Model
- Create `backend/models/subscription.py` with Pydantic Subscription model
- Fields: `user_id`, `is_trial_active`, `trial_started_at`, `trial_ends_at`, `plan`
- Create subscriptions collection with user_id unique index
- Manual Test Step: Check MongoDB Atlas → `subscriptions` collection exists
- User Test Prompt: "Verify subscriptions collection is created in MongoDB Atlas"

### Task S3.2: Auto-create Subscription on Signup
- Update signup endpoint to create subscription record
- Set `is_trial_active` to false by default
- Manual Test Step: Sign up new user, check MongoDB → Subscription record created
- User Test Prompt: "Sign up and verify subscription record is created in database"

### Task S3.3: Implement Start Trial Endpoint
- Create `backend/routers/subscription.py` with subscription router
- Implement `POST /api/v1/subscription/start-trial`
- Set `is_trial_active` to true, calculate `trial_ends_at` (14 days from now)
- Return trial status
- Manual Test Step: Click "Start Trial" on pricing page → Success message, trial activated
- User Test Prompt: "Start your free trial and verify confirmation message appears"

### Task S3.4: Implement Get Subscription Status Endpoint
- Implement `GET /api/v1/subscription/status` in `backend/routers/subscription.py`
- Return `hasAccess`, `isTrialActive`, `trialEndsAt`, `plan`
- Check if trial has expired (compare `trial_ends_at` with current time)
- Manual Test Step: Open profile page → Shows trial status correctly
- User Test Prompt: "Check your profile page and verify trial status is displayed"

**Definition of Done:**
- Users can start 14-day free trial
- Subscription status is tracked in database
- Frontend displays correct trial status
- Trial expiration is calculated correctly

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S4 – Categories & Mock Data Seeding

**Objectives:**
- Seed categories collection with predefined categories
- Implement categories endpoint
- Ensure categories match frontend expectations

**User Stories:**
- As a user, I can see all available transaction categories
- As a developer, I have predefined categories in the database

**Tasks:**

### Task S4.1: Create Category Model
- Create `backend/models/category.py` with Pydantic Category model
- Fields: `name`, `type`, `color`
- Create categories collection
- Manual Test Step: Check MongoDB Atlas → `categories` collection exists
- User Test Prompt: "Verify categories collection is created in MongoDB Atlas"

### Task S4.2: Seed Categories Data
- Create `backend/seed_data.py` script
- Add all categories from frontend mockData (Inventory, Rent, Utilities, Payroll, Marketing, Office Supplies, Equipment, Professional Fees, Travel, Revenue, Repairs & Maintenance)
- Run seed script on startup if categories collection is empty
- Manual Test Step: Start backend, check MongoDB → 11 categories exist
- User Test Prompt: "Verify all 11 categories are seeded in database"

### Task S4.3: Implement Get Categories Endpoint
- Create `backend/routers/categories.py` with categories router
- Implement `GET /api/v1/categories`
- Return all categories
- Manual Test Step: Open transaction review page → Categories dropdown shows all options
- User Test Prompt: "Open transaction review and verify category dropdown has all options"

**Definition of Done:**
- Categories collection seeded with 11 categories
- Categories endpoint returns all categories
- Frontend can fetch and display categories

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S5 – Account Connection & Transaction Sync

**Objectives:**
- Implement account connection simulation
- Generate mock transactions when account is connected
- Support Square, Stripe, and Bank connections

**User Stories:**
- As a user, I can connect my Square/Stripe/Bank account
- As a user, I can see my connected accounts
- As a user, I can disconnect an account

**Tasks:**

### Task S5.1: Create Connected Account Model
- Create `backend/models/connected_account.py` with Pydantic model
- Fields: `user_id`, `source`, `name`, `connected_at`
- Create connected_accounts collection
- Manual Test Step: Check MongoDB Atlas → `connected_accounts` collection exists
- User Test Prompt: "Verify connected_accounts collection is created in MongoDB Atlas"

### Task S5.2: Implement Connect Account Endpoint
- Create `backend/routers/accounts.py` with accounts router
- Implement `POST /api/v1/accounts/connect`
- Store connected account in database
- Return account object
- Manual Test Step: Click "Connect Account" on connect-accounts page → Success message
- User Test Prompt: "Connect a Square account and verify success message"

### Task S5.3: Implement Get Connected Accounts Endpoint
- Implement `GET /api/v1/accounts/connected` in `backend/routers/accounts.py`
- Return all user's connected accounts
- Manual Test Step: Refresh connect-accounts page → Shows connected account
- User Test Prompt: "Refresh page and verify your connected account is displayed"

### Task S5.4: Implement Disconnect Account Endpoint
- Implement `DELETE /api/v1/accounts/:id` in `backend/routers/accounts.py`
- Delete account from database
- Return success message
- Manual Test Step: Click "Disconnect" → Account removed
- User Test Prompt: "Disconnect your account and verify it's removed"

### Task S5.5: Implement Transaction Sync with Mock Data Generation
- Create `backend/services/transaction_generator.py` with mock data generation logic
- Implement `POST /api/v1/transactions/sync` in `backend/routers/transactions.py`
- Generate 20-30 realistic transactions based on source (Square/Stripe/Bank)
- Include AI categorization with confidence scores and explanations
- Store transactions in database
- Manual Test Step: Click "Continue to Sync" → Progress bar completes, transactions created
- User Test Prompt: "Complete sync process and verify transactions are generated"

**Definition of Done:**
- Users can connect accounts (Square, Stripe, Bank)
- Connected accounts are stored and displayed
- Transaction sync generates realistic mock data
- All transactions have AI categorization

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S6 – Transaction Management

**Objectives:**
- Implement transaction CRUD operations
- Support filtering and search
- Enable category updates and status changes

**User Stories:**
- As a user, I can view all my transactions
- As a user, I can filter transactions by status
- As a user, I can search transactions by vendor or category
- As a user, I can update transaction category
- As a user, I can approve transactions

**Tasks:**

### Task S6.1: Create Transaction Model
- Create `backend/models/transaction.py` with Pydantic Transaction model
- Fields: `user_id`, `date`, `vendor`, `amount`, `category`, `confidence`, `status`, `explanation`, `payment_method`, `original_description`
- Create transactions collection with user_id index
- Manual Test Step: Check MongoDB Atlas → `transactions` collection exists
- User Test Prompt: "Verify transactions collection is created in MongoDB Atlas"

### Task S6.2: Implement Get All Transactions Endpoint
- Create `backend/routers/transactions.py` with transactions router
- Implement `GET /api/v1/transactions`
- Support query params: `status` (filter), `search` (vendor/category)
- Return filtered transactions
- Manual Test Step: Open transactions page → Shows all transactions
- User Test Prompt: "Open transactions page and verify all transactions are displayed"

### Task S6.3: Implement Get Single Transaction Endpoint
- Implement `GET /api/v1/transactions/:id` in `backend/routers/transactions.py`
- Verify transaction belongs to user
- Return transaction details
- Manual Test Step: Click on a transaction → Details displayed
- User Test Prompt: "Click on a transaction and verify details are shown"

### Task S6.4: Implement Update Transaction Endpoint
- Implement `PUT /api/v1/transactions/:id` in `backend/routers/transactions.py`
- Support updating `category` and `status`
- Update `updated_at` timestamp
- Return updated transaction
- Manual Test Step: Change transaction category → Success toast, category updated
- User Test Prompt: "Change a transaction's category and verify it's saved"

### Task S6.5: Implement Transaction Filtering
- Add filtering logic to GET transactions endpoint
- Filter by status: all, auto-approved, needs-review, manual
- Manual Test Step: Select "Needs Review" filter → Shows only needs-review transactions
- User Test Prompt: "Filter transactions by 'Needs Review' and verify results"

### Task S6.6: Implement Transaction Search
- Add search logic to GET transactions endpoint
- Search by vendor name or category name (case-insensitive)
- Manual Test Step: Type "Sysco" in search → Shows matching transactions
- User Test Prompt: "Search for 'Sysco' and verify matching transactions appear"

**Definition of Done:**
- Users can view all transactions
- Filtering by status works correctly
- Search by vendor/category works correctly
- Users can update transaction category and status
- All changes persist in database

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S7 – Dashboard Analytics

**Objectives:**
- Calculate financial statistics from transactions
- Generate revenue vs expenses trend data
- Create expense breakdown by category
- Provide recent transactions and alerts

**User Stories:**
- As a user, I can see my monthly revenue, profit, expenses, and cash balance
- As a user, I can see revenue vs expenses trend chart
- As a user, I can see expense breakdown pie chart
- As a user, I can see recent transactions on dashboard
- As a user, I can see financial alerts

**Tasks:**

### Task S7.1: Implement Dashboard Stats Endpoint
- Create `backend/routers/dashboard.py` with dashboard router
- Implement `GET /api/v1/dashboard/stats`
- Calculate from transactions: `monthlyRevenue`, `totalExpenses`, `netProfit`, `cashBalance`
- Calculate percentage changes (mock with random +/- 5-15%)
- Manual Test Step: Open dashboard → Stats cards show correct values
- User Test Prompt: "Open dashboard and verify stats cards display financial metrics"

### Task S7.2: Implement Revenue Trend Endpoint
- Implement `GET /api/v1/dashboard/revenue-trend` in `backend/routers/dashboard.py`
- Group transactions by date (last 7 days)
- Calculate daily revenue and expenses
- Return array of `{ date, revenue, expenses }`
- Manual Test Step: Open dashboard → Revenue vs Expenses chart displays
- User Test Prompt: "Verify the revenue vs expenses chart shows data for last 7 days"

### Task S7.3: Implement Expense Breakdown Endpoint
- Implement `GET /api/v1/dashboard/expense-breakdown` in `backend/routers/dashboard.py`
- Group expenses by category
- Calculate total amount and percentage for each category
- Include category color from categories collection
- Manual Test Step: Open dashboard → Expense breakdown pie chart displays
- User Test Prompt: "Verify expense breakdown pie chart shows category distribution"

### Task S7.4: Implement Recent Transactions Endpoint
- Implement `GET /api/v1/dashboard/recent-transactions` in `backend/routers/dashboard.py`
- Return 5 most recent transactions sorted by date
- Manual Test Step: Open dashboard → Recent transactions section shows 5 items
- User Test Prompt: "Verify recent transactions section shows your latest 5 transactions"

### Task S7.5: Implement Alerts Endpoint
- Implement `GET /api/v1/dashboard/alerts` in `backend/routers/dashboard.py`
- Generate smart alerts based on transaction patterns:
  - Unusual expenses (3x typical amount)
  - Upcoming payroll
  - Revenue trends
- Return array of alerts with type, title, message
- Manual Test Step: Open dashboard → Alerts panel shows relevant alerts
- User Test Prompt: "Verify alerts panel displays financial notifications"

**Definition of Done:**
- Dashboard stats calculate correctly from transactions
- Revenue trend chart displays last 7 days
- Expense breakdown shows category distribution
- Recent transactions display correctly
- Alerts generate based on transaction patterns

**Post-Sprint:** Commit and push to `main`

---

## 🧱 S8 – FinSense AI Chat

**Objectives:**
- Implement AI chat endpoint
- Store conversation history
- Generate contextual responses based on user's financial data

**User Stories:**
- As a user, I can chat with AI assistant about my finances
- As a user, I can see conversation history
- As a user, I receive relevant answers based on my transaction data

**Tasks:**

### Task S8.1: Create AI Conversation Model
- Create `backend/models/ai_conversation.py` with Pydantic model
- Fields: `user_id`, `conversation_id`, `messages` (array)
- Create ai_conversations collection
- Manual Test Step: Check MongoDB Atlas → `ai_conversations` collection exists
- User Test Prompt: "Verify ai_conversations collection is created in MongoDB Atlas"

### Task S8.2: Implement AI Chat Endpoint
- Create `backend/routers/ai.py` with AI router
- Implement `POST /api/v1/ai/chat`
- Accept message and optional conversation_id
- Generate conversation_id if not provided (UUID)
- Store user message in conversation
- Manual Test Step: Send message in AI assistant → Response received
- User Test Prompt: "Send a message to AI assistant and verify you get a response"

### Task S8.3: Implement Mock AI Response Generation
- Create `backend/services/ai_service.py` with response generation logic
- Analyze user's transactions to provide contextual answers
- Handle common queries:
  - "How much did I spend on X?"
  - "What was my profit in Y?"
  - "Show me my biggest expenses"
- Generate realistic responses with specific numbers from user's data
- Manual Test Step: Ask "How much did I spend on supplies?" → Receives detailed answer with amounts
- User Test Prompt: "Ask about your supply expenses and verify AI provides specific amounts"

### Task S8.4: Store AI Response in Conversation
- Save AI response to conversation messages array
- Update conversation `updated_at` timestamp
- Return response and conversation_id
- Manual Test Step: Send multiple messages → Conversation persists
- User Test Prompt: "Send multiple messages and verify conversation continues"

**Definition of Done:**
- Users can send messages to AI assistant
- AI generates contextual responses based on transaction data
- Conversation history is stored and persisted
- Multiple messages in same conversation work correctly

**Post-Sprint:** Commit and push to `main`

---

## ✅ Final Checklist

**Before Completion:**
- [ ] All sprints completed and pushed to `main`
- [ ] All manual tests passed via frontend UI
- [ ] MongoDB Atlas collections created and populated
- [ ] All API endpoints functional
- [ ] CORS configured correctly
- [ ] JWT authentication working
- [ ] Transaction categorization with AI explanations
- [ ] Dashboard displays accurate metrics
- [ ] AI assistant provides contextual responses
- [ ] No console errors in frontend
- [ ] Git repository clean and up to date

**Deployment Readiness:**
- [ ] `.env.example` file documented
- [ ] `requirements.txt` complete
- [ ] MongoDB Atlas connection string configured
- [ ] JWT secret generated (min 32 chars)
- [ ] CORS origins configured for production
- [ ] All sensitive data in `.env` (not committed)

---

## 📚 Additional Notes

**AI Categorization Logic:**
- Use pattern matching on vendor names
- Assign confidence scores based on match quality:
  - Exact vendor match: 0.95-0.99
  - Partial vendor match: 0.80-0.90
  - Category inference: 0.70-0.85
  - Uncertain: 0.60-0.75
- Generate explanations that reference:
  - Historical patterns
  - Vendor recognition
  - Amount comparisons
  - Frequency analysis

**Mock Data Generation Guidelines:**
- Use realistic vendor names for each category
- Vary amounts within reasonable ranges
- Distribute dates across last 30 days
- Mix of auto-approved (70%), needs-review (25%), manual (5%)
- Include both revenue (negative amounts) and expenses (positive amounts)

**Error Handling:**
- Return 400 for validation errors
- Return 401 for authentication errors
- Return 403 for authorization errors
- Return 404 for not found errors
- Return 500 for server errors
- Always include error message in response

---

**END OF BACKEND DEVELOPMENT PLAN**
