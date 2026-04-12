from sqlmodel import SQLModel, create_engine, Session
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)