from pydantic import BaseModel
from typing import Literal

# For creating a new expense
class ExpenseCreate(BaseModel):
    amount: float
    expense_name: str
    expense_type: Literal['m', 'y', 'd']  # monthly, yearly, daily

# For reading expense info
class ExpenseRead(BaseModel):
    id: int
    user_id: int
    expense_name: str
    amount: float
    expense_type: Literal['m', 'y', 'd']

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

# Optional: Update schema
class ExpenseUpdate(BaseModel):
    amount: float | None = None
    expense_type: Literal['m', 'y', 'd'] | None = None