from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##Mysql
#URL_DATABASE1 = 'mysql+pymysql://root:123456@localhost:3306/baseapplication'
#(資料庫名稱)+(聯絡的資料庫套件)://(帳號):(密碼)@(IP):(PORT)/(schema)

##Mssql (version : 18)
driver = "ODBC Driver 18 for SQL Server"
URL_DATABASE2 = f"mssql+pyodbc://sa:123456@127.0.0.1/baseapplication?TrustServerCertificate=yes&driver={driver}"
#(資料庫名稱)+(聯絡的資料庫套件)://(帳號):(密碼)@(IP)/(schema)?TrustServerCertificate=yes&driver={driver}
#TrustServerCertificate=yes : 信任加密憑證驗證(不想找麻煩一定要打)
#diver : MSSQL VERSION 18 後一定要加的東西

#建立與資料庫的連接( 牽線而已，並無開始聯絡
engine = create_engine(URL_DATABASE2, echo=True)
#建立與資料庫的雙向聯絡
SessionLocal = sessionmaker(autoflush=False, bind=engine)
