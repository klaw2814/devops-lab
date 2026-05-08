from pydantic import BaseModel


class Ticket(BaseModel):
    title: str
    priority: str
    description: str
