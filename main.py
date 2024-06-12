from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from icecream import ic
import uvicorn
import models


# 創建FastAPI 應用程序
app = FastAPI()
# 在資料庫中創建在models.py內已經定義好的資料表並初始化
# 若要聯絡的資料表已經創建好了下行即可註解(不註解不影響執行)
# models.Base.metadata.create_all(bind=engine)


# 定義 Pydantic 模型
# 這和 ORM 模型關係密切!! 順序可跟資料表不一樣，一定型別要一樣。
# uvicorn 可驗證
class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

class U_tableBase(BaseModel):
    u_name: str
    u_age: int
    u_email: str

# 先知道 SessionLocal() 長什麼樣子
# 執行 : ic(db_session.__dict__)
# 結果如下
# ic| db_session.__dict__: {'_Session__binds': {},
#                           '_close_state': <_SessionCloseState.CLOSE_IS_RESET: 3>,
#                           '_deleted': {},
#                           '_flushing': False,
#                           '_nested_transaction': None,
#                           '_new': {},
#                           '_query_cls': <class 'sqlalchemy.orm.query.Query'>,
#                           '_transaction': None,
#                           '_warn_on_events': False,
#                           'autobegin': True,
#                           'autoflush': False,
#                           'bind': Engine(mssql+pyodbc://sa:***@127.0.0.1/baseapplication?TrustServerCertificate=yes&driver=ODBC+Driver+18+for+SQL+Server),
#                           'enable_baked_queries': True,
#                           'expire_on_commit': True,
#                           'hash_key': 1,
#                           'identity_map': <sqlalchemy.orm.identity.WeakInstanceDict object at 0x00000269181B24D0>,
#                           'join_transaction_mode': 'conditional_savepoint',
#                           'twophase': False}

# 每次操作get_db_session時，db使用SessionLocal中提供的資料與資料庫連線，產生db存儲。完事後關閉，避免資源堆積和資料流出。
# 每次跟資料庫聯絡必定執行的function，由下面的Depends()操作
def get_db_session():
    db_session = SessionLocal()
    # ic(db_session.__dict__) #監控get_db_session()執行的動作
    try:
        yield db_session
    finally:
        db_session.close()
    # return db_session #也可改用return

# 一個db的dependency，可以看做是要操作的db，這裡的Depends對應get_db，get_db對應SessionLocal
# 自定義資料驗證，Depends(dependency=get_db_session) 回傳的資料型別一定要是Session
# 將自定義的資訊給db_dependency，這裡的用意是方便各CRUD 方法使用， 若不用可查看使用SQL語法查詢的方法
# (參考 : https://medium.com/@King610160/fastapi-sqlalchemy-postgresql-fastapi%E7%9A%84orm-00818bc63106
# (參考 : https://stackoverflow.com/questions/64763770/why-we-use-yield-to-get-sessionlocal-in-fastapi-with-sqlalchemy
db_dependency = Annotated[Session, Depends(dependency=get_db_session)]

# 新增資料至users表單
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

# 新增資料至posts表單
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_user(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()

# 新增資料至u_table表單
@app.post("/u_table/", status_code=status.HTTP_201_CREATED)
async def create_user(u_table: U_tableBase, db: db_dependency):
    db_post = models.U_table(**u_table.model_dump())
    db.add(db_post)
    db.commit()

# first() -> 搜尋到的結果的第一筆，型態:dict
# all() -> 搜尋到的所有結果，型態:list 包 dict -> [{},{}]

# 修改指定資料
@app.put("/u_table", status_code=status.HTTP_200_OK)
async def edit_u_table(u_id: int, Upate_table: U_tableBase,db: db_dependency):
    result = db.query(models.U_table).filter(models.U_table.id == u_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Can't delete!! u_id: {u_id} was not found in u_table")
    result.u_name = Upate_table.u_name
    result.u_age = Upate_table.u_age
    result.u_email = Upate_table.u_email
    db.commit()
    db.refresh(result)
    return result

# 刪除指定資料
@app.delete("/u_table/{u_id}", status_code=status.HTTP_200_OK)
async def delete_u_table(u_id: int, db: db_dependency):
    result = db.query(models.U_table).filter(models.U_table.id == u_id).all()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Can't delete!! u_id: {u_id} was not found in u_table")
    for data in result:
        db.delete(data)
        db.commit()

# 查詢u_table內的資料
@app.get('/u_table/{u_id}', status_code=status.HTTP_200_OK)
async def search_u_table(u_id: str, db: db_dependency):
    result = db.query(models.U_table).filter(models.U_table.id == u_id).all()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Can't search!! u_id: {u_id} was not found in u_table")
    return result

# 查詢u_table全部的資料
@app.get('/u_table/', status_code=status.HTTP_200_OK)
async def search_all_u_table(db: db_dependency):
    result = db.query(models.U_table).all()
    return result

# 查詢air_shop全部的資料(使用SQL語法)
# !!!極推薦!!! 若已在資料庫建立資料表，不須再建立ORM模型就即可使用
@app.get('/air_shop_all/', status_code=status.HTTP_200_OK)
async def search_all_air_shop_with_sql(db: Session = Depends(get_db_session)): #db設置的另一種方法
    result = db.execute(text('SELECT u_id, u_name, u_age, u_email FROM air_shop'))
    data = []
    for row in result.fetchall():
        data.append({list(result.keys())[i]: value for i, value in enumerate(row)})
    return data

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)
