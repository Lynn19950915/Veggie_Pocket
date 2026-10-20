from sqlmodel import SQLModel, Session, create_engine
# 確保類別 Model 有載入
from models.restaurant import Restaurant


DB_PATH = "sqlite:///data/restaurants.db"
engine = create_engine(
    DB_PATH, connect_args={"check_same_thread": False}
)

# 不會修改已存在的資料表結構
def create_db():
    SQLModel.metadata.create_all(engine)

# 供後續操作資料庫 (請求) 專用
def get_session():
    with Session(engine) as session:
        yield session
