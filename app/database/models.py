from sqlalchemy import Column, Integer, String

from app.database.database import Base


class TicketRecord(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(String)
    description = Column(String)
