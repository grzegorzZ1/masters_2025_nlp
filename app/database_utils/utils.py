from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Optional
from sqlalchemy import Date, Text, ARRAY

class Base(DeclarativeBase):
    pass

class Speech(Base):
    __tablename__ = "speeches"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    doc_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    words: Mapped[List[str]] = mapped_column(ARRAY(Text), default=list)
    entity_names: Mapped[List[str]] = mapped_column(ARRAY(Text), default=list)
    entity_ids: Mapped[List[str]] = mapped_column(ARRAY(Text), default=list)


def init_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)