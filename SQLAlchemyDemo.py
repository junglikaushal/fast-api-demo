from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

app = FastAPI()
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/test_db"

engine = create_engine(DATABASE_URL, echo=False)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(db: Session = Depends(get_db)):
    return {"message": "SQLAlchemy database is connected successfully!"}


@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@app.post("/todo/create")
def create_todo(title: str = None, db: Session = Depends(get_db)):
    todo = Todo(title=title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "Todo created successfully!", "todo": todo}


@app.get("/todo/read/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return {"message": "Todo found!", "todo": todo}
    else:
        return {"message": "Todo not found!"}


@app.put("/todo/update/{todo_id}")
def update_todo(todo_id: int, title: str = None, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.title = title
        db.commit()
        db.refresh(todo)
        return {"message": "Todo updated successfully!", "todo": todo}
    else:
        return {"message": "Todo not found!"}


@app.delete("/todo/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully!"}
    else:
        return {"message": "Todo not found!"}
