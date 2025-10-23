from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel

app = FastAPI() # creates instance of fastapi

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Blog is created with the title {request.title}'}

@app.get('/blog') # <- decorator
def index(limit = 10, published : bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} blogs from the database'}
    return {'data': f'{limit} unpublished blogs from the database'}



@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog where id = {id}
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of blog with id = {id}
    return {'data': {'1', '2'}}


