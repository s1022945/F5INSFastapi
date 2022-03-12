from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user

class dbSetting_mysql:
    user_name: str
    password: str
    host: str
    database_name: str
    SQLALCHEMY_DATABASE_URL: str
    engine: Engine
    session: sessionmaker
    def __init__(self, user_name, password, host, database_name):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.database_name = database_name
        self.SQLALCHEMY_DATABASE_URL = f'mysql://{user_name}:{password}@{host}/{database_name}?charset=utf8'
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

class dbSetting_sqlite:
    database_name: str
    SQLALCHEMY_DATABASE_URL: str
    engine: Engine
    session: sessionmaker
    def __init__(self, database_name):
        self.database_name = database_name
        self.SQLALCHEMY_DATABASE_URL = f'sqlite:///{database_name}'
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

# dbSetting_cf5insp_1e1r = dbSetting_mysql("edc", "xhon1105", "TW069203P:3306", "cf5insp_1e1r")
dbSetting_F5INSRPT = dbSetting_mysql("cfins", "cf5ins", "10.91.40.115:3306", "F5INSRPT")

# dbSetting_SPME01 = dbSetting_sqlite("./app/dashboard/database/SPME01.db")
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL: str = 'mysql://edc:xhon1105@localhost:3306/cf5insp_1e1r?charset=utf8&auth_plugin=mysql_native_password'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
Base = declarative_base()
