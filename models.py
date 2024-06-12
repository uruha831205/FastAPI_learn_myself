from sqlalchemy import Boolean, Column, Integer, String
#from database import Base
from sqlalchemy.ext.declarative import declarative_base

#PS: 如果要聯絡的資料表已經建立好在資料庫(schema)內，一樣要照資料表欄位和型態來建立ORM模型

#創建 SQLAlchemy ORM 模型
Base = declarative_base()

#以下三個資料表

#資料庫建立表單(一定要繼承 database.py的Base
class User(Base):
    #資料表名稱
    __tablename__  = 'users'

    #欄位及欄位參數
    id = Column(Integer, primary_key=True, index=True)#參數:index=True -> 自動生成編號，有這個參數的欄位，新增資料至資料表內時無需參考此欄位
    username = Column(String(50), unique=True)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    title = Column(String(50), unique=True)
    content = Column(String(50), unique=True)

#實驗 - 此表單已在資料庫上建立
#驗證 : 訪問OK。 
#PS : 訪問成功條件 : 欄位數量和參數一定要一樣!! 
#欄位數量不一樣 : 錯誤回報代碼=>500 ; 參數數量不一樣或有一個及以上不同 : 錯誤回報代碼=>422
class U_table(Base):
    __tablename__  = 'u_table'

    id = Column(Integer, primary_key=True, index=True)
    u_name = Column(String(50), nullable=False)
    u_age = Column(Integer, nullable=False)
    u_email = Column(String(100), nullable=False, unique=True)
    

