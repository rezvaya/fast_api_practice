from sqlmodel import create_engine, SQLModel

engine = create_engine('urls.db')

def init_db():
    SQLModel.metadata.create_all(engine)