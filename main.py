from fastapi import FastAPI

app = FastAPI()

@app.get('/') # <- decorator
def index():
    return {'data': {'name': 'Vinay'}}

@app.get('/about')
def about():
    return {'data':'about page'}