import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from common.env import SQL_INSTANCE_URI


engine = create_engine(SQL_INSTANCE_URI)
Session = sessionmaker(bind=engine)


def sql_execute_on_session(session, sql_command):
    return session.execute(sql_command)


def session_wrap(function_handler, auto_flush=False):
    def wrap(*args, **kwargs):
        session = Session(autoflush=auto_flush)
        kwargs['session'] = session

        try:
            result = function_handler(*args, **kwargs)
        except Exception as e:
            session.rollback()
            logging.error("SQL Commit Error: {}".format(e))
            raise e
        finally:
            session.close()

        return result
    return wrap
