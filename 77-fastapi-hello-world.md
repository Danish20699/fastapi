# Lab 77: FastAPI Core Routing, Static File Serving & Parameter Validation

![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ASGI](https://img.shields.io/badge/ASGI-Uvicorn-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hands--On%20Lab-orange?style=for-the-badge)

---

## 📌 1. Lab Objectives & Roadmap

In this lab, you will build and master the foundational building blocks of FastAPI from scratch. You will write code incrementally, run the server, inspect responses, test edge cases, and discover how FastAPI automates validation, serialization, and documentation.

### Learning Goals:
1. **Application Lifecycle & Instantiation**: Initializing the `FastAPI()` application instance.
2. **HTTP Verb Decorators & Routing**: Understanding `@app.get()` and `@app.post()`.
3. **Automatic Serialization**: Returning raw Python dictionaries and seeing them converted to RFC-compliant JSON responses.
4. **Serving Web Assets**: Using `FileResponse` from `fastapi.responses` to serve standalone HTML files (`index.html`, `contact.html`).
5. **Path Parameters & Runtime Type Coercion**: Handling dynamic paths like `/users/{id}` with automatic validation and automatic HTTP 422 error generation.
6. **Query Parameters**: Handling optional filtering parameters (`/blog?limit=10&published=true`).
7. **Pydantic Request Bodies**: Accepting structured JSON payloads on POST endpoints.
8. **Interactive Sandboxing**: Exploring and executing endpoints with Swagger UI (`/docs`) and ReDoc (`/redoc`).

```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                FastAPI Request Pipeline                           │
└───────────────────────────────────────────────────────────────────────────────────┘
   HTTP Request (Client)
         │
         ▼
   ┌───────────────┐
   │ Uvicorn ASGI  │  Handles lightning-fast network sockets and HTTP parsing
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ FastAPI Router│  Matches URL path and HTTP verb (GET, POST, etc.)
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ Pydantic Type │  Parses path / query / body arguments
   │  Validation   │  ❌ If invalid ──► Returns 422 Unprocessable Entity
   └───────┬───────┘
           │ ✅ If valid
           ▼
   ┌───────────────┐
   │ Route Handler │  Executes your Python function: def read_user(id: int): ...
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │ Serialization │  Converts dict / Pydantic model / FileResponse to HTTP Response
   └───────┬───────┘
           │
           ▼
   HTTP 200 JSON / HTML Response to Client
```

---

## 🏛️ 2. Step-by-Step Code Breakdown

### 2.1 The Application Instance
```python
from fastapi import FastAPI

app = FastAPI(
    title="Hello World Learning API",
    description="Hands-on FastAPI walkthrough covering routing, parameters, and HTML serving",
    version="1.0.0"
)
```
* **`FastAPI` Class**: The central ASGI application class inherited from Starlette.
* **`app` variable**: The callable instance that Uvicorn binds to when starting the web server (`uvicorn main:app`).
* Metadata arguments like `title`, `description`, and `version` directly populate the header of the Swagger UI documentation.

---

### 2.2 Serving JSON at the Root (`GET /`)
```python
@app.get("/")
def read_root():
    return {"message": "Hello-World"}
```
* **`@app.get("/")`**: A path operation decorator. It instructs FastAPI: *"Whenever an HTTP `GET` request arrives for path `/`, run this function."*
* **Automatic JSON Conversion**: In traditional frameworks like Flask, you must do `jsonify({"message": "Hello-World"})`. In FastAPI, any returned Python `dict`, `list`, or Pydantic model is automatically encoded into JSON with header `content-type: application/json`.

---

### 2.3 Serving Static HTML Pages (`FileResponse`)
```python
from fastapi.responses import FileResponse

@app.get("/new-home")
def get_new_home():
    return FileResponse("index.html")

@app.get("/contact")
def get_contact_page():
    return FileResponse("contact.html")
```
* **`FileResponse`**: A specialized Starlette response that streams a file directly from the filesystem to the browser.
* Sets proper MIME headers (e.g. `text/html; charset=utf-8`).
* When the client navigates to `http://127.0.0.1:8000/new-home`, the browser receives and renders `index.html`.

---

### 2.4 Path Parameters & Automatic Type Coercion (`/users/{id}`)
```python
@app.get("/users")
def get_users_page():
    return {"message": "This is user page"}

@app.get("/users/{id}")
def get_user_by_id(id: int):
    return {"message": f"This is user {id} page"}

@app.get("/users/{id}/contact")
def get_user_contact(id: int):
    return {"message": f"This is user {id} contact page. His contact no. is 911"}
```

#### What makes this powerful?
1. **Path Variable Matching**: The `{id}` in the decorator matches the argument `id` in `def get_user_by_id(id: int)`.
2. **Type Coercion**: Even though HTTP URLs are pure strings (e.g. `"/users/25"`), FastAPI sees `id: int` and automatically converts `"25"` into the Python integer `25`.
3. **Automatic Error Handling**: If someone requests `/users/john`, FastAPI immediately halts execution and returns an HTTP 422:
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "john"
    }
  ]
}
```

> [!WARNING]
> **Function Naming Best Practice**:
> In the original screenshot code, multiple routes reused `def read_root()` or `def read_user()`. While FastAPI's router allows this because decorators register the route, Python overwrites the function in the module namespace. Always give each endpoint a unique, descriptive function name (e.g., `read_root`, `get_new_home`, `get_user_by_id`).

> [!IMPORTANT]
> **Route Order Precedence**:
> If you have a static path like `/users/all` and a dynamic path `/users/{id}`, you **must** declare `@app.get("/users/all")` **before** `@app.get("/users/{id}")`. Otherwise, FastAPI evaluates routes sequentially from top to bottom and would interpret `"all"` as an `{id}`!

---

### 2.5 Query Parameters (`GET /blog`)
In HTTP, parameters passed after the `?` mark are **query parameters**.
```python
from typing import Optional

