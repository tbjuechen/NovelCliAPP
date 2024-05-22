from config.database import SessionLocal

# 返回数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()