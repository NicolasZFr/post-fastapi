from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel # Validar el tipo de dato que se recibe
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "Hello World, I'm Nicolás"}
# uvicorn main:app --reload

@app.get("/posts")
async def login():
    return {"data": "These are your posts"}


# async def create_posts(payLoad: dict = Body(...)):
    # print(payLoad)
    # return {"response": f"Post '{payLoad['title']}' was created succesfully",
    #         "title": payLoad['title'],
    #         "content": payLoad['content']
    #         }
@app.post("/posts")
async def create_posts(post: Post):
    print(post.model_dump())
    return {"response": f"Post '{post.title}' was created succesfully",
            "data" : post
            }