from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False) # foreign key
    expense_name = Column(String(50))
    amount = Column(Float, nullable=False)
    expense_type = Column(String(1), nullable=False) # only store m = monthly, y = yearly, d = daily

    user = relationship("User", back_populates="expenses")
