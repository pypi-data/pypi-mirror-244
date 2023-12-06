import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import urllib.parse
from ..env import getEnv, getEnvBool, getEnvInt

def newMysqlEngine(user, password, host, port, db, **kwargs):
    password = urllib.parse.quote_plus(password)
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4",**kwargs)


# engine = create_engine(
#     f"mysql+pymysql://{getEnv('MYSQL_USER', 'root')}:{getEnv('MYSQL_PASSWORD')}@{getEnv('MYSQL_HOST', 'localhost')}:{getEnv('MYSQL_PORT', '3306')}/{getEnv('MYSQL_DB')}?charset=utf8mb4",
#     echo=getEnvBool("IS_DEV"), echo_pool=getEnvBool("IS_DEV"), pool_recycle=getEnvInt('MYSQL_POOL_RECYCLE', 3600),
#     pool_pre_ping=True, pool_size=getEnvInt('MYSQL_POOL_SIZE', 100))

mysqlEngineEnv = newMysqlEngine(getEnv('MYSQL_USER', 'root'), getEnv('MYSQL_PASSWORD'), getEnv('MYSQL_HOST', 'localhost'), 
                       getEnv('MYSQL_PORT', '3306'), getEnv('MYSQL_DB'), echo=getEnvBool("IS_DEV"), 
                       echo_pool=getEnvBool("IS_DEV"), pool_recycle=getEnvInt('MYSQL_POOL_RECYCLE', 3600),
                        pool_pre_ping=True, pool_size=getEnvInt('MYSQL_POOL_SIZE', 100))

Base = declarative_base()


@contextmanager
def yieldSession(expunge_all=True,engine=mysqlEngineEnv) ->Generator[Session, None, None]:
    """
    with yieldSession() as session:
    """
    session = None
    try:
        session = Session(engine)
        yield session
        session.flush()
        if expunge_all:
            session.expunge_all()
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(e)
        raise e
    finally:
        if session:
            session.close()
