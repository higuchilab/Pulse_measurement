from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """
    SQLAlchemyセッションのコンテキストマネージャー
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Session rollback due to: {e}")
        raise
    finally:
        session.close()