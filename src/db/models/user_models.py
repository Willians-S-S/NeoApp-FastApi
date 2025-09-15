from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, Table
from sqlalchemy.orm import Mapped, registry, mapped_column

table_registry = registry()

@table_registry.mapped_as_dataclass
class UserModel:
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)  
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String(20))
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)

    creat_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
