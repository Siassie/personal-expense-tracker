from app.core.database import Base
from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(100))
    email = Column(String(70), unique = True, index=True)
    password = Column(String(250))

    expenses = relationship("Expenses", back_populates="user", cascade="all, delete")
