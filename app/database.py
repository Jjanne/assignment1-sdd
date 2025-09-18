from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./rideplanner.sqlite3"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from . import models
    SQLModel.metadata.create_all(engine)
