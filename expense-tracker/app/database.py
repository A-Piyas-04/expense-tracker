from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql+psycopg2://expense_user:expense_pass@localhost:5433/expense_db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session