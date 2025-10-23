from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, Sessionlocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not available')
    return blog



@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} does not exist.')
    
    blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not available')
    
    blog.update({'title': request.title, 'body': request.body})
    db.commit()

    return 'updated'
    

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist.')
    
    return user

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} does not exist.')

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)