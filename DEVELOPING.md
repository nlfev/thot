# Development Guide - NLF Database Application

This guide provides essential information for developers working on the NLF Database project.

## Quick Start for New Developers

### 1. Clone and Setup Backend

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
copy .env.example .env
# Edit .env with your local database credentials
```

### 2. Setup Frontend

```bash
cd frontend
npm install

# Create .env.local
cat > .env.local << EOF
VITE_BACKEND_URL=http://localhost:8000
VITE_ROOT_MOUNT=
EOF
```

### 3. Initialize Database

```bash
cd backend
python scripts/init_db.py
```

This will:
- Run Alembic migrations to create tables
- Seed default roles and permissions

### 4. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m app.main
# Server: http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# App: http://localhost:5173
```

---

## Application Configuration

### How It Works

The frontend loads configuration from the backend at startup:

1. **Frontend** starts → calls `useAppStore().initializeConfig()`
2. **Backend** endpoint: `GET /api/v1/config` is called
3. **Configuration** is loaded from `backend/config.py` and cached in Pinia store
4. **Components** access config via `appStore.getConfig(key)`

### Configuration Endpoint

```
GET /api/v1/config
```

Returns public application configuration:
```json
{
  "appName": "NLF Database",
  "appVersion": "1.0.0",
  "companyName": "Your Company",
  "logoUrl": "/static/logo.png",
  "copyrightYear": 2026,
  "itemsPerPageDefault": 10,
  "itemsPerPageOptions": [10, 20, 50],
  "tokenRefreshIntervalMinutes": 55,
  "sessionTimeoutMinutes": 60,
  "features": {
    "otp": true,
    "emailVerification": true,
    "corporateApprovals": true
  },
  "languages": {
    "en": "English",
    "de": "Deutsch"
  },
  "defaultLanguage": "en"
}
```

### Modifying Configuration

1. **Edit** `backend/config.py`:
   ```python
   APP_NAME = "My Company Database"
   COMPANY_NAME = "My Company"
   ```

2. **Backend restarts automatically** (in development with `--reload`)

3. **Frontend fetches new config** on next app reload - no code changes needed!

---

## Database Migrations with Alembic

### Standard Workflow

#### 1. Modify a Model

Edit any model file in `backend/app/models/`:

```python
# backend/app/models/user.py
class User(BaseModel):
    __tablename__ = "users"
    
    # ... existing fields ...
    
    # Add new field:
    phone_number = Column(String(20), nullable=True)
```

#### 2. Generate Migration

```bash
cd backend
alembic revision --autogenerate -m "add phone field to users"
```

This creates a new file in `alembic/versions/` with:
- `upgrade()` - SQL operations to apply the change
- `downgrade()` - SQL operations to reverse the change

#### 3. Review Migration

**Always review the generated migration before applying!**

```bash
cat alembic/versions/002_add_phone_field_to_users.py
```

Look for:
- Correct table names
- Correct column names and types
- Foreign key constraints
- Index definitions

#### 4. Apply Migration

```bash
alembic upgrade head
```

This runs all pending migrations. You'll see output like:

```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 002_...
```

#### 5. Test the Changes

Run your test suite:

```bash
# Backend tests
pytest tests/ -v

# Frontend tests
npm run test
```

---

### Common Migration Scenarios

#### Adding a New Column

```bash
alembic revision --autogenerate -m "add email verification field"
```

Generated migration looks like:
```python
def upgrade():
    op.add_column('users', 
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false')
    )

def downgrade():
    op.drop_column('users', 'email_verified')
```

#### Removing a Column

```bash
alembic revision --autogenerate -m "remove deprecated field"
```

Generated migration:
```python
def upgrade():
    op.drop_column('users', 'deprecated_field')

def downgrade():
    op.add_column('users',
        sa.Column('deprecated_field', sa.String(255), nullable=True)
    )
```

#### Renaming a Column

```bash
alembic revision --autogenerate -m "rename username to login"
```

#### Creating a New Table

Add the model file to `backend/app/models/`, then:

```bash
alembic revision --autogenerate -m "create audit log table"
```

#### Adding Index or Constraint

Modify model relationships/constraints, then:

```bash
alembic revision --autogenerate -m "add unique constraint on email"
```

---

### Migration Management

#### View Current Revision

```bash
alembic current
# Output: 002_add_phone_field_to_users
```

#### View Migration History

```bash
alembic history
# Output:
# <base> -> 001_initial_migration, create users and roles tables
# 001_initial_migration -> 002_add_phone_field_to_users, add phone field to users
```

#### Downgrade One Migration

```bash
alembic downgrade -1
```

Data loss warning: Downgrades may lose data depending on the migration!

#### Downgrade to Specific Revision

```bash
alembic downgrade 001_initial_migration
```

---

### Troubleshooting Migrations

#### "No changes detected in models"

**Cause:** Alembic can't find differences between models and database.

**Solutions:**
1. Ensure model changes are saved
2. Check `alembic/env.py` correctly imports `target_metadata`
3. Verify the model is imported in `app/models/__init__.py`

#### "Could not locate a marked branch point"

**Cause:** Migration history is inconsistent.

**Solution:** Check `alembic_version` table:
```bash
psql nlf_db -c "SELECT * FROM alembic_version;"
```

#### Migration fails with SQL error

**Cause:** Generated SQL may need manual adjustment.

**Solution:**
1. Edit the `.py` file in `alembic/versions/`
2. Modify the SQL in `upgrade()` or `downgrade()`
3. Re-run: `alembic upgrade head`

---

## Running Tests

### Backend Unit Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_user_service.py -v

# Run with coverage
pytest tests/ -v --cov=app

