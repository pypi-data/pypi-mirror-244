import importlib
from contextlib import contextmanager

from lesscode_database.db_options import db_options


class DsHelper:
    def __init__(self, pool_name):
        self.pool, self.conn_info = getattr(db_options, pool_name)

    def exec(self, method: str, *args, **kwargs):
        return getattr(self.pool, method)(*args, **kwargs)

    async def async_exec(self, method: str, *args, **kwargs):
        return await getattr(self.pool, method)(*args, **kwargs)

    @contextmanager
    def make_session(self, **kwargs):
        try:
            sqlalchemy_orm = importlib.import_module("sqlalchemy.orm")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        session = None
        try:
            db_session = sqlalchemy_orm.scoped_session(sqlalchemy_orm.sessionmaker(bind=self.pool, **kwargs))
            session = db_session()
            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        else:
            session.commit()
        finally:
            if session:
                session.close()
