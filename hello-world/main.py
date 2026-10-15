from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel

# 1. create the application instance
app = FastAPI()

# 2. path operation decorator and Handler function
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 3. serving static html files 
@app.get("/new-home")
def get_new_home():
    return FileResponse("index.html")

@app.get("/contact")
def get_contact():
    return FileResponse("contact.html")

# 4. Static users page
@app.get("/users")
def get_users():
    return {"message": "This is user page"}

# 5. Dynamic route with integer validation
@app.get("/users/{id}")
def read_user(id: int):
    return {"message": f"This is user {id} page"}

# 6. Nested dynamic route
@app.get("/users/{id}/contact")
def read_user_contact(id: int):
    return {"message": f"This is user {id} contact page. His contact no. is 911"}

# 7. Blog Path Parameter
@app.get("/blog/{id}")
def get_blog(id: int):
    return {"Type": "blog", "id": id}

@app.get("/blog/{id}/comments")
def get_blog_comments(id: int):
    return {"Type": "Comments", "Blog-id": id}

# 8. Blog Query Parameters
@app.get("/blog")
def list_blogs(
    limit: int = 10, 
    published: bool = True, 
    sort: Optional[str] = None
):
    return {
        "Type": "blog",
        "limit": limit,
        "published": published,
        "sort": sort,
        "data": f"Showing {limit} posts (published={published})"
    }


# 9. Pydantic Model & POST for Blog
class Blog(BaseModel):
    id: int
    title: str
    body: str
    published: Optional[bool] = True

@app.post("/blog")
def create_blog(new_blog: Blog):
    return {
        "message": "Blog is saved",
        "Title": new_blog.title,
        "Body": new_blog.body,
        "id": new_blog.id
    }


# 10. Pydantic Model & POST for Contact Form
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/api/contact")
def submit_contact(data: ContactForm):
    return {
        "status": "success",
        "message": f"Thank you {data.name}! We received your message and will email you at {data.email}."
    }