# Run with markers
pytest tests/ -v -m "not slow"
```

### Frontend Unit Tests

```bash
cd frontend

# Run tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage
```

---

## API Development

### Adding a New Endpoint

1. **Create route in `backend/app/routes/`:**

```python
# backend/app/routes/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItemResponse, ItemCreateRequest
from app.services import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=list[ItemResponse])
async def list_items(db: Session = Depends(get_db)):
    """List all items"""
    return ItemService.list_items(db)

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new item"""
    return ItemService.create_item(db, item)
```

2. **Create schema in `backend/app/schemas/__init__.py`:**

```python
class ItemCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class ItemResponse(ItemCreateRequest):
    id: UUID
    created_on: datetime
    
    class Config:
        from_attributes = True
```

3. **Create service in `backend/app/services/item_service.py`:**

```python
class ItemService:
    @staticmethod
    def list_items(db: Session) -> list:
        return db.query(Item).all()
    
    @staticmethod
    def create_item(db: Session, data: ItemCreateRequest) -> Item:
        item = Item(name=data.name, description=data.description)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
```

4. **Register route in `backend/app/routes/api.py`:**

```python
from app.routes import items

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(items.router)
```

5. **Create tests in `backend/tests/test_items.py`:**

```python
def test_list_items(client, db):
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## Frontend Development

### Project Structure

```
frontend/src/
├── components/       # Reusable Vue components
├── views/           # Page components (routed)
├── stores/          # Pinia state management
├── services/        # API services
├── locales/         # i18n translations
├── router/          # Vue Router configuration
└── App.vue          # Root component
```

### Creating a New Page

1. **Create view component:**

```vue
<!-- frontend/src/views/ItemsPage.vue -->
<template>
  <div class="items-page">
    <h1>{{ $t('items.title') }}</h1>
    
    <button @click="createItem">{{ $t('items.create') }}</button>
    
    <div v-if="items.length">
      <div v-for="item in items" :key="item.id" class="item-card">
        {{ item.name }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useItemStore } from '@/stores/items'

const itemStore = useItemStore()
const items = ref([])

onMounted(async () => {
  await itemStore.fetchItems()
  items.value = itemStore.items
})

const createItem = () => {
  // Handle create
}
</script>
```

2. **Create Pinia store:**

```js
// frontend/src/stores/items.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as itemService from '@/services/items'

export const useItemStore = defineStore('items', () => {
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchItems() {
    loading.value = true
    try {
      items.value = await itemService.listItems()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    return await itemService.createItem(data)
  }

  return { items, loading, error, fetchItems, create }
})
```

3. **Add route:**

```js
// frontend/src/router/index.js
const routes = [
  // ...
  {
    path: '/items',
    name: 'Items',
    component: () => import('@/views/ItemsPage.vue'),
    meta: { requiresAuth: true }
  }
]
```

4. **Add i18n translations:**

```js
// frontend/src/locales/messages.js
const messages = {
  en: {
    items: {
      title: 'Items',
      create: 'Create Item'
    }
  },
  de: {
    items: {
      title: 'Elemente',
      create: 'Element erstellen'
    }
  }
}
```

---

## Code Style & Quality

### Backend

**Format code with Black:**
```bash
black backend/app
```

**Sort imports with isort:**
```bash
isort backend/app
```

**Lint with flake8:**
```bash
flake8 backend/app --max-line-length=120
```

### Frontend

**Format with Prettier (if configured):**
```bash
npm run format
```

**Lint with ESLint:**
```bash
npm run lint
```

---

## Debugging

### Backend Debugging

**Print Debugging:**
```python
import logging
logger = logging.getLogger(__name__)

logger.debug(f"User ID: {user_id}")
logger.info("Processing started")
logger.warning("Potential issue")
logger.error(f"Error occurred: {str(e)}")
```

**VS Code Debugger:**

1. Set breakpoint by clicking line number
2. Launch "Python: FastAPI" from debug menu
3. Requests will pause at breakpoints

### Frontend Debugging

**Vue DevTools:**
- Install [Vue DevTools extension](https://devtools.vuejs.org/)
- Inspect component state and events

**Console Logging:**
```js
console.log('value:', value)
console.error('error:', error)
```

**VS Code Debugger:**
1. Install "Firefox Debugger" extension
2. Set breakpoints
3. Press F5 to launch Firefox with debugger

---

## Environment Variables

### Backend `.env`

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=nlf_user
DB_PASSWORD=your_password
DB_NAME=nlf_db

# Security
SECRET_KEY=your-secret-key-here

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=NLF Database

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend `.env.local`

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## Common Development Tasks

### Reset Database (Development Only)

```bash
# Drop and recreate database
psql -U postgres -c "DROP DATABASE nlf_db;"
psql -U postgres -c "CREATE DATABASE nlf_db OWNER nlf_user;"

# Re-run migrations
python scripts/init_db.py
```

### View Database Tables

```bash
psql nlf_db -U nlf_user

# List tables
\dt

# Describe table
\d users

# View data
SELECT * FROM users;
```

### Create a Test User

```python
# In Python shell:
from app.services import UserService
from app.database import SessionLocal

db = SessionLocal()
user = UserService.create_user(
    db=db,
    username="testuser",
    email="test@example.com",
    password="TestPassword123!",
    is_first_user=False
)
print(f"Created user: {user.id}")
```

---

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Pinia Store](https://pinia.vuejs.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Getting Help

1. Check the [install.md](install.md) for setup issues
2. Review the [README.md](README.md) for project overview
3. Look at existing tests for usage examples
4. Check Alembic history: `alembic history`
5. Ask senior developers or create GitHub issues

---

**Last Updated:** March 1, 2026

