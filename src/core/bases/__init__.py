from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import SETTINGS



class Base(DeclarativeBase):
    """
        Base class for SQLAlchemy declarative model classes.
    """
    pass



class DatabaseSession:
    """
        Class to manage SQLAlchemy database sessions.
    """


    def __init__(self, url: str = SETTINGS.DATABASE_URL) -> None:
        """
            Initialize an instance of DatabaseSession.

            Args:
                url (str): The database URL. Defaults to the URL defined in the settings.
        """
        self.engine = create_engine(url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )


    def create_all(self) -> None:
        """
            Create all tables in the database defined in the Base class metadata.
        """
        Base.metadata.create_all(self.engine)


    def close(self) -> None:
        """
            Close the connection to the database.
        """
        self.engine.dispose()


    def __enter__(self):
        """
            Entry method for using the instance in a 'with' block. Opens a database session.
        """
        self.session = self.SessionLocal()
        return self.session


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Exit method for using the instance in a 'with' block. Closes the database session.

            Args:
                exc_type: Type of exception.
                exc_val: Exception value.
                exc_tb: Traceback of the exception.
        """
        self.session.close()


    def commit_rollback(self) -> None:
        """
            Attempt to commit the current session. If an exception occurs, perform a rollback.

            Raises:
                Exception: Raises an exception if the commit fails and performs a rollback.
        """
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise



# Create a global instance of DatabaseSession for use in other parts of the code.
CONNECTION_DATABASE = DatabaseSession()