@app.get("/blog")
def get_blogs(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    return {
        "limit": limit,
        "published": published,
        "sort": sort,
        "data": f"Displaying {limit} blogs where published={published}"
    }
```
* When function parameters are **not** present in the `@app.get(...)` path, FastAPI automatically reads them from the query string!
* Example calls:
  * `/blog` -> Uses defaults: `limit=10`, `published=True`.
  * `/blog?limit=25` -> `limit=25`, `published=True`.
  * `/blog?limit=5&published=false` -> `limit=5`, `published=False`.
* FastAPI automatically coerces boolean strings: `"yes"`, `"1"`, `"true"`, `"on"` all map to `True`; `"no"`, `"0"`, `"false"`, `"off"` all map to `False`.

---

### 2.6 Pydantic Request Bodies (`POST`)
When clients submit form data or send JSON payloads:
```python
from pydantic import BaseModel

class BlogCreate(BaseModel):
    id: int
    title: str
    body: str

class ContactSubmission(BaseModel):
    name: str
    email: str
    message: str

@app.post("/blog")
def create_blog(blog: BlogCreate):
    return {
        "message": "Blog created successfully",
        "blog": blog
    }

@app.post("/api/contact")
def receive_contact_form(form: ContactSubmission):
    return {
        "status": "success",
        "message": f"Thank you {form.name}! We received your message and will reply to {form.email} shortly."
    }
```
* **AJAX Integration**: The `contact.html` frontend makes a `fetch('/api/contact')` sending `{ name, email, message }`. This endpoint accepts the payload, validates it via Pydantic, and returns a confirmation JSON that `contact.html` displays on screen!

---

## 🛠️ 3. Complete Reference Code for `hello-world/main.py`

Here is the clean, production-ready code with all endpoints and proper typing:

```python
from typing import Optional
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Initialize the Application
app = FastAPI(
    title="FastAPI Hello World & Fundamentals",
    description="Core tutorial for routing, static files, path/query parameters, and Pydantic models.",
    version="1.0.0"
)

# Base directory for reliably locating HTML files
BASE_DIR = Path(__file__).resolve().parent

# ----------------------------------------------------
# 1. Root & Static HTML Serving Endpoints
# ----------------------------------------------------
@app.get("/")
def read_root():
    """Returns a basic JSON greeting."""
    return {"message": "Hello-World"}


@app.get("/new-home")
def get_new_home():
    """Serves the index.html landing card."""
    return FileResponse(BASE_DIR / "index.html")


@app.get("/contact")
def get_contact_page():
    """Serves the interactive contact.html form."""
    return FileResponse(BASE_DIR / "contact.html")


# ----------------------------------------------------
# 2. Path Parameters & Dynamic Routes
# ----------------------------------------------------
@app.get("/users")
def get_users():
    """Static users endpoint."""
    return {"message": "This is user page"}


@app.get("/users/{id}")
def get_user_by_id(id: int):
    """Dynamic user route with integer type validation."""
    return {"message": f"This is user {id} page"}


@app.get("/users/{id}/contact")
def get_user_contact(id: int):
    """Nested user contact route."""
    return {"message": f"This is user {id} contact page. His contact no. is 911"}


# ----------------------------------------------------
# 3. Query Parameters & Path Combinations
# ----------------------------------------------------
@app.get("/blog/{id}")
def get_blog_post(id: int):
    """Fetch a single blog by ID."""
    return {"Type": "blog", "id": id}


@app.get("/blog")
def list_blogs(limit: int = 10, published: bool = True, search: Optional[str] = None):
    """List blogs with query parameters."""
    return {
        "limit": limit,
        "published": published,
        "search": search,
        "message": f"Showing {limit} blogs (published={published})"
    }


# ----------------------------------------------------
# 4. Pydantic Models & POST Endpoints
# ----------------------------------------------------
class BlogPost(BaseModel):
    id: int
    title: str
    body: str


class ContactMessage(BaseModel):
    name: str
    email: str
    message: str


@app.post("/blog")
def create_blog(blog: BlogPost):
    """Create a new blog post via JSON request body."""
    return {"message": "Blog created successfully", "data": blog}


@app.post("/api/contact")
def submit_contact(contact: ContactMessage):
    """Endpoint consumed by the AJAX form in contact.html."""
    return {
        "status": "success",
        "message": f"Thank you {contact.name}, your message has been received!"
    }
```

---

## 🚀 4. How to Run and Test

### Step 1: Open PowerShell in the `hello-world` folder
```powershell
cd c:\Users\danis\Desktop\fastapi\hello-world
```

### Step 2: Start the Uvicorn ASGI Server
```powershell
uvicorn main:app --reload
```
* `main`: Refers to `main.py`
* `app`: Refers to the `app = FastAPI()` object inside `main.py`
* `--reload`: Automatically reloads the server whenever you save edits!

### Step 3: Test All Routes
| What to Test | URL to Open in Browser | What You Should See |
|---|---|---|
| Root API | `http://127.0.0.1:8000/` | `{"message":"Hello-World"}` |
| Home Page | `http://127.0.0.1:8000/new-home` | Styled HTML Card with Button |
| Contact Form | `http://127.0.0.1:8000/contact` | Working form that posts to `/api/contact` |
| Valid User ID | `http://127.0.0.1:8000/users/42` | `{"message":"This is user 42 page"}` |
| Invalid User ID | `http://127.0.0.1:8000/users/alice` | **422 Unprocessable Entity** error! |
| Query Parameters | `http://127.0.0.1:8000/blog?limit=5&published=false` | Custom limits returned as JSON |
| Swagger Docs | `http://127.0.0.1:8000/docs` | Interactive API documentation |

---

## 💡 5. Key Takeaways & Best Practices

1. **Path parameters** are defined inside curly braces `{param}` in the route path and declared as function arguments.
2. **Query parameters** are function arguments that do *not* appear in the route path.
3. **Type annotations** (`id: int`, `published: bool`) are not just comments; FastAPI uses them at runtime to validate incoming values and generate accurate OpenAPI schemas.
4. Always use `Path(__file__).resolve().parent / "filename.html"` when serving files with `FileResponse` so the server works regardless of where the command line was launched from.

