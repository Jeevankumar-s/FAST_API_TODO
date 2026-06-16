from fastapi import FastAPI, Depends, HTTPException;
from schemas import Todo as TodoSchema, TodoCreate;
from sqlalchemy.orm import Session;
from database import sessionLocal, Base, engine;
from models import Todo, User
from schemas import User as UserSchema, CreateUser; 
import httpx
import time
import asyncio

Base.metadata.create_all(bind = engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Create TODO
@app.post("/todos", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(instance=db_todo)
    return db_todo

# GET - All Todo
@app.get("/todos", response_model=list[TodoSchema])
def get_todos(db:Session = Depends(get_db)):
    return db.query(Todo).all()

# GEt - Single TODO
@app.get("/todos/{todo_id}", response_model=TodoSchema)
def get_single_todo(todo_id: int, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code = 404, detail= "Todo not found")
    else:
        return todo

# PUT - Update TODO
@app.put("/todos/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, updated: TodoCreate ,db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code = 404, detail = "Todo not found")
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo
    
# Delete - delete todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int , db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {
        "message": "Todo Deleted Successfully"
    }

# User - Create User
@app.post("/users", response_model = UserSchema)
def create_user(user: CreateUser, db:Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(instance=db_user)
    return db_user

# User - get all user
@app.get("/users", response_model = list[UserSchema])
def get_all_user(db: Session = Depends(get_db)):
    return db.query(User).all()

# User - get single user
@app.get("/users/{user_id}", response_model = UserSchema)
def get_single_user(user_id: int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id ==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user
    
# get jokes - sync
@app.get("/jokes-sync")
def get_sync_jokes():
    joke_url = "https://official-joke-api.appspot.com/random_joke"
    jokes=[]
    startTime=time.time()
    with httpx.Client() as client:
        for _ in range(10):
            res = client.get(joke_url)
            data=res.json()
            print(data)
            jokes.append({"setup":data['setup'], "punchline":data['punchline']})
    elapsed=time.time()-startTime
        
    return {
        "jokes":jokes,
        "timeTaken":elapsed,
        "message":"success",
    }

# GET Jokes - Async
@app.get("/jokes-async")
async def get_async_jokes():
    joke_url = "https://official-joke-api.appspot.com/random_joke"
    jokes=[]
    startTime=time.time()
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            res = await client.get(joke_url)
            data=res.json()
            print(data)
            jokes.append({"setup":data['setup'], "punchline":data['punchline']})
    elapsed=time.time()-startTime
        
    return {
        "jokes":jokes,
        "timeTaken":elapsed,
        "message":"success",
    }