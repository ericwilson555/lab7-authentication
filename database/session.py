from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./lab7.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    SQLModel.metadata.create_all(engine)