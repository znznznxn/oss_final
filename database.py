from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_talk.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 모든 테이블을 삭제하고 다시 생성하는 함수
def reset_database():
    meta = MetaData()
    meta.reflect(bind=engine)
    with engine.connect() as conn:
        # 모든 테이블 삭제
        for table in reversed(meta.sorted_tables):
            conn.execute(text(f"DROP TABLE IF EXISTS {table.name}"))
        # 모든 테이블 다시 생성
        Base.metadata.create_all(bind=engine)

# 사용 예제
#if __name__ == "__main__":
#    reset_database()
#    print("Database has been reset")
