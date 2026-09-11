from app.database.database import Base, engine
from app.database.models import TransactionRecord


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("DB tables created")