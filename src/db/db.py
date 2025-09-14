from ..core.settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine(settings.DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db() -> None:
    from ..db.models.user_models import table_registry, UserModel

    print("Criando tabelas no banco de dados...")
    print(table_registry.metadata)

    with engine.begin() as conn:
        table_registry.metadata.create_all(conn)

if __name__ == "__main__":
    init_db()
