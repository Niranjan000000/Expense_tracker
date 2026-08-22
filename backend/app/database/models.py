from sqlalchemy import Column,Integer,String,DateTime,Boolean,VARCHAR
from sqlalchemy.orm import declarative_base
from datetime import datetime
from app.database.base import Base



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column("Name", String(250), nullable=False)

    email = Column("email", String(250), nullable=False)

    password_hash = Column(
        "password_hash",
        String(250),
        nullable=False
    )

    created_date = Column(
        "created_date",
        DateTime,
        nullable=False,
        default=datetime.now
    )

    account_status = Column(
        "account_status",
        Boolean,
        default=True
    )


    class Expense(Base):
    __tablename__ = "expense"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    expense_date = Column(Date,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )