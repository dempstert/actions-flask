from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db


class Example(db.Model):
    __tablename__ = 'example'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
