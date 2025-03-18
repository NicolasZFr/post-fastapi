from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from fastapi.responses import Response

from pydantic import BaseModel # Validar el tipo de dato que se recibe
from typing import Optional, Union

# Importar funciones de otro archivo
from app.main_functions import find_post

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: Union[bool,None] = None
    rating: Optional[float] = None


my_posts = [
    {
        "title": "El retrato de Dorian Gray",
        "content": "Y el joven Dorian se convirtió en aquel viejo de la pintura",
        "published": True,
        "rating": 4.5,
        "id": 1
    },
    {
        "title": "El principito",
        "content": "Él era un zorro semejante a diezmil otros, pero yo lo hice mi amigo y ahora es único en el mundo",
        "published": True,
        "rating": 5.0,
        "id": 2
    }
]

# ------------------- Endpoints -------------------
# GET /posts --------------------------------------

@app.get("/")
async def root():
    return {"message": "Hello World, I'm Nicolás"}
# uvicorn app.main:app --reload

@app.get("/posts")
async def get_posts_list():
    return {"data": my_posts}

@app.get("/posts/latest")
async def get_latest_post():
    return {"response":my_posts[-1]}

@app.get("/posts/{id}")
async def get_post_object(id:int):
    post = find_post(id, my_posts)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"response": f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
        
    return {"response": post}


# POST /posts --------------------------------------
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    my_post = post.model_dump()
    my_post["id"] = len(my_posts) + 1
    my_posts.append(my_post)
    print(my_posts[-1])
    return {"response": f"Post '{post.title}' was created succesfully", "data" : my_post}


# DELETE /posts --------------------------------------
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    post = find_post(id, my_posts)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
    
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# DELETE /posts --------------------------------------
@app.put("/posts/{id}")
async def put_post(id:int,post:Post):
    i_post = find_post(id, my_posts,'index')
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
    my_posts[i_post] = post.model_dump()
    my_posts[i_post]["id"] = id
    return {"response": f"The post with id '{id}' was updated succesfully", "data": my_posts[i_post]}