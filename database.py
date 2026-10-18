from sqlmodel import SQLModel, Session, create_engine
from models.restaurant import Restaurant


DB_PATH = "sqlite:///data/restaurants.db"
engine = create_engine(DB_PATH)

def create_db():
    SQLModel.metadata.create_all(engine)

# 供後續操作資料庫用
def get_session():
    with Session(engine) as session:
        yield session
