from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = "mysql+pymysql://root:community@127.0.0.1:3306/community"

engine = create_engine(DATABASE_URL)  # echo = True 로그 너무많이뜸
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
